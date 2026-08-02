"""
Demo: wires RefinementLoop end-to-end using FAKE MutationRunner / LLMClient
implementations, so the architecture can be exercised and its log output
validated against execution_log_schema.json *before* Member 2's real mutmut
pipeline and a live LLM API are plugged in (Week 3 work).

Run:
    python examples/demo_run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from refinement_loop import RefinementConfig, RefinementLoop, SurvivingMutant
from refinement_loop.config import VARIANT_ERROR_TRACE, VARIANT_STATE_PREDICTION
from refinement_loop.logger import validate_run_log, write_run_log
from refinement_loop.models import MutationResult

FUNCTION_SOURCE = (REPO_ROOT / "dataset" / "function_25.py").read_text()

INITIAL_TEST_CODE = '''\
import pytest
from function_25 import is_prime

def test_is_prime_true_cases():
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(563)

def test_is_prime_false_cases():
    assert not is_prime(0)
    assert not is_prime(1)
    assert not is_prime(27)

def test_is_prime_invalid_input():
    with pytest.raises(ValueError):
        is_prime(-4)
'''


class FakeMutationRunner:
    """
    Simulates mutmut: starts with 3 surviving mutants (chosen to mirror
    plausible real ones for is_prime's boundary/arithmetic logic), then
    'kills' one mutant per refinement round to demonstrate the loop
    converging and the plateau rule firing.
    """

    def __init__(self) -> None:
        self._survivors = [
            SurvivingMutant(
                mutant_id="m1",
                mutant_operator="ConditionalBoundary",
                line_number=30,
                original_line="if 1 < number < 4:",
                mutated_line="if 1 <= number < 4:",
                failing_assertions=["assert is_prime(3)"],
                covering_test_names=["test_is_prime_true_cases"],
            ),
            SurvivingMutant(
                mutant_id="m2",
                mutant_operator="ArithmeticOperator",
                line_number=36,
                original_line="for i in range(5, int(math.sqrt(number) + 1), 6):",
                mutated_line="for i in range(5, int(math.sqrt(number) - 1), 6):",
                failing_assertions=["assert is_prime(563)"],
                covering_test_names=["test_is_prime_true_cases"],
            ),
            SurvivingMutant(
                mutant_id="m3",
                mutant_operator="ComparisonOperator",
                line_number=32,
                original_line="elif number < 2 or number % 2 == 0 or number % 3 == 0:",
                mutated_line="elif number <= 2 or number % 2 == 0 or number % 3 == 0:",
                failing_assertions=["assert not is_prime(0)", "assert not is_prime(1)"],
                covering_test_names=["test_is_prime_false_cases"],
            ),
        ]
        self._total_mutants = 12
        self._call_count = 0

    def run(self, function_source: str, test_code: str) -> MutationResult:
        self._call_count += 1
        # After the first regeneration, "kill" the oldest surviving mutant.
        if self._call_count > 1 and self._survivors:
            self._survivors.pop(0)
        killed = self._total_mutants - len(self._survivors)
        return MutationResult(
            total_mutants=self._total_mutants,
            killed_mutants=killed,
            survivors=list(self._survivors),
            line_coverage_pct=92.0,
        )


class FakeLLMClient:
    """Stand-in for the real Anthropic API call; echoes a plausible token count."""

    def generate(self, user_prompt: str, system_prompt: str = "") -> tuple[str, int]:
        generated = INITIAL_TEST_CODE + (
            "\ndef test_regenerated_case():\n    assert is_prime(2999)\n"
        )
        approx_tokens = (len(system_prompt) + len(user_prompt) + len(generated)) // 4
        return generated, approx_tokens


def run_variant(variant: str) -> None:
    print(f"\n=== Running {variant} ===")
    config = RefinementConfig(variant=variant)
    loop = RefinementLoop(
        config=config,
        mutation_runner=FakeMutationRunner(),
        llm_client=FakeLLMClient(),
    )
    run_log = loop.run(
        function_id="function_25",
        function_source=FUNCTION_SOURCE,
        function_name="is_prime",
        initial_test_code=INITIAL_TEST_CODE,
    )

    out_path = Path(__file__).parent / f"sample_log_{variant}.json"
    write_run_log(run_log, out_path)
    validate_run_log(run_log)

    print(f"iterations run:      {run_log.iteration_count}")
    print(f"final mutation score:{run_log.mutation_score_pct}%")
    print(f"tokens used:          {run_log.total_tokens_used}")
    print(f"log written to:       {out_path}")


if __name__ == "__main__":
    run_variant(VARIANT_ERROR_TRACE)
    run_variant(VARIANT_STATE_PREDICTION)
