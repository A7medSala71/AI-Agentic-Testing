"""Structured-output schemas for Baseline A and Baseline B (Member 3).

These are the contracts the LLM is forced to fill in. Constraining generation
to a schema is what makes an unattended run of
30 functions x 3 systems x 3 repeats possible: no scraping code out of prose,
no markdown fences to strip, no half-parsed responses at 2am.

`ExecutionLog` mirrors schema/execution_log_schema.json (Member 1) so a run
can be validated against the team contract before it is written to logs/.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

SystemVariant = Literal[
    "Baseline_A",
    "Baseline_B",
    "Variant_1_ErrorTrace",
    "Variant_2_StatePrediction",
]


# --- LLM output contracts --------------------------------------------------


class TestCase(BaseModel):
    """A single generated pytest test function."""

    test_name: str = Field(description="pytest function name, must start with test_")
    test_code: str = Field(description="Complete source of the test function.")
    rationale: str = Field(description="What behaviour or edge case this targets.")


class GeneratedTestSuite(BaseModel):
    """Output of Baseline A, and of Baseline B's propose and finalise stages."""

    module_under_test: str = Field(description="Module imported, e.g. function_03")
    imports: list[str] = Field(description="Import lines the test file needs.")
    tests: list[TestCase]

    def to_source(self) -> str:
        """Render the suite as a runnable pytest file.

        Wildcard imports are rejected. `function_25.py` ships its own
        `class Test(unittest.TestCase)`; a `from function_25 import *` pulls it
        into the test module and pytest then collects its methods as if the
        model had written them -- 1 generated test becomes 3 collected tests,
        two of which came from the dataset. That silently corrupts the pass
        rate, so it is blocked here rather than left to prompt compliance.
        """
        seen: set[str] = set()
        lines: list[str] = []
        for imp in self.imports:
            stripped = imp.strip()
            if not stripped or stripped in seen:
                continue
            if stripped.endswith("*"):
                raise ValueError(
                    f"Wildcard import rejected for {self.module_under_test!r}: "
                    f"{stripped!r}. Use explicit named imports."
                )
            seen.add(stripped)
            lines.append(stripped)
        body = "\n\n\n".join(t.test_code.strip() for t in self.tests)
        return "\n".join(lines) + "\n\n\n" + body + "\n"


class OracleJudgement(BaseModel):
    """One panelist's verdict on one proposed test's assertion.

    CANDOR used a separate "Interpreter" agent to compress a reasoning model's
    very long output into exactly these fields. Native structured output makes
    that second agent unnecessary, which is why Baseline B is 5 calls not 8.
    """

    test_name: str
    oracle_correct: bool = Field(
        description="True if the assertion matches the function's real behaviour."
    )
    reason: str = Field(description="One or two sentences. No restating the code.")
    confidence: float = Field(ge=0.0, le=1.0)
    suggested_fix: str | None = Field(
        default=None, description="Corrected assertion when oracle_correct is False."
    )


class PanelReview(BaseModel):
    """One panelist's full review of the proposed suite."""

    judgements: list[OracleJudgement]
    missing_cases: list[str] = Field(
        default_factory=list,
        description="Untested behaviours the panelist believes were missed.",
    )


# --- Team logging contract -------------------------------------------------


class IterationDetail(BaseModel):
    iteration: int
    mutant_id: str | None = None
    mutant_operator: str | None = None
    predicted_state: str | None = None
    generated_test_code: str
    mutant_killed: bool


class ExecutionLog(BaseModel):
    """Mirrors schema/execution_log_schema.json.

    Fields marked optional there stay optional here. `iterations_detail` is
    mutant-centric and is meant for Member 4's refinement variants; the
    baselines emit one whole suite scored against all mutants at once, so they
    leave it unset.
    """

    function_id: str
    system_variant: SystemVariant
    iteration_count: int = Field(ge=1, le=5)
    total_tokens_used: int
    mutation_score_pct: float
    estimated_cost_usd: float | None = None
    line_coverage_pct: float | None = None
    iterations_detail: list[IterationDetail] | None = None

    # --- Fields NOT in the team schema yet -------------------------------
    # Brief section 3.5 requires "Calls / cost per file -- Number of LLM calls
    # (and tokens)" and a pass rate, but the schema has slots for neither.
    # Baseline B makes 5 calls per function against Baseline A's 1, so RQ1's
    # cost-fairness claim cannot be made from tokens alone.
    # Requested from Member 1; emitted now so no run has to be repeated later.
    num_llm_calls: int | None = None
    pass_rate_pct: float | None = None
    branch_coverage_pct: float | None = None
