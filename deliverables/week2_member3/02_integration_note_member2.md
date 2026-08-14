# Integration note — Member 3 → Member 2

**What the mutation pipeline can expect from the Baseline systems, and what
Member 3 found while validating them locally.**

---

## 1. Where the test files are

Generated suites land in `generated_tests/` at the repo root, one file per run:

```
<function_id>__<system_variant>__run<n>__test.py

function_03__Baseline_A__run1__test.py
function_03__Baseline_B__run1__test.py
function_17__Baseline_A__run2__test.py
```

`system_variant` matches the enum in `schema/execution_log_schema.json`
exactly (`Baseline_A`, `Baseline_B`, …), so a filename parses straight into a
log record.

**These files are committed.** Mock output (`__MOCK__` in the name) is
gitignored — it is a fixed canned suite, identical for every function, and
would be mistaken for real data.

### Current status

| | count |
|---|---|
| Real generated suites | **1** (`function_03`, Baseline A) |
| Remaining | 29 for Baseline A, 30 for Baseline B |

The single real file is there so the pipeline can be developed against a true
sample rather than a placeholder. See §4 for when the rest arrives.

---

## 1a. `function_18` cannot be imported — dataset issue, not a generation issue

`dataset/function_18.py` reads a data file **at import time**:

```python
data: str = Path(__file__).parent.joinpath("words.txt").read_text(encoding="utf-8")
```

`words.txt` is not in `dataset/`, so importing the module raises
`FileNotFoundError` before any test runs. Verified across all 30 files —
**it is the only one affected**:

```
ملفات مش بتتستورد لوحدها: 1 من 30
  function_18: FileNotFoundError: No such file or directory: '.../words.txt'
```

Every generated suite for `function_18` therefore errors at collection, in all
three repeats and for both systems. This is not a model failure and should not
be counted as one — the generated tests themselves are fine.

**Three options, for Member 1 to pick:**

1. Add `words.txt` to `dataset/`.
2. Move the file-reading lines under `if __name__ == "__main__":` so import is side-effect free.
3. Drop `function_18` from the benchmark and report n=29.

Until it is resolved, exclude `function_18` from reported means — leaving it in
depresses every system's score identically, for a reason unrelated to oracle
quality.

---

## 2. Each suite must be scored in isolation

A generated suite imports its module by bare name (`from function_03 import
arc_length`), and mutmut mutates whatever `source_paths` points at. Running
all 30 functions in one directory would mutate all of them at once and score
every suite against every other function's mutants.

The working layout is one temp workspace per (function × system × run):

```
<workspace>/
├── function_03.py                      # copied from dataset/
├── setup.cfg                           # [mutmut] config, see below
└── tests/
    └── test_function_03.py             # the generated suite
```

---

## 3. The mutmut recipe that works

Verified against mutmut **3.6.0**. Three findings that cost time to discover:

**(a) mutmut 3.x refuses to start without config** — even `mutmut --help`
raises `FileNotFoundError` when there is no `[mutmut]` section. A bare
`mutmut run` (as in the current `mutation_runner.py`) fails before doing any
work.

**(b) The config keys were renamed in 3.x.** The old names still parse but
emit deprecation warnings:

| old | new |
|---|---|
| `paths_to_mutate` | `source_paths` |
| `tests_dir` | `pytest_add_cli_args_test_selection` |

```ini
[mutmut]
source_paths=function_03.py
pytest_add_cli_args_test_selection=tests/
```

**(c) Read results from JSON, not stdout.** `mutmut run` prints a live
updating spinner — it is not parseable, and `mutmut results` prints nothing
when every mutant is killed. The machine-readable output is
`mutants/<file>.py.meta`:

```python
import json
meta = json.loads(Path("mutants/function_03.py.meta").read_text())
exit_codes = meta["exit_code_by_key"]
killed = sum(1 for code in exit_codes.values() if code != 0)   # non-zero == killed
total  = len(exit_codes)
mutation_score_pct = killed / total * 100
```

A **non-zero** exit code means the test suite failed against that mutant,
i.e. the mutant was **killed**. Zero means it survived.

A complete working implementation is in `baselines/score.py` — copy from it
freely. It also computes line coverage (`coverage json` → `totals.percent_covered`)
and pass rate.

> `score.py` exists so Baseline A and B could be validated while
> `evaluation/` was unavailable. It is **not** a replacement — the paper's
> numbers should come from the shared pipeline so all four systems are scored
> identically.

---

## 4. Timeline for the remaining files

Baseline A is 1 LLM call per function; Baseline B is 5.

| deliverable | calls | on free tier (20/day) | with billing |
|---|---|---|---|
| Baseline A, all 30, 1 repeat | 30 | ~1.5 days | minutes |
| Baseline B, all 30, 1 repeat | 150 | ~7.5 days | minutes |
| Both, 3 repeats (brief §3.4) | 540 | ~27 days | under an hour |

Billing is being enabled. Until it is active, **Baseline A for all 30
functions is deliverable in about two days** even on the free tier — that is
the first useful batch for the pipeline.

Runs are resumable: `baselines/runner.py` skips any run already logged, so a
sweep interrupted by quota picks up where it stopped rather than restarting.

---

## 5. Two things blocking the pipeline right now

Both were found while trying to score Baseline A's output.

**`evaluation/evaluator.py` does not import.** Lines 5–6 carry a `.py` suffix
in the module path:

```python
from evaluation.coverage_runner.py import run_coverage   # -> .coverage_runner
from evaluation.mutation_runner.py import run_mutation   # -> .mutation_runner
```

```
ModuleNotFoundError: No module named 'evaluation.coverage_runner.py';
'evaluation.coverage_runner' is not a package
```

**Return types don't match the team schema.** `evaluate()` puts raw stdout
*strings* into `line_coverage_pct` and `mutation_score_pct`, but
`schema/execution_log_schema.json` declares both as `"type": "number"`. A run
built from that output will not validate.

---

## 6. What Member 3 writes into `logs/`

Once a run completes, `baselines/runner.py` writes a schema-validated record:

```json
{
  "function_id": "function_03",
  "system_variant": "Baseline_A",
  "iteration_count": 1,
  "total_tokens_used": 2532,
  "estimated_cost_usd": 0.006901,
  "line_coverage_pct": 80.0,
  "mutation_score_pct": 100.0,
  "num_llm_calls": 1,
  "pass_rate_pct": 100.0
}
```

`iteration_count` is always **1** for both baselines — neither iterates.
`iterations_detail` is left unset: it is mutant-centric and meant for Member
4's refinement variants, whereas a baseline emits one suite scored against all
mutants at once.

**Three fields are dropped on write** because the schema has no slot for them:
`num_llm_calls`, `pass_rate_pct`, and `branch_coverage_pct`. All three are
required by brief §3.5 — `num_llm_calls` in particular, since Baseline B
spends 5 calls to Baseline A's 1 and RQ1's cost-fairness claim cannot be made
from token counts alone. Requested from Member 1.

If the pipeline computes the scores instead, Member 3's runner can stop
scoring locally and just consume them — say which direction you prefer.
