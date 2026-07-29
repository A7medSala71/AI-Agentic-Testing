"""Prompt templates for Baseline A and Baseline B (Member 3).

All prompts live here rather than inline so the exact wording can be quoted in
the paper and diffed when results change.

Three rules are shared by every prompt and are not stylistic preferences --
each was forced by something measured in Week 1:

1. **State the module name.** The model sees source, never a filename. Left to
   guess it invents one ('solution', 'arc_length_module') and every generated
   suite dies with ModuleNotFoundError. Measured: pass rate 0% -> 80% from this
   one line.
2. **Explicit named imports only.** `from function_25 import *` drags that
   file's own unittest class into the test module, and pytest then collects the
   dataset's tests as if the model had written them.
3. **pytest.approx for floats.** Most of this dataset returns floats; an exact
   == on a float is a flaky oracle that fails for reasons unrelated to the
   system under test.

Rules 1-3 apply to Baseline A, Baseline B and Member 4's variants alike. A
system that omits them scores badly for reasons that have nothing to do with
its design, which would silently invalidate RQ1.
"""

from __future__ import annotations

# --- shared -----------------------------------------------------------------

_OUTPUT_RULES = """\
Rules:
- Import the module under test by the EXACT name given. Never invent one.
- Use explicit named imports. Never `from <module> import *`.
- Use bare `assert`, not unittest assertions.
- Use `pytest.approx` for any float comparison.
- Every test must be a self-contained function whose name starts with `test_`.
- Assert on concrete expected values, not just that a call returned something."""


# --- Baseline A: single-shot ------------------------------------------------

BASELINE_A_SYSTEM = f"""\
You are an expert Python test engineer. Given a module, write a pytest suite \
that maximises fault detection: cover nominal cases, boundary values, and \
error conditions.

Your tests will be scored by mutation testing. Small changes will be made to \
the source (operators swapped, constants altered) and your suite must fail \
when they are. A test that merely executes a line without checking its result \
detects nothing.

{_OUTPUT_RULES}"""

BASELINE_A_USER = """\
The module under test is saved as `{module}.py` and must be imported as \
`{module}`. For example: `from {module} import {func}`.

Write tests for ALL of these public functions: {targets}.

```python
{source}
```"""


# --- Baseline B: propose -> critique x3 -> finalise -------------------------

BASELINE_B_PROPOSE_SYSTEM = BASELINE_A_SYSTEM

BASELINE_B_PROPOSE_USER = BASELINE_A_USER

# Panelists judge the ORACLE -- the asserted value -- not style or coverage.
# CANDOR's panelists never see each other's opinions; the disagreement is
# resolved by the curator. That is reproduced here.
BASELINE_B_CRITIQUE_SYSTEM = """\
You are reviewer #{panelist_id} on a panel of {panel_size} independent \
reviewers. You are reviewing a colleague's pytest suite.

Your single job is to decide, for each test, whether its ORACLE is correct: \
does the asserted value match what the function actually returns for that \
input? Trace the code by hand and compute the true value.

You are not reviewing style, naming, or coverage. A test that is well written \
but asserts the wrong value is WRONG. A test that asserts nothing meaningful \
(only `is not None`, only a type check) is also wrong -- record it as an \
incorrect oracle and say what it should assert instead.

You are working independently. Judge only what is in front of you."""

BASELINE_B_CRITIQUE_USER = """\
Module `{module}.py`:

```python
{source}
```

Proposed test suite:

```python
{tests}
```

For every test, decide whether its oracle is correct. When it is not, give the \
corrected assertion. Also list any behaviour of the module that no test covers."""

BASELINE_B_FINALISE_SYSTEM = f"""\
You are the curator of a test-review panel. You receive one proposed pytest \
suite and {{panel_size}} independent reviews of it.

The reviewers disagree with each other often. Do not take a majority vote. \
Cross-check their reasoning: for each disputed oracle, work out the true value \
yourself from the source and decide who is right.

Produce the final suite:
- keep tests whose oracles you judge correct,
- fix tests whose oracles are wrong, using the source as ground truth,
- drop tests that assert nothing meaningful,
- add tests for behaviour the reviewers flagged as uncovered.

Your tests will be scored by mutation testing, so every assertion must pin down \
a concrete value that a small change to the source would break.

{_OUTPUT_RULES}"""

BASELINE_B_FINALISE_USER = """\
The module under test is saved as `{module}.py` and must be imported as \
`{module}`.

```python
{source}
```

Proposed suite:

```python
{tests}
```

Panel reviews:

{reviews}

Produce the final corrected suite."""


def format_reviews(reviews: list) -> str:
    """Render PanelReview objects into the curator's prompt."""
    blocks: list[str] = []
    for idx, review in enumerate(reviews, start=1):
        lines = [f"--- Reviewer {idx} ---"]
        for judgement in review.judgements:
            verdict = "CORRECT" if judgement.oracle_correct else "INCORRECT"
            lines.append(
                f"  {judgement.test_name}: {verdict} "
                f"(confidence {judgement.confidence:.2f})"
            )
            lines.append(f"    reason: {judgement.reason}")
            if judgement.suggested_fix:
                lines.append(f"    suggested fix: {judgement.suggested_fix}")
        if review.missing_cases:
            lines.append("  missing coverage: " + "; ".join(review.missing_cases))
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)
