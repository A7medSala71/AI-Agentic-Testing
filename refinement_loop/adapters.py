"""Adapters connecting the refinement loop to the shared evaluation pipeline and LLM providers.

The refinement loop itself stays provider/tool agnostic.  This module is the
single integration boundary for:
  * Member 2's shared mutmut + coverage.py evaluation code;
  * Member 3's structured Baseline-A seed generation;
  * Gemini or Groq live generation for refinement rounds.

No second mutation implementation is maintained here.
"""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

from baselines import config as baselines_config
from baselines.llm_client import _retry_delay_seconds
from evaluation.coverage_runner import run_coverage
from evaluation.mutation_runner import prepare_mutmut, run_mutation

from .models import MutationResult, SurvivingMutant

GROQ_API_KEY_ENV = "GROQ_API_KEY"
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL_ID = os.getenv("GROQ_MODEL_ID", "llama-3.3-70b-versatile")
GROQ_PRICE_PER_1M_INPUT_USD = float(os.getenv("GROQ_PRICE_IN", "0.59"))
GROQ_PRICE_PER_1M_OUTPUT_USD = float(os.getenv("GROQ_PRICE_OUT", "0.79"))

_OPERATOR_GROUPS = [
    ("LogicalOperator", {"and", "or", "not"}),
    ("ComparisonOperator", {"==", "!=", "is", "is not"}),
    ("ConditionalBoundary", {"<", "<=", ">", ">="}),
    ("ArithmeticOperator", {"+", "-", "*", "/", "//", "%", "**"}),
]

_TEST_DEF_RE = re.compile(r"^\s*def\s+(test_\w+)\s*\(", re.MULTILINE)
_ASSERT_RE = re.compile(r"^\s*assert .+$", re.MULTILINE)


def _classify_operator(original_line: str, mutated_line: str) -> str:
    orig = set(re.findall(r"[A-Za-z]+|[+\-*/%<>=!]+", original_line))
    mut = set(re.findall(r"[A-Za-z]+|[+\-*/%<>=!]+", mutated_line))
    changed = orig.symmetric_difference(mut)
    for label, ops in _OPERATOR_GROUPS:
        if changed & ops:
            return label
    return "Unknown"


def _parse_diff(text: str) -> tuple[int, str | None, str | None]:
    line_no = 0
    captured_at = 0
    original = mutated = None
    for line in text.splitlines():
        hunk = re.match(r"^@@ -(\d+),\d+ \+\d+,\d+ @@", line)
        if hunk:
            line_no = int(hunk.group(1))
            continue
        if not line_no:
            continue
        if line.startswith("-") and not line.startswith("---"):
            if original is None:
                original = line[1:]
                captured_at = line_no
            line_no += 1
        elif line.startswith("+") and not line.startswith("+++"):
            if mutated is None:
                mutated = line[1:]
        elif line.startswith(" "):
            line_no += 1
        if original is not None and mutated is not None:
            return captured_at, original, mutated
    return captured_at or line_no, original, mutated


class MutmutMutationRunner:
    """MutationRunner backed by Member 2's shared evaluation functions."""

    def __init__(self, function_id: str) -> None:
        self.function_id = function_id

    def run(self, function_source: str, test_code: str) -> MutationResult:
        import shutil
        import subprocess
        import sys
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            (workdir / "tests").mkdir()
            (workdir / f"{self.function_id}.py").write_text(function_source, encoding="utf-8")
            (workdir / "tests" / f"test_{self.function_id}.py").write_text(test_code, encoding="utf-8")
            prepare_mutmut(workdir, self.function_id)

            coverage = run_coverage(workdir, self.function_id)
            mutation = run_mutation(workdir, self.function_id)

            meta_path = workdir / "mutants" / f"{self.function_id}.py.meta"
            survivors: list[SurvivingMutant] = []
            if meta_path.exists():
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                for key, code in meta.get("exit_code_by_key", {}).items():
                    if code != 0:
                        continue
                    shown = subprocess.run(
                        [sys.executable, "-m", "mutmut", "show", key],
                        cwd=workdir, capture_output=True, text=True, timeout=60,
                    )
                    line_no, original, mutated = _parse_diff(shown.stdout)
                    if original is None or mutated is None:
                        continue
                    survivors.append(
                        SurvivingMutant(
                            mutant_id=str(key),
                            mutant_operator=_classify_operator(original, mutated),
                            line_number=line_no,
                            original_line=original,
                            mutated_line=mutated,
                            # mutmut exposes mutant survival, not assertion-level
                            # provenance. These are deliberately labelled as
                            # candidate assertions rather than fabricated failures.
                            failing_assertions=_ASSERT_RE.findall(test_code)[:3],
                            covering_test_names=_TEST_DEF_RE.findall(test_code),
                        )
                    )

        return MutationResult(
            total_mutants=mutation["mutants_total"],
            killed_mutants=mutation["mutants_killed"],
            survivors=survivors,
            line_coverage_pct=coverage["line_coverage_pct"],
            tests_collected=coverage["tests_collected"],
            tests_passed=coverage["tests_passed"],
        )


