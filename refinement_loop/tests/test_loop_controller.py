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


def test_loop_stops_when_no_survivors_remain():
    results = [
        MutationResult(10, 8, [_mutant("m1"), _mutant("m2")], 90.0),
        MutationResult(10, 10, [], 90.0),  # all killed after 1 round
    ]
    loop = RefinementLoop(RefinementConfig(), ScriptedMutationRunner(results), StubLLMClient())
    log = loop.run("fn", "def f(): ...", "f", "def test_f(): ...")

    assert log.iteration_count == 1
    assert log.mutation_score_pct == 100.0


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
