"""
Refinement loop configuration.

Values default to what's locked in the project brief (Section 3.3):
  - cap at 5 iterations per file
  - stop early if mutation score improves by less than 2 percentage points
    between rounds
"""

from __future__ import annotations

from dataclasses import dataclass

VARIANT_ERROR_TRACE = "Variant_1_ErrorTrace"
VARIANT_STATE_PREDICTION = "Variant_2_StatePrediction"

SUPPORTED_VARIANTS = (VARIANT_ERROR_TRACE, VARIANT_STATE_PREDICTION)


@dataclass(frozen=True)
class RefinementConfig:
    max_iterations: int = 5
    plateau_threshold_pp: float = 2.0          # percentage points
    variant: str = VARIANT_ERROR_TRACE
    max_mutants_per_prompt: int = 8            # cap feedback size / token budget
    max_assertions_per_mutant: int = 3         # trim noisy failing_assertions lists

    def __post_init__(self) -> None:
        if self.variant not in SUPPORTED_VARIANTS:
            raise ValueError(
                f"Unknown variant '{self.variant}'. Must be one of {SUPPORTED_VARIANTS}"
            )
        if self.max_iterations < 1:
            raise ValueError("max_iterations must be >= 1")
