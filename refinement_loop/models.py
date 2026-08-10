"""
Data model for the refinement loop.

These classes mirror the fields in `execution_log_schema.json` exactly, so that
`RunLog.to_dict()` can be dumped straight to JSON and validated against the
shared schema Member 1 owns. Keeping the model 1:1 with the schema avoids a
translation layer that could silently drift out of sync.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class SurvivingMutant:
    """
    One mutant that survived the test suite (i.e. tests still passed against
    the mutated code -> a "weak oracle" signal, per RQ2).

    This is the atomic unit of feedback: everything the regeneration prompt
    says about a mutant comes from this object.
    """

    mutant_id: str                     # stable id from mutmut, e.g. "7"
    mutant_operator: str                # e.g. "ConditionalBoundary", "ArithmeticOperator"
    line_number: int
    original_line: str                  # source line before mutation
    mutated_line: str                   # source line after mutation
    failing_assertions: list[str] = field(default_factory=list)
    # ^ assertions that ran against the mutant but did not fail (i.e. did not catch it)
    covering_test_names: list[str] = field(default_factory=list)
    # ^ which existing tests executed this line but failed to kill the mutant
    predicted_state: Optional[str] = None
    # ^ only populated by Variant_2 (StatePrediction); None for Variant_1 (ErrorTrace)


@dataclass
class MutationResult:
    """Output of one mutation-testing/evaluation pass.

    Member 2 owns the authoritative implementation. The optional coverage/pass-rate
    fields let that implementation expose the complete project metrics without
    forcing Member 4's loop to own scoring logic.
    """

    total_mutants: int
    killed_mutants: int
    survivors: list[SurvivingMutant]
    line_coverage_pct: float
    pass_rate_pct: float | None = None
    branch_coverage_pct: float | None = None

    @property
    def mutation_score_pct(self) -> float:
        if self.total_mutants == 0:
            return 100.0
        return round(100.0 * self.killed_mutants / self.total_mutants, 2)


@dataclass
class IterationRecord:
    """One row of `iterations_detail` in execution_log_schema.json."""

    iteration: int
    mutant_id: str
    generated_test_code: str
    mutant_killed: bool
    mutant_operator: Optional[str] = None
    predicted_state: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RunLog:
    """Top-level object matching execution_log_schema.json."""

    function_id: str
    system_variant: str                 # "Variant_1_ErrorTrace" | "Variant_2_StatePrediction"
    iteration_count: int
    total_tokens_used: int
    mutation_score_pct: float
    line_coverage_pct: float
    estimated_cost_usd: float = 0.0
    iterations_detail: list[IterationRecord] = field(default_factory=list)
    num_llm_calls: int | None = None
    pass_rate_pct: float | None = None
    branch_coverage_pct: float | None = None
    initial_mutation_score_pct: float | None = None
    stop_reason: str | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["iterations_detail"] = [r.to_dict() for r in self.iterations_detail]
        # Optional metrics are omitted rather than serialized as null so the
        # JSON remains compatible with the shared schema and older consumers.
        return {k: v for k, v in d.items() if v is not None}
