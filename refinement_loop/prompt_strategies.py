"""
Surviving-mutant -> regeneration-prompt mapping.

This is the Week 2 deliverable: the design of how a list of `SurvivingMutant`
objects becomes the text sent back to the LLM for the next refinement round.

Two strategies are implemented, matching the two `system_variant` values in
execution_log_schema.json:

  Variant_1_ErrorTrace
      Straight from brief Section 3.3 "Feedback content": for each surviving
      mutant, give the mutated line, the original line, and the specific
      assertion(s) that failed to catch it. Cheap, deterministic, one LLM
      call per iteration.

  Variant_2_StatePrediction
      Inspired by LogicHunter (brief 1.4) — instead of only describing the
      diff, the prompt first asks the model to reason about the *runtime
      state divergence* the mutation causes (what value changes, at what
      point, and how it propagates) before writing a test that asserts on
      that divergence. This targets RQ2 specifically: weak-oracle tests
      that pass despite covering the mutant. `predicted_state` on the
      mutant is filled in by parsing that reasoning out of the model's
      response (left to Member 4's Week 3 implementation) and is carried
      into the log for analysis.

Both strategies share a `PromptStrategy` interface so `RefinementLoop` never
needs to know which variant it's running.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .config import VARIANT_ERROR_TRACE, VARIANT_STATE_PREDICTION, RefinementConfig
from .models import SurvivingMutant

_SHARED_SYSTEM_PROMPT = """\
You are refining a pytest test suite for a single Python function so that it \
kills surviving mutation-testing mutants. You will be given:
  1. the function's source code,
  2. the current test suite (which already passes on the ORIGINAL code),
  3. a list of mutants that survived (the tests still pass on the MUTATED code).

For each surviving mutant, add or modify tests so the suite fails on the \
mutated code while still passing on the original code. Do not remove or \
weaken any existing assertions that are working. Respond with ONLY the \
complete, updated pytest test file — no prose, no markdown fences."""


class PromptStrategy(ABC):
    """Base class: turns (source, tests, survivors) into an LLM prompt pair."""

    variant_name: str

    @abstractmethod
    def build(
        self,
        function_source: str,
        function_name: str,
        current_test_code: str,
        survivors: list[SurvivingMutant],
        config: RefinementConfig,
    ) -> tuple[str, str]:
        """Returns (system_prompt, user_prompt)."""
        raise NotImplementedError

    @staticmethod
    def _select_targets(
        survivors: list[SurvivingMutant], config: RefinementConfig
    ) -> list[SurvivingMutant]:
        """
        Cap how many mutants go into a single prompt.

        Prioritize operator diversity first (so one round doesn't spend its
        whole budget on ten near-duplicate boundary mutants on the same
        line), then fill remaining slots in survival order. This directly
        feeds RQ4 (does the loop help some operator classes more than
        others) by making sure early rounds sample across operator types
        rather than exhausting one type before ever seeing another.
        """
        if len(survivors) <= config.max_mutants_per_prompt:
            return survivors

        by_operator: dict[str, list[SurvivingMutant]] = {}
        for m in survivors:
            by_operator.setdefault(m.mutant_operator, []).append(m)

        selected: list[SurvivingMutant] = []
        operators = list(by_operator.keys())
        i = 0
        while len(selected) < config.max_mutants_per_prompt and any(
            by_operator[op] for op in operators
        ):
            op = operators[i % len(operators)]
            if by_operator[op]:
                selected.append(by_operator[op].pop(0))
            i += 1
        return selected


class ErrorTraceStrategy(PromptStrategy):
    """Variant_1_ErrorTrace: mutated line + original line + failing assertions."""

    variant_name = VARIANT_ERROR_TRACE

    def build(
        self,
        function_source: str,
        function_name: str,
        current_test_code: str,
        survivors: list[SurvivingMutant],
        config: RefinementConfig,
    ) -> tuple[str, str]:
        targets = self._select_targets(survivors, config)
        blocks = [self._mutant_block(m, config) for m in targets]

        user_prompt = f"""\