class GeminiTextClient:
    def __init__(self, model: str | None = None) -> None:
        from google import genai
        api_key = baselines_config.api_key()
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set.")
        self.model = model or baselines_config.MODEL_ID
        self._client = genai.Client(api_key=api_key)

    def generate(self, user_prompt: str, system_prompt: str = "") -> tuple[str, int]:
        from google.genai import types
        cfg = types.GenerateContentConfig(
            system_instruction=system_prompt or None,
            temperature=baselines_config.TEMPERATURE,
            max_output_tokens=baselines_config.MAX_OUTPUT_TOKENS,
        )
        response = self._call_with_retry(user_prompt, cfg)
        usage = response.usage_metadata
        thoughts = getattr(usage, "thoughts_token_count", None) or 0
        prompt = getattr(usage, "prompt_token_count", None) or 0
        output = getattr(usage, "candidates_token_count", None) or 0
        total = getattr(usage, "total_token_count", None) or (prompt + output + thoughts)
        return _clean_code(response.text or ""), total

    def _call_with_retry(self, user_prompt, cfg):
        last = None
        for attempt in range(baselines_config.MAX_RETRIES + 1):
            try:
                return self._client.models.generate_content(
                    model=self.model, contents=user_prompt, config=cfg
                )
            except Exception as exc:
                msg = str(exc)
                if "429" not in msg and "RESOURCE_EXHAUSTED" not in msg:
                    raise
                last = exc
                if attempt == baselines_config.MAX_RETRIES:
                    break
                delay = _retry_delay_seconds(msg)
                print(f"    [refinement] rate limited; waiting {delay:.0f}s")
                time.sleep(delay)
        raise last


def groq_api_key() -> str | None:
    return os.getenv(GROQ_API_KEY_ENV) or None


def has_groq_key() -> bool:
    return bool(groq_api_key())


def _groq_chat(messages, *, temperature, max_tokens, model, response_format=None, max_retries=3):
    import urllib.error
    import urllib.request
    api_key = groq_api_key()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set.")
    body = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if response_format:
        body["response_format"] = response_format
    last = None
    for attempt in range(max_retries + 1):
        req = urllib.request.Request(
            GROQ_BASE_URL,
            data=json.dumps(body).encode(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                payload = json.loads(resp.read().decode())
            msg = payload["choices"][0]["message"]
            content = msg.get("content") or ""
            usage = payload.get("usage", {})
            p = usage.get("prompt_tokens", 0)
            o = usage.get("completion_tokens", 0)
            return content, p, o, usage.get("total_tokens", p + o)
        except urllib.error.HTTPError as exc:
            body_text = exc.read().decode("utf-8", errors="replace")
            if exc.code != 429:
                raise RuntimeError(f"Groq API error {exc.code}: {body_text[:500]}") from exc
            last = RuntimeError(f"Groq 429: {body_text[:300]}")
            if attempt == max_retries:
                break
            retry_after = exc.headers.get("Retry-After")
            delay = float(retry_after) + 2 if retry_after else 30.0
            print(f"    [groq] rate limited; waiting {delay:.0f}s")
            time.sleep(delay)
    raise last


class GroqTextClient:
    def __init__(self, model: str | None = None) -> None:
        if not has_groq_key():
            raise RuntimeError("GROQ_API_KEY is not set.")
        self.model = model or GROQ_MODEL_ID
        self.input_tokens = self.output_tokens = self.total_tokens = self.num_calls = 0

    def generate(self, user_prompt: str, system_prompt: str = "") -> tuple[str, int]:
        messages = ([{"role": "system", "content": system_prompt}] if system_prompt else [])
        messages.append({"role": "user", "content": user_prompt})
        content, p, o, total = _groq_chat(
            messages, temperature=baselines_config.TEMPERATURE,
            max_tokens=baselines_config.MAX_OUTPUT_TOKENS, model=self.model
        )
        self.input_tokens += p
        self.output_tokens += o
        self.total_tokens += total
        self.num_calls += 1
        return _clean_code(content), total


class GroqStructuredClient:
    def __init__(self, tracker=None, model: str | None = None) -> None:
        from baselines.llm_client import UsageTracker
        if not has_groq_key():
            raise RuntimeError("GROQ_API_KEY is not set.")
        self.tracker = tracker or UsageTracker()
        self.model = model or GROQ_MODEL_ID

    def generate(self, *, system_prompt, user_prompt, response_model, label, temperature=None):
        from baselines.llm_client import CallRecord
        schema_prompt = (
            f"{system_prompt}\n\nReturn ONLY one JSON object matching this schema:\n"
            f"{json.dumps(response_model.model_json_schema())}"
        )
        messages = [{"role": "system", "content": schema_prompt}, {"role": "user", "content": user_prompt}]
        last = None
        for _ in range(2):
            content, p, o, total = _groq_chat(
                messages,
                temperature=baselines_config.TEMPERATURE if temperature is None else temperature,
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
                self.tracker.add(CallRecord(label=label, input_tokens=p, output_tokens=o,
                    thought_tokens=0, total_tokens=total, model=self.model))
                return parsed
            except Exception as exc:
                last = exc
                messages += [{"role": "assistant", "content": content},
                             {"role": "user", "content": f"Invalid JSON: {exc}. Return corrected JSON only."}]
        raise RuntimeError(f"{label}: structured output validation failed: {last}")


def groq_cost_usd(input_tokens: int, output_tokens: int) -> float:
    return input_tokens / 1_000_000 * GROQ_PRICE_PER_1M_INPUT_USD + output_tokens / 1_000_000 * GROQ_PRICE_PER_1M_OUTPUT_USD


def _clean_code(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return text.strip()
