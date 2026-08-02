"""
Integration boundary.

These Protocols are the *contract* the refinement loop depends on. Member 2's
mutation pipeline just needs to expose something matching `MutationRunner`;
whoever wires up the LLM API just needs something matching `LLMClient`. The
loop itself never imports mutmut, coverage.py, or an SDK directly, so it can
be unit-tested with fakes (see tests/) and swapped onto Member 2's real
pipeline without changing `loop_controller.py`.
"""

from __future__ import annotations

from typing import Protocol

from .models import MutationResult


class MutationRunner(Protocol):
    """Implemented by Member 2's mutation-testing pipeline."""

    def run(self, function_source: str, test_code: str) -> MutationResult:
        """
        Run mutation testing (mutmut, fallback cosmic-ray) for `function_source`
        against `test_code`, plus coverage.py for line coverage.

        Returns a MutationResult with the current surviving mutants. Must be
        deterministic given the same inputs (mutant set is fixed per function;
        only which mutants survive changes as test_code improves).
        """
        ...


class LLMClient(Protocol):
    """Implemented by whoever wires up the Anthropic (or other) API client."""

    def generate(self, user_prompt: str, system_prompt: str = "") -> tuple[str, int]:
        """
        Returns (generated_test_code, tokens_used).

        `tokens_used` should be prompt + completion tokens for this single
        call, so the loop can accumulate `total_tokens_used` for the
        cost-quality tradeoff (RQ3).
        """
        ...
