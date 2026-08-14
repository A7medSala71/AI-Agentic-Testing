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
  - The fallback runner leaves `covering_test_names` / `failing_assertions` empty
    rather than inventing attribution. Exact per-mutant assertion attribution is
    a requirement for the final shared Member-2 pipeline.
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
    orig_tokens = set(
        re.findall(r"[A-Za-z]+|[+\-*/%<>=!]+", original_line)
    )
    mut_tokens = set(
        re.findall(r"[A-Za-z]+|[+\-*/%<>=!]+", mutated_line)
    )

    changed = orig_tokens.symmetric_difference(mut_tokens)

    for label, ops in _OPERATOR_GROUPS:
        if changed & ops:
            return label

    return "Unknown"


def _parse_pytest_counts(stdout: str) -> tuple[int, int]:
    """Return (collected, passed) from pytest's summary line."""
    passed = failed = errors = skipped = 0

    for line in reversed(stdout.strip().splitlines()):
        if not any(
            token in line
            for token in (" passed", " failed", " error", " skipped")
        ):
            continue

        for chunk in line.replace("=", " ").split(","):
            parts = chunk.split()

            for i, token in enumerate(parts[:-1]):
                if not token.isdigit():
                    continue

                label = parts[i + 1].rstrip("s")

                if label == "passed":
                    passed = int(token)
                elif label == "failed":
                    failed = int(token)
                elif label == "error":
                    errors = int(token)
                elif label == "skipped":
                    skipped = int(token)

        break

    return passed + failed + errors + skipped, passed


def _estimate_tokens_for_diagnostics(text: str) -> int:
    """
    Conservative token estimate for diagnostics only.

    This is NOT used for billing or experimental metrics. Groq's actual
    usage values returned by the API remain the authoritative token counts.
    """
    return max(1, len(text) // 4)


class MutmutMutationRunner:
    """Implements interfaces.MutationRunner for one fixed function_id."""

    def __init__(self, function_id: str) -> None:
        self.function_id = function_id

    def run(
        self,
        function_source: str,
        test_code: str,
    ) -> MutationResult:

        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)

            (workdir / "tests").mkdir()

            (workdir / f"{self.function_id}.py").write_text(
                function_source,
                encoding="utf-8",
            )

            (workdir / "tests" / f"test_{self.function_id}.py").write_text(
                test_code,
                encoding="utf-8",
            )

            (workdir / "setup.cfg").write_text(
                SETUP_CFG.format(module=self.function_id),
                encoding="utf-8",
            )

            # ---------------------------------------------------------
            # Pass rate + coverage against ORIGINAL source
            # ---------------------------------------------------------

            pytest_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "coverage",
                    "run",
                    f"--source={self.function_id}",
                    "-m",
                    "pytest",
                    "-q",
                    "tests/",
                ],
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=300,
            )

            collected, passed = _parse_pytest_counts(
                pytest_result.stdout
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "coverage",
                    "json",
                    "-o",
                    "cov.json",
                ],
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=120,
            )

            coverage_pct = 0.0
            branch_coverage_pct: float | None = None

            cov_path = workdir / "cov.json"

            if cov_path.exists():
                totals = json.loads(
                    cov_path.read_text(encoding="utf-8")
                )["totals"]

                coverage_pct = totals.get(
                    "percent_covered",
                    0.0,
                )

                if totals.get("num_branches"):
                    branch_coverage_pct = round(
                        100.0
                        * totals.get("covered_branches", 0)
                        / totals["num_branches"],
                        1,
                    )

            # ---------------------------------------------------------
            # Mutation run
            # ---------------------------------------------------------

            mutation_process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "mutmut",
                    "run",
                ],
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=1800,
            )

            meta_path = (
                workdir
                / "mutants"
                / f"{self.function_id}.py.meta"
            )

            if not meta_path.exists():
                detail = (
                    mutation_process.stderr
                    or mutation_process.stdout
                    or "unknown mutmut failure"
                ).strip()

                raise RuntimeError(
                    f"mutmut did not produce its result metadata "
                    f"for {self.function_id}. "
                    f"Exit code={mutation_process.returncode}. "
                    f"{detail[-1000:]}"
                )

            total = 0
            killed = 0
            survivor_keys: list[str] = []

            exit_codes = json.loads(
                meta_path.read_text(encoding="utf-8")
            )["exit_code_by_key"]

            total = len(exit_codes)

            # Non-zero exit code:
            # test suite failed against mutant -> mutant killed.
            #
            # Zero:
            # test suite passed against mutant -> mutant survived.
            killed = sum(
                1
                for code in exit_codes.values()
                if code != 0
            )

            survivor_keys = [
                key
                for key, code in exit_codes.items()
                if code == 0
            ]

            # Do not fabricate per-assertion attribution.
            #
            # The fallback runner only has mutant-level exit codes.
            # Member 2's shared pipeline must provide exact assertion
            # attribution for the final experiment.
            covering_tests: list[str] = []
            failing_assertions: list[str] = []

            survivors = [
                self._survivor_from_key(
                    workdir,
                    key,
                    covering_tests,
                    failing_assertions,
                )
                for key in survivor_keys
            ]

            survivors = [
                survivor
                for survivor in survivors
                if survivor is not None
            ]

        return MutationResult(
            total_mutants=total,
            killed_mutants=killed,
            survivors=survivors,
            line_coverage_pct=round(
                coverage_pct,
                1,
            ),
            pass_rate_pct=(
                round(
                    100.0 * passed / collected,
                    1,
                )
                if collected
                else 0.0
            ),
            branch_coverage_pct=branch_coverage_pct,
        )

    def _survivor_from_key(
        self,
        workdir: Path,
        key: str,
        covering_tests: list[str],
        failing_assertions: list[str],
    ) -> SurvivingMutant | None:

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "mutmut",
                "show",
                key,
            ],
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=60,
        )

        line_number, original_line, mutated_line = _parse_diff(
            result.stdout
        )

        if original_line is None:
            return None

        if mutated_line is None:
            mutated_line = original_line

        return SurvivingMutant(
            mutant_id=key,
            mutant_operator=_classify_operator(
                original_line,
                mutated_line,
            ),
            line_number=line_number,
            original_line=original_line,
            mutated_line=mutated_line,
            failing_assertions=failing_assertions[:3],
            covering_test_names=covering_tests,
        )