Function under test: `{function_name}`

--- function source ---
{function_source}

--- current test suite ---
{current_test_code}

--- surviving mutants ({len(targets)} of {len(survivors)} total) ---
{chr(10).join(blocks)}

Update the test suite so each surviving mutant above is killed."""
        return _SHARED_SYSTEM_PROMPT, user_prompt

    @staticmethod
    def _mutant_block(m: SurvivingMutant, config: RefinementConfig) -> str:
        assertions = m.failing_assertions[: config.max_assertions_per_mutant]
        assertions_txt = (
            "\n".join(f"    - {a}" for a in assertions)
            if assertions
            else "    - (exact assertion-level attribution is unavailable from this mutation runner; target the mutated line directly)"
        )
        return f"""Mutant {m.mutant_id} ({m.mutant_operator}) at line {m.line_number}:
  original: {m.original_line.strip()}
  mutated:  {m.mutated_line.strip()}
  assertions that ran but did not catch it:
{assertions_txt}
"""


class StatePredictionStrategy(PromptStrategy):
    """
    Variant_2_StatePrediction: same diff context as Variant_1, plus an explicit
    reasoning step asking the model to predict the runtime state divergence
    before writing the assertion.
    """

    variant_name = VARIANT_STATE_PREDICTION

    def build(
        self,
        function_source: str,
        function_name: str,
        current_test_code: str,
        survivors: list[SurvivingMutant],
        config: RefinementConfig,
    ) -> tuple[str, str]:
        targets = self._select_targets(survivors, config)
        blocks = [self._mutant_block(m, config) for m in targets]

        system_prompt = _SHARED_SYSTEM_PROMPT + """

Before writing each test, briefly reason (as a Python comment directly above \
the test) about how the mutation changes program state at that line and at \
return time — e.g. which variable's value diverges and what its mutated value \
is — then write an assertion that specifically targets that divergence \
rather than a generic input/output check. Keep the reasoning comment to one \
line per mutant."""

        user_prompt = f"""\
Function under test: `{function_name}`

--- function source ---
{function_source}

--- current test suite ---
{current_test_code}

--- surviving mutants ({len(targets)} of {len(survivors)} total) ---
{chr(10).join(blocks)}

For each mutant: predict the state divergence it causes, then update the \
test suite so the divergence is asserted on directly."""
        return system_prompt, user_prompt

    @staticmethod
    def _mutant_block(m: SurvivingMutant, config: RefinementConfig) -> str:
        assertions = m.failing_assertions[: config.max_assertions_per_mutant]
        assertions_txt = (
            "\n".join(f"    - {a}" for a in assertions)
            if assertions
            else "    - (exact assertion-level attribution is unavailable from this mutation runner; target the mutated line directly)"
        )
        prior_state = (
            f"\n  previously predicted state: {m.predicted_state}"
            if m.predicted_state
            else ""
        )
        return f"""Mutant {m.mutant_id} ({m.mutant_operator}) at line {m.line_number}:
  original: {m.original_line.strip()}
  mutated:  {m.mutated_line.strip()}
  assertions that ran but did not catch it:
{assertions_txt}{prior_state}
"""


_STRATEGIES: dict[str, type[PromptStrategy]] = {
    VARIANT_ERROR_TRACE: ErrorTraceStrategy,
    VARIANT_STATE_PREDICTION: StatePredictionStrategy,
}


def get_strategy(variant: str) -> PromptStrategy:
    """Factory: system_variant string (from config/schema) -> strategy instance."""
    try:
        return _STRATEGIES[variant]()
    except KeyError as exc:
        raise ValueError(
            f"No PromptStrategy registered for variant '{variant}'. "
            f"Known variants: {list(_STRATEGIES)}"
        ) from exc
