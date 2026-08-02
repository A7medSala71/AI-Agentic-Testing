import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest

from refinement_loop.config import RefinementConfig
from refinement_loop.models import SurvivingMutant
from refinement_loop.prompt_strategies import (
    ErrorTraceStrategy,
    StatePredictionStrategy,
    get_strategy,
)

MUTANT = SurvivingMutant(
    mutant_id="m1",
    mutant_operator="ConditionalBoundary",
    line_number=10,
    original_line="if x < 4:",
    mutated_line="if x <= 4:",
    failing_assertions=["assert f(4) == True"],
)


def test_error_trace_prompt_includes_diff_and_assertions():
    strategy = ErrorTraceStrategy()
    config = RefinementConfig(variant="Variant_1_ErrorTrace")
    _, user_prompt = strategy.build("def f(x): ...", "f", "def test_f(): ...", [MUTANT], config)

    assert "if x < 4:" in user_prompt
    assert "if x <= 4:" in user_prompt
    assert "assert f(4) == True" in user_prompt
    assert "m1" in user_prompt


def test_state_prediction_prompt_asks_for_reasoning():
    strategy = StatePredictionStrategy()
    config = RefinementConfig(variant="Variant_2_StatePrediction")
    system_prompt, user_prompt = strategy.build(
        "def f(x): ...", "f", "def test_f(): ...", [MUTANT], config
    )

    assert "state" in system_prompt.lower() and "divergence" in system_prompt.lower()
    assert "predict" in user_prompt.lower()


def test_get_strategy_factory_routes_by_variant():
    assert isinstance(get_strategy("Variant_1_ErrorTrace"), ErrorTraceStrategy)
    assert isinstance(get_strategy("Variant_2_StatePrediction"), StatePredictionStrategy)
    with pytest.raises(ValueError):
        get_strategy("not_a_real_variant")


def test_select_targets_caps_and_diversifies_by_operator():
    survivors = [
        SurvivingMutant("a1", "OperatorA", 1, "x", "y"),
        SurvivingMutant("a2", "OperatorA", 2, "x", "y"),
        SurvivingMutant("a3", "OperatorA", 3, "x", "y"),
        SurvivingMutant("b1", "OperatorB", 4, "x", "y"),
        SurvivingMutant("c1", "OperatorC", 5, "x", "y"),
    ]
    config = RefinementConfig(max_mutants_per_prompt=3)
    selected = ErrorTraceStrategy._select_targets(survivors, config)

    assert len(selected) == 3
    operators = {m.mutant_operator for m in selected}
    # with only 3 slots and 3 distinct operator types, diversity-first
    # selection should pull from all three rather than exhausting OperatorA.
    assert operators == {"OperatorA", "OperatorB", "OperatorC"}


def test_invalid_variant_rejected_by_config():
    with pytest.raises(ValueError):
        RefinementConfig(variant="totally_made_up")