def _parse_diff(
    diff_text: str,
) -> tuple[int, str | None, str | None]:
    """
    Pull (line_number, original_line, mutated_line)
    out of `mutmut show` output.
    """

    line_no = 0
    original_line = None
    mutated_line = None
    captured_at = 0

    for line in diff_text.splitlines():

        hunk = re.match(
            r"^@@ -(\d+),\d+ \+\d+,\d+ @@",
            line,
        )

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

        if (
            original_line is not None
            and mutated_line is not None
        ):
            return (
                captured_at,
                original_line,
                mutated_line,
            )

    return (
        line_no,
        original_line,
        mutated_line,
    )


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
        self.last_call_cost_usd = 0.0
        self.num_calls = 0
        self.total_tokens_used = 0
        self.total_cost_usd = 0.0

    def generate(
        self,
        user_prompt: str,
        system_prompt: str = "",
    ) -> tuple[str, int]:

        from google.genai import types

        request_config = types.GenerateContentConfig(
            system_instruction=system_prompt or None,
            temperature=baselines_config.TEMPERATURE,
            max_output_tokens=baselines_config.MAX_OUTPUT_TOKENS,
        )

        response = self._call_with_retry(
            user_prompt,
            request_config,
        )

        usage = response.usage_metadata

        prompt_tokens = (
            usage.prompt_token_count or 0
        )

        candidate_tokens = (
            usage.candidates_token_count or 0
        )

        thoughts = (
            getattr(
                usage,
                "thoughts_token_count",
                None,
            )
            or 0
        )

        total = (
            usage.total_token_count
            or (
                prompt_tokens
                + candidate_tokens
                + thoughts
            )
        )

        self.last_call_cost_usd = (
            (prompt_tokens / 1_000_000 * baselines_config.PRICE_PER_1M_INPUT_USD)
            + ((candidate_tokens + thoughts) / 1_000_000 * baselines_config.PRICE_PER_1M_OUTPUT_USD)
        )
        self.num_calls += 1
        self.total_tokens_used += total
        self.total_cost_usd += self.last_call_cost_usd

        text = (response.text or "").strip()

        if text.startswith("```"):
            text = re.sub(
                r"^```[a-zA-Z]*\n?",
                "",
                text,
            )
            text = re.sub(
                r"\n?```$",
                "",
                text,
            )

        return text, total

    def _call_with_retry(self, user_prompt: str, request_config):
        last_error: Exception | None = None
        for attempt in range(baselines_config.MAX_RETRIES + 1):
            try:
                return self._client.models.generate_content(
                    model=self.model, contents=user_prompt, config=request_config
                )
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                message = str(exc)
                kind = "rate_limit" if ("429" in message or "RESOURCE_EXHAUSTED" in message) else None
                if kind is None:
                    raise RuntimeError(
                        f"Gemini refinement request failed. model={self.model}; "
                        f"prompt_chars={len(user_prompt):,}; "
                        f"prompt_tokens_est={_estimate_tokens_for_diagnostics(user_prompt):,}; "
                        f"attempt={attempt + 1}; error_type={type(exc).__name__}; "
                        f"error={message[:2000]}"
                    ) from exc
                if attempt == baselines_config.MAX_RETRIES:
                    break
                delay = _retry_delay_seconds(message)
                print(f"    [gemini] rate limited, waiting {delay:.0f}s (attempt {attempt + 1}/{baselines_config.MAX_RETRIES})")
                time.sleep(delay)
        raise RuntimeError(
            f"Gemini refinement retries exhausted. model={self.model}; "
            f"prompt_chars={len(user_prompt):,}; error={str(last_error)[:2000]}"
        ) from last_error


