"""
Real implementations of the `MutationRunner` and `LLMClient` Protocols
(see interfaces.py), replacing the Fakes used in examples/demo_run.py.

MutmutMutationRunner
    Runs mutmut in an isolated temp workdir (same recipe as
    baselines/score.py, which is the one already verified end-to-end in
    toolchain_check.py) and, for every surviving mutant, calls
    `mutmut show <key>` to pull the real unified diff -- the original line,
    the mutated line, and the line number. This is Member 2's job in
    principle; evaluation/mutation_runner.py and evaluation/evaluator.py are
    not usable yet (evaluator.py has a broken import -- see note at bottom of
    this file -- and neither returns per-mutant survivor detail, only a raw
    report string). This adapter unblocks Member 4 in the meantime; swap it
    for Member 2's pipeline once evaluator.py implements the same contract.

GeminiTextClient
    Wraps google-genai directly for **plain text** generation (no
    response_schema), because prompt_strategies.py asks the model to return
    a raw pytest file, not a structured object. baselines/llm_client.py
    can't be reused as-is here since its `generate()` always requires a
    pydantic response_model.

GroqTextClient / GroqStructuredClient
    Same two roles as GeminiTextClient, but talking to Groq's OpenAI-
    compatible REST API instead. Added because the project's Gemini Cloud
    project started returning 403 PERMISSION_DENIED ("Your project has been
    denied access") independent of the key itself -- consistent with the key
    having been exposed. GroqTextClient satisfies the same `LLMClient`
    Protocol as GeminiTextClient (structural typing -- RefinementLoop takes
    either with zero changes). GroqStructuredClient duck-types
    baselines.llm_client.LLMClient (same `.generate(...)` signature and
    `.tracker` attribute) so it drops into `baseline_a.run(ctx, client=...)`
    for the seed call. Implemented with stdlib `urllib` rather than the
    `groq` package to avoid adding a dependency neither Member 2 nor Member 3
    otherwise need.

Known simplifications (documented rather than hidden, same policy as the
rest of the repo):
  - `mutant_operator` is inferred with a small token-diff heuristic, since
    mutmut 3.x doesn't expose the operator name through `show` or the meta
    file. Good enough for RQ4's rough operator-class buckets; not a
    substitute for reading mutmut's internal mutation registry.
  - `covering_test_names` / `failing_assertions` are approximated as "every
    test in the current suite" / "every assert line in the current suite",
    because mutmut's exit-code-per-mutant granularity doesn't tell us which
    specific test or assertion ran against which mutant without per-mutant
    coverage instrumentation (out of scope for a v0.1).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

from baselines import config as baselines_config
from baselines.llm_client import _retry_delay_seconds
from .models import MutationResult, SurvivingMutant

SETUP_CFG = """\
[mutmut]
source_paths={module}.py
pytest_add_cli_args_test_selection=tests/
"""

_ASSERT_RE = re.compile(r"^\s*(assert .+)$", re.MULTILINE)
_TEST_DEF_RE = re.compile(r"^\s*def\s+(test_\w+)\s*\(", re.MULTILINE)

_OPERATOR_GROUPS = [
    ("LogicalOperator", {"and", "or", "not"}),
    ("ComparisonOperator", {"==", "!=", "is", "is not"}),
    ("ConditionalBoundary", {"<", "<=", ">", ">="}),
    ("ArithmeticOperator", {"+", "-", "*", "/", "//", "%", "**"}),
]


def _classify_operator(original_line: str, mutated_line: str) -> str:
    """Best-effort operator label from a token diff of the two lines."""
    orig_tokens = set(re.findall(r"[A-Za-z]+|[+\-*/%<>=!]+", original_line))
    mut_tokens = set(re.findall(r"[A-Za-z]+|[+\-*/%<>=!]+", mutated_line))
    changed = orig_tokens.symmetric_difference(mut_tokens)
    for label, ops in _OPERATOR_GROUPS:
        if changed & ops:
            return label
    return "Unknown"


class MutmutMutationRunner:
    """Implements interfaces.MutationRunner for one fixed function_id."""

    def __init__(self, function_id: str) -> None:
        self.function_id = function_id

    def run(self, function_source: str, test_code: str) -> MutationResult:
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            (workdir / "tests").mkdir()
            (workdir / f"{self.function_id}.py").write_text(
                function_source, encoding="utf-8"
            )
            (workdir / "tests" / f"test_{self.function_id}.py").write_text(
                test_code, encoding="utf-8"
            )
            (workdir / "setup.cfg").write_text(
                SETUP_CFG.format(module=self.function_id), encoding="utf-8"
            )

            # coverage, for RunLog.line_coverage_pct
            subprocess.run(
                [sys.executable, "-m", "coverage", "run",
                 f"--source={self.function_id}", "-m", "pytest", "-q", "tests/"],
                cwd=workdir, capture_output=True, text=True, timeout=300,
            )
            subprocess.run(
                [sys.executable, "-m", "coverage", "json", "-o", "cov.json"],
                cwd=workdir, capture_output=True, text=True, timeout=120,
            )
            coverage_pct = 0.0
            cov_path = workdir / "cov.json"
            if cov_path.exists():
                coverage_pct = json.loads(cov_path.read_text(encoding="utf-8"))[
                    "totals"
                ]["percent_covered"]

            # mutation run. Invoked as `-m mutmut` rather than a `mutmut`
            # console script, since sys.executable and pip's installed
            # console-script bin dir aren't guaranteed to be the same
            # directory outside a venv (e.g. Colab's system Python).
            subprocess.run(
                [sys.executable, "-m", "mutmut", "run"],
                cwd=workdir, capture_output=True, text=True, timeout=1800,
            )

            meta_path = workdir / "mutants" / f"{self.function_id}.py.meta"
            total = killed = 0
            survivor_keys: list[str] = []
            if meta_path.exists():
                exit_codes = json.loads(meta_path.read_text(encoding="utf-8"))[
                    "exit_code_by_key"
                ]
                total = len(exit_codes)
                # Non-zero exit code == suite failed against the mutant == killed.
                # Zero == suite still passed on mutated code == survived.
                killed = sum(1 for code in exit_codes.values() if code != 0)
                survivor_keys = [k for k, code in exit_codes.items() if code == 0]

            covering_tests = _TEST_DEF_RE.findall(test_code)
            failing_assertions = _ASSERT_RE.findall(test_code)

            survivors = [
                self._survivor_from_key(workdir, key, covering_tests, failing_assertions)
                for key in survivor_keys
            ]
            survivors = [s for s in survivors if s is not None]

        return MutationResult(
            total_mutants=total,
            killed_mutants=killed,
            survivors=survivors,
            line_coverage_pct=round(coverage_pct, 1),
        )

    def _survivor_from_key(
        self,
        workdir: Path,
        key: str,
        covering_tests: list[str],
        failing_assertions: list[str],
    ) -> SurvivingMutant | None:
        result = subprocess.run(
            [sys.executable, "-m", "mutmut", "show", key],
            cwd=workdir, capture_output=True, text=True, timeout=60,
        )
        line_number, original_line, mutated_line = _parse_diff(result.stdout)
        if original_line is None:
            return None
        return SurvivingMutant(
            mutant_id=key,
            mutant_operator=_classify_operator(original_line, mutated_line),
            line_number=line_number,
            original_line=original_line,
            mutated_line=mutated_line,
            failing_assertions=failing_assertions[:3],
            covering_test_names=covering_tests,
        )


def _parse_diff(diff_text: str) -> tuple[int, str | None, str | None]:
    """Pull (line_number, original_line, mutated_line) out of `mutmut show` output."""
    line_no = 0
    original_line = mutated_line = None
    for line in diff_text.splitlines():
        hunk = re.match(r"^@@ -(\d+),\d+ \+\d+,\d+ @@", line)
        if hunk:
            line_no = int(hunk.group(1))
            continue
        if not line_no:
            continue
        if line.startswith("-") and not line.startswith("---"):
            if original_line is None:
                original_line = line[1:]
                captured_at = line_no
            line_no += 1
        elif line.startswith("+") and not line.startswith("+++"):
            if mutated_line is None:
                mutated_line = line[1:]
        elif line.startswith(" "):
            line_no += 1
        if original_line is not None and mutated_line is not None:
            return captured_at, original_line, mutated_line
    return line_no, original_line, mutated_line


class GeminiTextClient:
    """Implements interfaces.LLMClient with a live, unstructured Gemini call."""

    def __init__(self, model: str | None = None) -> None:
        from google import genai

        api_key = baselines_config.api_key()
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not set. Put it in .env or the environment "
                "before running the refinement loop live."
            )
        self.model = model or baselines_config.MODEL_ID
        self._client = genai.Client(api_key=api_key)

    def generate(self, user_prompt: str, system_prompt: str = "") -> tuple[str, int]:
        from google.genai import types

        request_config = types.GenerateContentConfig(
            system_instruction=system_prompt or None,
            temperature=baselines_config.TEMPERATURE,
            max_output_tokens=baselines_config.MAX_OUTPUT_TOKENS,
        )
        response = self._call_with_retry(user_prompt, request_config)
        usage = response.usage_metadata
        thoughts = getattr(usage, "thoughts_token_count", None) or 0
        total = usage.total_token_count or (
            (usage.prompt_token_count or 0) + (usage.candidates_token_count or 0) + thoughts
        )
        text = (response.text or "").strip()
        # Model sometimes wraps output in ```python fences despite instructions
        # not to -- strip them defensively rather than let a bad suite in.
        if text.startswith("```"):
            text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        return text, total

    def _call_with_retry(self, user_prompt: str, request_config):
        """Same 429-handling policy as baselines/llm_client.py: honour the
        server's own retryDelay, cap retries, re-raise anything else. A
        full-scale run (30 functions x 2 variants x up to 6 calls each) hits
        429s routinely, not exceptionally -- see MAX_RETRIES/MAX_RETRY_DELAY
        in baselines/config.py."""
        last_error: Exception | None = None
        for attempt in range(baselines_config.MAX_RETRIES + 1):
            try:
                return self._client.models.generate_content(
                    model=self.model, contents=user_prompt, config=request_config,
                )
            except Exception as exc:  # noqa: BLE001
                message = str(exc)
                if "429" not in message and "RESOURCE_EXHAUSTED" not in message:
                    raise
                last_error = exc
                if attempt == baselines_config.MAX_RETRIES:
                    break
                delay = _retry_delay_seconds(message)
                print(f"    [refinement] rate limited, waiting {delay:.0f}s "
                      f"(attempt {attempt + 1}/{baselines_config.MAX_RETRIES})")
                time.sleep(delay)
        raise last_error  # type: ignore[misc]


# --- Groq (OpenAI-compatible) ----------------------------------------------
GROQ_API_KEY_ENV = "GROQ_API_KEY"
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
# llama-3.3-70b-versatile: solid coding benchmark scores, available on Groq's
# free tier. TODO(team): re-verify pricing below before it goes in the paper,
# same caveat as PRICE_PER_1M_INPUT_USD in baselines/config.py -- Groq's
# pricing page is the source of truth, this is a snapshot.
GROQ_MODEL_ID = os.getenv("GROQ_MODEL_ID", "llama-3.3-70b-versatile")
GROQ_PRICE_PER_1M_INPUT_USD = float(os.getenv("GROQ_PRICE_IN", "0.59"))
GROQ_PRICE_PER_1M_OUTPUT_USD = float(os.getenv("GROQ_PRICE_OUT", "0.79"))


def groq_api_key() -> str | None:
    return os.getenv(GROQ_API_KEY_ENV) or None


def has_groq_key() -> bool:
    return bool(groq_api_key())


def _groq_chat(
    messages: list[dict],
    *,
    temperature: float,
    max_tokens: int,
    model: str,
    response_format: dict | None = None,
    max_retries: int = 3,
) -> tuple[str, int, int, int]:
    """POST to Groq's chat/completions endpoint. Returns
    (content, prompt_tokens, completion_tokens, total_tokens).

    Same 429-handling policy as baselines/llm_client.py._call_with_retry:
    honour the server's Retry-After header, cap retries, re-raise anything
    else. Implemented with urllib rather than requests/the groq SDK so this
    file adds zero new entries to requirements.txt.
    """
    api_key = groq_api_key()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY not set. Put it in .env or the environment before "
            "running with --provider groq."
        )
    body: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if response_format:
        body["response_format"] = response_format

    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        request = urllib.request.Request(
            GROQ_BASE_URL,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                # Cloudflare (fronting api.groq.com) returns a 403/"error
                # code: 1010" for urllib's default User-Agent
                # (Python-urllib/x.y) -- documented Cloudflare behavior is
                # that non-browser UA strings get blocked at the edge before
                # the request reaches the origin at all (see Cloudflare
                # community reports on error 1010). Not verified against a
                # live call from this environment -- this sandbox can't
                # reach api.groq.com -- so treat this as the leading
                # hypothesis fix, and if a browser-shaped UA still 403s,
                # switch _groq_chat to the official `groq` package instead of
                # tuning headers further blind.
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                ),
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                payload = json.loads(response.read().decode("utf-8"))
            content = payload["choices"][0]["message"]["content"] or ""
            usage = payload.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)
            return content, prompt_tokens, completion_tokens, total_tokens
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            if exc.code != 429:
                raise RuntimeError(f"Groq API error {exc.code}: {error_body[:400]}") from exc
            last_error = RuntimeError(f"Groq 429: {error_body[:200]}")
            if attempt == max_retries:
                break
            retry_after = exc.headers.get("Retry-After")
            delay = float(retry_after) + 2 if retry_after else 30.0
            print(f"    [groq] rate limited, waiting {delay:.0f}s "
                  f"(attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)
    raise last_error  # type: ignore[misc]


class GroqTextClient:
    """Implements interfaces.LLMClient with a live Groq call. Drop-in
    alternative to GeminiTextClient for refinement rounds."""

    def __init__(self, model: str | None = None) -> None:
        if not has_groq_key():
            raise RuntimeError(
                "GROQ_API_KEY not set. Put it in .env or the environment "
                "before running with --provider groq."
            )
        self.model = model or GROQ_MODEL_ID

    def generate(self, user_prompt: str, system_prompt: str = "") -> tuple[str, int]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        content, _prompt_tok, _completion_tok, total = _groq_chat(
            messages,
            temperature=baselines_config.TEMPERATURE,
            max_tokens=baselines_config.MAX_OUTPUT_TOKENS,
            model=self.model,
        )
        text = content.strip()
        if text.startswith("```"):
            text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        return text, total


class GroqStructuredClient:
    """Duck-types baselines.llm_client.LLMClient (same `.generate(...)`
    signature and `.tracker` attribute) so it drops into
    `baseline_a.run(ctx, client=...)` for the seed call, using Groq instead
    of Gemini. Groq's JSON mode (response_format={"type": "json_object"})
    is not schema-constrained the way Gemini's response_schema is, so the
    target schema is embedded in the prompt and the response is validated
    client-side, with one retry-with-error-feedback if it doesn't parse."""

    def __init__(self, tracker=None, model: str | None = None) -> None:
        from baselines.llm_client import UsageTracker

        if not has_groq_key():
            raise RuntimeError(
                "GROQ_API_KEY not set. Put it in .env or the environment "
                "before running with --provider groq."
            )
        self.tracker = tracker or UsageTracker()
        self.model = model or GROQ_MODEL_ID

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model,
        label: str,
        temperature: float | None = None,
    ):
        from baselines.llm_client import CallRecord

        schema = response_model.model_json_schema()
        schema_prompt = (
            f"{system_prompt}\n\nRespond with ONLY a single JSON object matching "
            f"this JSON Schema exactly -- no prose, no markdown fences:\n"
            f"{json.dumps(schema)}"
        )
        messages = [
            {"role": "system", "content": schema_prompt},
            {"role": "user", "content": user_prompt},
        ]

        last_error: Exception | None = None
        for attempt in range(2):  # one retry with the validation error fed back
            content, prompt_tok, completion_tok, total = _groq_chat(
                messages,
                temperature=(
                    baselines_config.TEMPERATURE if temperature is None else temperature
                ),
                max_tokens=baselines_config.MAX_OUTPUT_TOKENS,
                model=self.model,
                response_format={"type": "json_object"},
            )
            cleaned = content.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
                cleaned = re.sub(r"\n?```$", "", cleaned)
            try:
                parsed = response_model.model_validate_json(cleaned)
            except Exception as exc:  # noqa: BLE001 -- fed back to the model, then re-raised
                last_error = exc
                messages.append({"role": "assistant", "content": content})
                messages.append({
                    "role": "user",
                    "content": f"That was not valid JSON for the schema ({exc}). "
                               f"Return ONLY the corrected JSON object.",
                })
                continue

            self.tracker.add(
                CallRecord(
                    label=label,
                    input_tokens=prompt_tok,
                    output_tokens=completion_tok,
                    thought_tokens=0,
                    total_tokens=total,
                    model=self.model,
                )
            )
            return parsed

        raise RuntimeError(
            f"[{label}] Groq response never validated against "
            f"{response_model.__name__}: {last_error}"
        )


def groq_cost_usd(input_tokens: int, output_tokens: int) -> float:
    """List-price equivalent for Groq calls, mirroring
    baselines.llm_client.UsageTracker.estimated_cost_usd but with Groq's own
    price table instead of Gemini's -- needed because UsageTracker.summary()
    always prices against baselines.config.PRICE_PER_1M_*, which are Gemini
    figures, and would silently mis-price a Groq-seeded run if reused as-is."""
    return (
        input_tokens / 1_000_000 * GROQ_PRICE_PER_1M_INPUT_USD
        + output_tokens / 1_000_000 * GROQ_PRICE_PER_1M_OUTPUT_USD
    )


# --- Note on evaluation/ (Member 2) ----------------------------------------
# evaluation/evaluator.py currently has `from evaluation.coverage_runner.py
# import run_coverage` -- invalid syntax (a module path can't have `.py` in
# an import statement) -- so it cannot run at all in its current state, and
# separately, run_mutation()/run_coverage() return raw subprocess stdout
# rather than the structured MutationResult this loop (or the shared log
# schema) needs. That's Member 2's fix to make, not something this adapter
# should route around by re-implementing their whole ownership area -- but
# flagging it here so it isn't missed before the Week 4 full-scale run.
