"""LLM client with per-call usage accounting (Member 3).

Why this file exists at all, rather than calling the SDK directly from the
baselines: brief section 3.5 requires reporting "Calls / cost per file", and
RQ1 only holds if Baseline A, Baseline B and the proposed variants are
compared at a comparable budget. Baseline B spends 5 calls per function where
Baseline A spends 1. If that is not recorded at the moment each call is made,
it cannot be reconstructed afterwards, and the Week 4 full-scale runs would
have to be repeated to recover it.

Every call therefore goes through `LLMClient.generate`, which returns the
parsed object and folds the token counts into a `UsageTracker`.

Runs without an API key in mock mode, so the whole pipeline is testable now.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import TypeVar

from pydantic import BaseModel

from . import config

T = TypeVar("T", bound=BaseModel)


@dataclass
class CallRecord:
    """Accounting for one LLM call."""

    label: str
    input_tokens: int
    output_tokens: int
    thought_tokens: int
    total_tokens: int
    model: str
    mocked: bool = False


@dataclass
class UsageTracker:
    """Accumulates usage across the calls that make up one function's run."""

    records: list[CallRecord] = field(default_factory=list)

    def add(self, record: CallRecord) -> None:
        self.records.append(record)

    @property
    def num_calls(self) -> int:
        return len(self.records)

    @property
    def input_tokens(self) -> int:
        return sum(r.input_tokens for r in self.records)

    @property
    def output_tokens(self) -> int:
        return sum(r.output_tokens for r in self.records)

    @property
    def thought_tokens(self) -> int:
        return sum(r.thought_tokens for r in self.records)

    @property
    def total_tokens(self) -> int:
        return sum(r.total_tokens for r in self.records)

    @property
    def estimated_cost_usd(self) -> float:
        """List-price equivalent. Reasoning tokens bill at the output rate."""
        billed_output = self.output_tokens + self.thought_tokens
        return (
            self.input_tokens / 1_000_000 * config.PRICE_PER_1M_INPUT_USD
            + billed_output / 1_000_000 * config.PRICE_PER_1M_OUTPUT_USD
        )

    def summary(self) -> dict:
        return {
            "num_llm_calls": self.num_calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "thought_tokens": self.thought_tokens,
            "total_tokens_used": self.total_tokens,
            "estimated_cost_usd": round(self.estimated_cost_usd, 6),
        }