# ---------------------------------------------------------------------------
# Groq (OpenAI-compatible)
# ---------------------------------------------------------------------------

GROQ_API_KEY_ENV = "GROQ_API_KEY"

GROQ_BASE_URL = (
    "https://api.groq.com/openai/v1/chat/completions"
)

GROQ_MODEL_ID = os.getenv(
    "GROQ_MODEL_ID",
    "llama-3.1-8b-instant",
)

GROQ_PRICE_PER_1M_INPUT_USD = float(
    os.getenv(
        "GROQ_PRICE_IN",
        "0.05",
    )
)

GROQ_PRICE_PER_1M_OUTPUT_USD = float(
    os.getenv(
        "GROQ_PRICE_OUT",
        "0.08",
    )
)

# Separate budgets are important because the initial seed request and
# subsequent refinement requests have different purposes.
#
# The previous implementation reused baselines_config.MAX_OUTPUT_TOKENS
# (8192 in the current baseline configuration). The Groq seed request was
# rejected with HTTP 413, so the default Groq output budget is deliberately
# reduced while remaining configurable through environment variables.
GROQ_SEED_MAX_OUTPUT_TOKENS = int(
    os.getenv(
        "GROQ_SEED_MAX_OUTPUT_TOKENS",
        "4096",
    )
)

GROQ_REFINEMENT_MAX_OUTPUT_TOKENS = int(
    os.getenv(
        "GROQ_REFINEMENT_MAX_OUTPUT_TOKENS",
        "4096",
    )
)

