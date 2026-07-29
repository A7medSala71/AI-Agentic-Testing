# Week 1 Report — Member 3 (Baseline Systems Lead)

**Scope per brief:** environment setup + literature survey.
**Status:** complete. Environment verified against the live API (§6).

---

## 1. What was built

| Item | Evidence |
|---|---|
| Python 3.12.4 venv, pinned deps | `requirements.txt` |
| pytest 9.1.1, mutmut 3.6.0, coverage 7.15.2 | `baselines/toolchain_check.py` passes |
| LLM SDK + structured outputs | `baselines/llm_client.py`, verified by `smoke_test` |
| Per-call token / cost accounting | `UsageTracker` in `llm_client.py` |
| Prompt-context builder | `baselines/prompt_context.py` |
| Schema-validated run logging | `baselines/run_log.py` |
| Literature survey — all of §1.1–§1.4 | `docs/literature_survey.md` |

Run either check:

```bash
.venv/bin/python -m baselines.smoke_test
.venv/bin/python -m baselines.toolchain_check
```

`smoke_test` works **without an API key** (mock mode), so the pipeline is
verifiable before spending anything.

### Model

The brief names "Gemini 3 Flash", but that ID has been superseded. We use
**`gemini-3.6-flash`**, the current GA Flash model
([docs](https://ai.google.dev/gemini-api/docs/latest-model)). The pricing in
brief §4 ($0.50 / $3.00 per 1M) is carried over in `config.py` and **must be
re-verified** before any cost figure enters the paper.

### Temperature

`config.TEMPERATURE = 1.0`, not 0. Brief §3.4 requires 3 repeats per function
reported as mean ± standard deviation, which only carries information if
generation is actually stochastic. At temperature 0 the three repeats would be
near-identical and the reported deviation meaningless.

---

## 2. Measured result: coverage does not detect weak oracles

`toolchain_check.py` runs two suites against `function_03` (`arc_length`):

| Suite | Line coverage | Mutation score |
|---|---|---|
| Strong oracle — `== pytest.approx(15.707963267948966)` | 80.0% | **100.0%** (6/6) |
| Weak oracle — `is not None` / `isinstance(result, float)` | 80.0% | **0.0%** (0/6) |

**Coverage is identical. Mutation score differs by 100 points.**

This is RQ2's premise demonstrated on our own dataset, and it is worth
reproducing as a motivating figure in the paper: it justifies mutation score as
the headline metric over coverage in a single table.

---

## 3. Blocking issue: `evaluation/` does not run

Member 2's pipeline crashes on import:

```
ModuleNotFoundError: No module named 'evaluation.coverage_runner.py';
'evaluation.coverage_runner' is not a package
```

`evaluation/evaluator.py:5-6` — the import path carries a `.py` suffix:

```python
from evaluation.coverage_runner.py import run_coverage   # -> .coverage_runner
from evaluation.mutation_runner.py import run_mutation   # -> .mutation_runner
```

Four further issues, all verified locally:

1. **`mutmut run` with no config fails.** mutmut 3.6 aborts before doing any
   work — even `mutmut --help` raises `FileNotFoundError` — unless `setup.cfg`
   declares a `[mutmut]` section. A working config:

   ```ini
   [mutmut]
   source_paths=function_03.py
   pytest_add_cli_args_test_selection=tests/
   ```

   Note mutmut 3.x renamed its keys: `paths_to_mutate` → `source_paths`, and
   `tests_dir` → `pytest_add_cli_args_test_selection`. The old names still
   parse but emit deprecation warnings.

2. **Results should be read from JSON, not scraped from stdout.** mutmut 3.x
   writes `mutants/<file>.py.meta` containing `exit_code_by_key`; a non-zero
   exit code means the mutant was killed. Parsing that is stable, whereas
   stdout is a live-updating spinner (see the raw output in this repo's run
   logs — it is not parseable).

3. **Return types violate the team's own schema.** `evaluator.py` puts raw
   stdout *strings* into `line_coverage_pct` and `mutation_score_pct`, but
   `schema/execution_log_schema.json` declares both as `"type": "number"`.

4. **No per-function isolation.** `run_mutation()` mutates everything at once
   and `run_coverage()` runs the whole suite, so a per-`function_id` score —
   which the schema requires — cannot be produced.

`baselines/toolchain_check.py` contains a working reference implementation of
the config, the run, and the score parsing. It is Member 2's component to own;
the code is there to unblock, not to take over.

---

## 4. Decisions the team needs to make

### 4.1 Doctest policy — DECIDED (Prof. Doaa, Week 3): strip them

Every dataset function carries doctests, i.e. literal input→output oracles, in
its docstring:

```python
def arc_length(angle: int, radius: int) -> float:
    """
    >>> arc_length(45, 5)
    3.9269908169872414
    """
```

Handing those to the model measures transcription, not oracle reasoning.

- **(a) Strip doctests** — prompt on signature + prose only. Measures what RQ2 actually asks about. **Currently implemented (`INCLUDE_DOCTESTS=false`).**
- **(b) Keep them** — more realistic, but inflates all systems and blurs the comparison.

**Resolved:** strip them. The decisive argument was comparability — CANDOR's
HumanEvalJava benchmark carries no worked examples (the Java translation drops
HumanEval's Python docstrings), so stripping ours matches the system we compare
against. See `docs/week2_baseline_design.md` §3a for the full rationale and the
ablation that was considered and set aside.

### 4.2 Unit of testing — 17 of 30 files hold more than one public function

`function_01` has `slow_primes`, `primes`, `fast_primes`; `function_08` has
five defs. Measured across the dataset: **17 of 30 files** contain more than one
public function.

Options: test only the primary function; test all public functions per file; or
split the dataset so one file means one function. This changes the file count,
every per-function metric, and the denominator of the mutation score.

Non-testable scaffolding (`benchmark`, `if __name__ == "__main__"`) is already
excluded from prompts.

### 4.3 Schema fields missing for §3.5 metrics

`schema/execution_log_schema.json` has no slot for three required metrics:

| Missing field | Why it is needed |
|---|---|
| `num_llm_calls` | §3.5 requires "**Number of LLM calls** (and tokens)". Baseline B spends 5 calls to Baseline A's 1 — RQ1's cost-fairness claim cannot be made from tokens alone. |
| `pass_rate_pct` | Listed as a metric in §3.5, no slot exists. |
| `branch_coverage_pct` | §3.5 says "line/branch"; only `line_coverage_pct` exists. |

`ExecutionLog` in `baselines/schemas.py` already emits all three so no run has
to be repeated later, but they are dropped on write until Member 1 adds them to
the schema. **Requested from Member 1.**

### 4.4 Equivalent mutants

Meta's ACH paper reports needing a dedicated detector for mutants that are
impossible to kill. Untreated, they depress every system's score and can
consume Member 4's entire 5-iteration budget on an unkillable target.
**Flagged to Members 2 and 4** — needs an owner.

### 4.5 Baseline B must be described honestly

CANDOR's Step II is an iterative *coverage* loop worth −0.111 mutation score in
their ablation. Our Baseline B forbids all iteration, so it will be
substantially weaker than published CANDOR.

That is the correct design — RQ1 asks whether mutation-guided iteration beats
consensus alone, so the comparator must be non-iterative — but the paper must
state plainly that Baseline B is a **consensus-only ablation of CANDOR, not a
CANDOR reimplementation**, and cite the −0.111 figure. Otherwise a reviewer
will read it as a straw man. **Needs Prof. Doaa's sign-off.**

---

## 5. Second measured result: wildcard imports corrupt the pass rate

`function_25.py` ships its own `class Test(unittest.TestCase)` with
`test_primes` and `test_not_primes` inside it. Measured:

```
from function_25 import is_prime   ->  1 test collected
from function_25 import *          ->  3 tests collected
```

Two of those three came from the dataset, not from the model. Untreated, this
inflates `function_25`'s test count and pass rate for **every** system, and
looks like the model wrote passing tests it never wrote.

Blocked in code: `GeneratedTestSuite.to_source()` raises on any wildcard
import, and `smoke_test.py` asserts it. Belongs in the paper's threats to
validity.

---

## 6. Live API verification — done

`baselines/live_check.py`, run against `gemini-3.6-flash` on `function_03`.

### 6.1 Structured output is reliable

**10/10 calls conformant (100%)** across two runs. Brief §4's warning that
Gemini is "less consistent" at structured output did not materialise at this
sample size. No retry wrapper is needed yet; re-check at full scale.

### 6.2 Reasoning tokens dominate the bill

| | tokens |
|---|---|
| input | 855 |
| output (`candidates_token_count`) | 3,149 |
| **reasoning (`thoughts_token_count`)** | **5,319** |
| total | 9,323 |

**Reasoning tokens are 63% of all generated tokens** — they exceed the visible
output. Counting only prompt + candidates, as a naive wrapper would, understates
the bill by roughly 2.7×. `UsageTracker` bills them at the output rate.

### 6.3 Cost is not a constraint

$0.0052 per call → **$2.79 projected** for Baseline A + B across 30 functions ×
3 repeats (list-price equivalent; actual spend is $0 on the free tier). The
brief's §4 estimate of $8–18 for Gemini was conservative.

### 6.4 Finding: the module name must be in the prompt

The model never sees the filename, only the source. Left to infer it, it
invents one — observed: `solution`, `arc_length_module` — and every generated
suite then dies with `ModuleNotFoundError`.

| Prompt | Pass rate |
|---|---|
| Source only | **0/5 (0%)** |
| Source + "saved as `function_03.py`, import as `function_03`" | **4/5 (80%)** |

This single line moved the pass rate 80 points. It must be in Baseline A,
Baseline B, and both of Member 4's variants — a system that omits it scores
zero for reasons that have nothing to do with its design.

### 6.5 BLOCKER: the free tier cannot run this experiment

After roughly **20 successful calls** the API began returning
`429 RESOURCE_EXHAUSTED`. Three probes spread over ~70 seconds were all
rejected, so this is a **daily** cap, not a per-minute one. Per Google's docs,
requests-per-day quotas reset at midnight Pacific time.

Call budget for the full procedure in brief §3.4 (30 functions × 3 repeats):

| System | Calls per run | Total |
|---|---|---|
| Baseline A | 1 | 90 |
| Baseline B | 5 | 450 |
| Variant 1 (ErrorTrace) | ~4 | ~360 |
| Variant 2 (StatePrediction) | ~4 | ~360 |
| **Total, one clean pass** | | **~1,260** |

At ~20 calls/day that is **63 days for a single clean pass, with no allowance
for debugging or re-runs.** The deadline is 15 Aug — 18 days away. Even with
all four members on separate keys (~80/day) one pass takes ~16 days with zero
margin.

**Recommendation: enable billing on one key.** Measured cost is $0.0052 per
call, so the entire experiment — all four systems, plus generous re-runs — lands
in the **$5–15** range. That is far below the brief's own §4 estimate of $8–18
for Gemini, and it removes a blocker that would otherwise surface in Week 4 when
there is no time left to react.

This needs Prof. Doaa's decision now, not in Week 4. Until it is resolved,
development is limited to ~20 live calls per person per day, which is workable
for Week 2–3 prototyping but not for the full runs.

**Mitigations already in place:** `smoke_test.py` is forced to mock mode so it
never consumes quota, and `toolchain_check.py` needs no API at all. Only
`live_check.py` and the baselines themselves spend calls.

### 6.6 Observed: single-shot generation does hallucinate oracles

Across 11 single-shot generations for `arc_length`, **one** produced a suite
with a wrong assertion — it passed schema validation, imported correctly, ran,
and asserted the wrong value. The other 10 were fully correct.

n=11 on one simple function is far too small to report as a rate, and it is
listed here only as a qualitative observation. But it is exactly the failure
mode Baseline B's panel exists to catch, and the same measurement at full scale
is what RQ2 quantifies.

---

## 7. Next (Week 2)

Design and freeze the prompts and architecture for both baselines:
`baseline_a.py` (1 call) and `baseline_b.py` (propose → 3× critique →
finalise, 5 calls). Blocked on §4.1 and §4.2 being decided.

Carry into the prompt design:

- the module-name line from §6.4 — non-negotiable, worth 80 points of pass rate;
- explicit named imports only, per §5;
- `pytest.approx` for floats — most of this dataset returns them.