class LLMClient:
    """Thin wrapper over google-genai that enforces structured output."""

    def __init__(
        self,
        tracker: UsageTracker | None = None,
        model: str | None = None,
        force_mock: bool = False,
    ):
        """`force_mock` keeps a check deterministic and free even when a key is
        present -- used by smoke_test, which verifies plumbing rather than
        model behaviour and should not consume the daily quota."""
        self.tracker = tracker or UsageTracker()
        self.model = model or config.MODEL_ID
        self._client = None
        self.mocked = force_mock or not config.has_api_key()
        if not self.mocked:
            from google import genai

            self._client = genai.Client(api_key=config.api_key())

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
        label: str,
        temperature: float | None = None,
    ) -> T:
        """Run one call and return an instance of `response_model`.

        The response is schema-constrained, so the return value is already a
        validated object -- there is no prose to strip and no fenced block to
        find.
        """
        if self.mocked:
            return self._mock(response_model, label)

        from google.genai import types

        request_config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=response_model,
            temperature=config.TEMPERATURE if temperature is None else temperature,
            max_output_tokens=config.MAX_OUTPUT_TOKENS,
        )
        response = self._call_with_retry(user_prompt, request_config, label)

        usage = response.usage_metadata
        # Gemini 3.x models emit reasoning tokens. They are billed and they
        # count against the budget, so leaving them out would understate cost.
        thoughts = getattr(usage, "thoughts_token_count", None) or 0
        prompt_tokens = usage.prompt_token_count or 0
        candidate_tokens = usage.candidates_token_count or 0
        total = usage.total_token_count or (
            prompt_tokens + candidate_tokens + thoughts
        )

        self.tracker.add(
            CallRecord(
                label=label,
                input_tokens=prompt_tokens,
                output_tokens=candidate_tokens,
                thought_tokens=thoughts,
                total_tokens=total,
                model=self.model,
            )
        )

        parsed = response.parsed
        if parsed is None:
            raise RuntimeError(
                f"[{label}] model returned no schema-valid object. "
                f"Raw: {getattr(response, 'text', '')[:400]}"
            )
        return parsed

    # --- rate limiting -----------------------------------------------------

    def _call_with_retry(self, user_prompt: str, request_config, label: str):
        """Issue the request, honouring the server's own retry hint on a 429.

        Baseline B fires 5 calls back to back per function, and a full-scale
        run is hundreds in sequence, so rate limits are hit routinely rather
        than exceptionally -- on paid tiers too, which have their own
        per-minute caps. A 429 response carries a `retryDelay` telling us
        exactly how long to wait; honouring it beats a fixed backoff guess.

        A daily-quota 429 is not recoverable by waiting, so retries are capped
        and the error is re-raised rather than looped on indefinitely.
        """
        last_error: Exception | None = None

        for attempt in range(config.MAX_RETRIES + 1):
            try:
                return self._client.models.generate_content(
                    model=self.model,
                    contents=user_prompt,
                    config=request_config,
                )
            except Exception as exc:  # noqa: BLE001 - inspected, then re-raised
                message = str(exc)
                if "429" not in message and "RESOURCE_EXHAUSTED" not in message:
                    raise
                last_error = exc
                if attempt == config.MAX_RETRIES:
                    break
                delay = _retry_delay_seconds(message)
                print(
                    f"    [{label}] rate limited, waiting {delay:.0f}s "
                    f"(attempt {attempt + 1}/{config.MAX_RETRIES})"
                )
                time.sleep(delay)

        raise last_error  # type: ignore[misc]

    # --- mock mode ---------------------------------------------------------

    def _mock(self, response_model: type[T], label: str) -> T:
        """Return a schema-valid stub so the pipeline is runnable without a key."""
        payload = _MOCKS.get(response_model.__name__)
        if payload is None:
            raise NotImplementedError(
                f"No mock registered for {response_model.__name__}"
            )
        obj = response_model.model_validate(payload)
        encoded = len(json.dumps(payload))
        self.tracker.add(
            CallRecord(
                label=label,
                input_tokens=100,
                output_tokens=encoded // 4,
                thought_tokens=0,
                total_tokens=100 + encoded // 4,
                model=f"{self.model} (mock)",
                mocked=True,
            )
        )
        return obj


def _retry_delay_seconds(error_message: str) -> float:
    """Pull the server's suggested wait out of a 429 body.

    The error carries `'retryDelay': '42s'` (and a float in the human-readable
    text). Falling back to a fixed delay when neither is present.
    """
    match = re.search(r"'retryDelay':\s*'(\d+(?:\.\d+)?)s'", error_message)
    if not match:
        match = re.search(r"retry in (\d+(?:\.\d+)?)s", error_message)
    if match:
        # A small margin, since the server's clock and ours are not the same.
        return min(float(match.group(1)) + 2, config.MAX_RETRY_DELAY_SECONDS)
    return min(30.0, config.MAX_RETRY_DELAY_SECONDS)


_MOCKS: dict[str, dict] = {
    "GeneratedTestSuite": {
        "module_under_test": "function_03",
        "imports": ["import pytest", "from function_03 import arc_length"],
        "tests": [
            {
                "test_name": "test_arc_length_quarter_circle",
                "test_code": (
                    "def test_arc_length_quarter_circle():\n"
                    "    assert arc_length(90, 10) == pytest.approx(15.707963267948966)"
                ),
                "rationale": "Nominal case: a quarter of the circumference.",
            },
            {
                "test_name": "test_arc_length_zero_angle",
                "test_code": (
                    "def test_arc_length_zero_angle():\n"
                    "    assert arc_length(0, 10) == 0"
                ),
                "rationale": "Boundary: a zero angle has zero arc length.",
            },
        ],
    },
    "PanelReview": {
        "judgements": [
            {
                "test_name": "test_arc_length_quarter_circle",
                "oracle_correct": True,
                "reason": "2*pi*10*(90/360) is 15.70796..., and approx handles float error.",
                "confidence": 0.95,
                "suggested_fix": None,
            },
            {
                "test_name": "test_arc_length_zero_angle",
                "oracle_correct": True,
                "reason": "The angle ratio is zero, so the product is zero exactly.",
                "confidence": 0.9,
                "suggested_fix": None,
            },
        ],
        "missing_cases": ["Negative angle", "Zero radius"],
    },
}