# A 429 Retry-After can otherwise block a Colab session for tens of minutes.
GROQ_MAX_RETRY_WAIT_SECONDS = float(
    os.getenv(
        "GROQ_MAX_RETRY_WAIT_SECONDS",
        "120",
    )
)


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
    """
    POST to Groq's chat/completions endpoint.

    Returns:
        (content, prompt_tokens, completion_tokens, total_tokens)

    The actual usage values returned by Groq are used for the experimental
    token/cost metrics. The diagnostic token estimate is never used for
    billing or reported results.
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

    combined_input = "\n".join(
        str(message.get("content", ""))
        for message in messages
    )

    print(
        "    [groq] request diagnostics: "
        f"model={model}, "
        f"input_chars={len(combined_input):,}, "
        f"estimated_input_tokens="
        f"{_estimate_tokens_for_diagnostics(combined_input):,}, "
        f"max_output_tokens={max_tokens:,}"
    )

    last_error: Exception | None = None

    for attempt in range(max_retries + 1):

        request = urllib.request.Request(
            GROQ_BASE_URL,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/124.0.0.0 "
                    "Safari/537.36"
                ),
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=120,
            ) as response:

                payload = json.loads(
                    response.read().decode(
                        "utf-8"
                    )
                )

            content = (
                payload["choices"][0]["message"]["content"]
                or ""
            )

            usage = payload.get(
                "usage",
                {},
            )

            prompt_tokens = usage.get(
                "prompt_tokens",
                0,
            )

            completion_tokens = usage.get(
                "completion_tokens",
                0,
            )

            total_tokens = usage.get(
                "total_tokens",
                prompt_tokens + completion_tokens,
            )

            return (
                content,
                prompt_tokens,
                completion_tokens,
                total_tokens,
            )

        except urllib.error.HTTPError as exc:

            error_body = exc.read().decode(
                "utf-8",
                errors="replace",
            )

            # 413 is a request-size error. Do not retry it.
            if exc.code == 413:
                raise RuntimeError(
                    "Groq API error 413: Request too large. "
                    f"model={model}, "
                    f"input_chars={len(combined_input):,}, "
                    f"estimated_input_tokens="
                    f"{_estimate_tokens_for_diagnostics(combined_input):,}, "
                    f"max_output_tokens={max_tokens:,}. "
                    f"Response: {error_body[:600]}"
                ) from exc

            # All non-429 errors remain non-retryable.
            if exc.code != 429:
                raise RuntimeError(
                    f"Groq API error {exc.code}: "
                    f"{error_body[:400]}"
                ) from exc

            # ---------------------------------------------------------
            # 429 handling
            # ---------------------------------------------------------

            retry_after = exc.headers.get(
                "Retry-After"
            )

            remaining_requests = exc.headers.get(
                "x-ratelimit-remaining-requests",
                "?",
            )

            remaining_tokens = exc.headers.get(
                "x-ratelimit-remaining-tokens",
                "?",
            )

            reset_requests = exc.headers.get(
                "x-ratelimit-reset-requests",
                "?",
            )

            reset_tokens = exc.headers.get(
                "x-ratelimit-reset-tokens",
                "?",
            )

            detail = (
                f"Groq 429: {error_body[:200]} | "
                f"retry-after={retry_after or '?'}s, "
                f"remaining_requests={remaining_requests}, "
                f"remaining_tokens={remaining_tokens}, "
                f"reset_requests={reset_requests}, "
                f"reset_tokens={reset_tokens}"
            )

            last_error = RuntimeError(detail)

            if attempt == max_retries:
                break

            delay = (
                float(retry_after) + 2
                if retry_after
                else 30.0
            )

            max_wait = float(
                os.getenv(
                    "GROQ_MAX_RETRY_WAIT_SECONDS",
                    str(
                        GROQ_MAX_RETRY_WAIT_SECONDS
                    ),
                )
            )

            if delay > max_wait:
                raise RuntimeError(
                    f"{detail} | "
                    f"retry delay {delay:.0f}s exceeds "
                    "GROQ_MAX_RETRY_WAIT_SECONDS="
                    f"{max_wait:.0f}s; "
                    "aborting this run instead of "
                    "blocking the experiment."
                ) from exc

            print(
                "    [groq] rate limited, "
                f"waiting {delay:.0f}s "
                f"(attempt {attempt + 1}/"
                f"{max_retries})"
            )

            time.sleep(delay)

    raise last_error  # type: ignore[misc]


class GroqTextClient:
    """
    Implements interfaces.LLMClient with a live Groq call.

    This client is used for the refinement rounds after the initial
    Baseline-A-style seed suite has been generated.
    """

    def __init__(
        self,
        model: str | None = None,
    ) -> None:

        if not has_groq_key():
            raise RuntimeError(
                "GROQ_API_KEY not set. Put it in .env or the environment "
                "before running with --provider groq."
            )

        self.model = model or GROQ_MODEL_ID
        self.last_call_cost_usd = 0.0
        self.num_calls = 0
        self.total_tokens_used = 0
        self.total_cost_usd = 0.0

    def generate(
        self,
        user_prompt: str,
        system_prompt: str = "",
    ) -> tuple[str, int]:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        content, prompt_tok, completion_tok, total = _groq_chat(
            messages,
            temperature=baselines_config.TEMPERATURE,
            max_tokens=GROQ_REFINEMENT_MAX_OUTPUT_TOKENS,
            model=self.model,
        )

        self.last_call_cost_usd = groq_cost_usd(prompt_tok, completion_tok)
        self.num_calls += 1
        self.total_tokens_used += total
        self.total_cost_usd += self.last_call_cost_usd

        text = content.strip()

        if text.startswith("```"):
            text = re.sub(
                r"^```[a-zA-Z]*\n?",
                "",
                text,
            )
            text = re.sub(
                r"\n?```$",
                "",
                text,
            )

        return text, total


class GroqStructuredClient:
    """
    Duck-types baselines.llm_client.LLMClient.

    Used by Baseline A to generate the initial structured test suite.
    """

    def __init__(
        self,
        tracker=None,
        model: str | None = None,
    ) -> None:

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
            f"{system_prompt}\n\n"
            "Respond with ONLY a single JSON object matching "
            "this JSON Schema exactly -- no prose, "
            "no markdown fences:\n"
            f"{json.dumps(schema)}"
        )

        messages = [
            {
                "role": "system",
                "content": schema_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        last_error: Exception | None = None

        for attempt in range(2):

            content, prompt_tok, completion_tok, total = _groq_chat(
                messages,
                temperature=(
                    baselines_config.TEMPERATURE
                    if temperature is None
                    else temperature
                ),
                max_tokens=GROQ_SEED_MAX_OUTPUT_TOKENS,
                model=self.model,
                response_format={
                    "type": "json_object"
                },
            )

            cleaned = content.strip()

            if cleaned.startswith("```"):
                cleaned = re.sub(
                    r"^```[a-zA-Z]*\n?",
                    "",
                    cleaned,
                )
                cleaned = re.sub(
                    r"\n?```$",
                    "",
                    cleaned,
                )

            try:
                parsed = (
                    response_model.model_validate_json(
                        cleaned
                    )
                )

            except Exception as exc:  # noqa: BLE001
                last_error = exc

                messages.append(
                    {
                        "role": "assistant",
                        "content": content,
                    }
                )

                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "That was not valid JSON for the "
                            f"schema ({exc}). "
                            "Return ONLY the corrected JSON object."
                        ),
                    }
                )

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
            f"[{label}] Groq response never validated "
            "against "
            f"{response_model.__name__}: "
            f"{last_error}"
        )


def groq_cost_usd(
    input_tokens: int,
    output_tokens: int,
) -> float:
    """
    List-price equivalent for Groq calls.

    UsageTracker prices against baselines.config's provider pricing,
    so Groq calls must be priced separately here.
    """

    return (
        input_tokens
        / 1_000_000
        * GROQ_PRICE_PER_1M_INPUT_USD
        + output_tokens
        / 1_000_000
        * GROQ_PRICE_PER_1M_OUTPUT_USD
    )


# ---------------------------------------------------------------------------
# Note on evaluation/ (Member 2)
# ---------------------------------------------------------------------------
#
# evaluation/evaluator.py currently has an invalid import:
#
#     from evaluation.coverage_runner.py import run_coverage
#
# and separately, run_mutation()/run_coverage() return raw subprocess stdout
# rather than the structured MutationResult this loop (or the shared log
# schema) needs.
#
# That is Member 2's fix to make, not something this adapter should route
# around by re-implementing their ownership area.
