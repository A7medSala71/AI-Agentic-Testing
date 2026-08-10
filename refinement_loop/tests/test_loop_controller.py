import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from refinement_loop import RefinementConfig, RefinementLoop, SurvivingMutant
from refinement_loop.models import MutationResult


class ScriptedMutationRunner:
    """Returns a pre-scripted sequence of MutationResults, one per call."""

    def __init__(self, results: list[MutationResult]) -> None:
        self._results = results
        self._i = 0

    def run(self, function_source: str, test_code: str) -> MutationResult:
        result = self._results[min(self._i, len(self._results) - 1)]
        self._i += 1
        return result


class StubLLMClient:
    def generate(self, user_prompt: str, system_prompt: str = "") -> tuple[str, int]:
        return "def test_stub(): pass", 100


def _mutant(mid: str) -> SurvivingMutant:
    return SurvivingMutant(mid, "Op", 1, "a", "b")


def test_invalid_regeneration_is_discarded_not_merged():
    """A round that returns prose/empty output (no `def test_`) must not
    overwrite the existing suite -- see RefinementConfig.discard_invalid_regeneration."""

    class ProseLLMClient:
        def generate(self, user_prompt: str, system_prompt: str = "") -> tuple[str, int]:
            return "I'm sorry, I can't help with that request.", 40

    results = [MutationResult(10, 8, [_mutant("m1")], 90.0)]
    loop = RefinementLoop(RefinementConfig(), ScriptedMutationRunner(results), ProseLLMClient())
    log = loop.run("fn", "def f(): ...", "f", "def test_f(): ...")

    assert log.iteration_count == 1
    assert log.iterations_detail[0].mutant_killed is False
    # score stays whatever the last real mutation run reported (80%), not
    # invented from the discarded round
    assert log.mutation_score_pct == 80.0


def test_loop_stops_when_no_survivors_remain():
    results = [
        MutationResult(10, 8, [_mutant("m1"), _mutant("m2")], 90.0),
        MutationResult(10, 10, [], 90.0),  # all killed after 1 round
    ]
    loop = RefinementLoop(RefinementConfig(), ScriptedMutationRunner(results), StubLLMClient())
    log = loop.run("fn", "def f(): ...", "f", "def test_f(): ...")

    assert log.iteration_count == 1
    assert log.mutation_score_pct == 100.0
    assert log.stop_reason == "no_survivors"


def test_loop_stops_on_plateau_below_threshold():
    # Each round only gains 1pp, below the default 2pp threshold -> stop after round 1.
    results = [
        MutationResult(100, 80, [_mutant("m1")], 90.0),
        MutationResult(100, 81, [_mutant("m1")], 90.0),
        MutationResult(100, 82, [_mutant("m1")], 90.0),
    ]
    loop = RefinementLoop(RefinementConfig(), ScriptedMutationRunner(results), StubLLMClient())
    log = loop.run("fn", "def f(): ...", "f", "def test_f(): ...")

    assert log.iteration_count == 1


def test_loop_respects_max_iterations_cap():
    # Big gains every round (never plateaus) but hits the 5-iteration cap.
    results = [MutationResult(100, 50, [_mutant("m1")], 90.0)] + [
        MutationResult(100, 50 + 10 * i, [_mutant("m1")], 90.0) for i in range(1, 7)
    ]
    loop = RefinementLoop(RefinementConfig(max_iterations=5), ScriptedMutationRunner(results), StubLLMClient())
    log = loop.run("fn", "def f(): ...", "f", "def test_f(): ...")

    assert log.iteration_count == 5


def test_initial_suite_success_reports_zero_refinement_rounds():
    results = [MutationResult(10, 10, [], 80.0, pass_rate_pct=100.0)]
    loop = RefinementLoop(RefinementConfig(), ScriptedMutationRunner(results), StubLLMClient())
    log = loop.run("fn", "def f(): ...", "f", "def test_f(): ...")
    assert log.iteration_count == 0
    assert log.num_llm_calls == 0
    assert log.stop_reason == "no_survivors"
    assert log.pass_rate_pct == 100.0


def test_invalid_python_regeneration_is_discarded():
    class BadLLM:
        def generate(self, user_prompt: str, system_prompt: str = "") -> tuple[str, int]:
            return "def test_broken(:", 20

    results = [MutationResult(10, 8, [_mutant("m1")], 90.0)]
    loop = RefinementLoop(RefinementConfig(), ScriptedMutationRunner(results), BadLLM())
    log = loop.run("fn", "def f(): ...", "f", "def test_f(): ...")
    assert log.stop_reason == "invalid_regeneration"
    assert log.mutation_score_pct == 80.0


def test_merge_preserves_dropped_existing_test():
    current = "from function_01 import f\n\ndef test_old():\n    assert f(1) == 1\n"
    generated = "from function_01 import f\n\ndef test_new():\n    assert f(2) == 2\n"
    merged = RefinementLoop._merge_tests(current, generated)
    assert "def test_old" in merged
    assert "def test_new" in merged
