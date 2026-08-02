"""
refinement_loop
================

Member 4's mutant-guided iterative refinement loop.

Public entry points:
    - RefinementLoop        : orchestrates generate -> mutate -> feedback -> regenerate
    - RefinementConfig       : stopping rule / budget knobs
    - get_strategy           : returns the correct prompt-building strategy for a
                                system_variant string from execution_log_schema.json
    - SurvivingMutant, MutationResult, RunLog, IterationRecord : shared data model
"""

from .config import RefinementConfig
from .models import IterationRecord, MutationResult, RunLog, SurvivingMutant
from .prompt_strategies import ErrorTraceStrategy, StatePredictionStrategy, get_strategy
from .loop_controller import RefinementLoop

__all__ = [
    "RefinementConfig",
    "SurvivingMutant",
    "MutationResult",
    "IterationRecord",
    "RunLog",
    "ErrorTraceStrategy",
    "StatePredictionStrategy",
    "get_strategy",
    "RefinementLoop",
]
