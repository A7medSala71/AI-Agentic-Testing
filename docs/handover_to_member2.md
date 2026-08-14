# Handover — Member 3 → Member 2

**Baseline A and Baseline B are complete.** 180 runs, all generated, scored and
logged. Everything below is on the repo and ready to consume.

---

## 1. What you have

| | count | where |
|---|---|---|
| Generated test suites | **180** | `generated_tests/` |
| Run records | **180** | `logs/` |
| Functions covered | **30 of 30** | — |
| Repeats per function | **3** | brief §3.4 |

Naming, one file per run:

```
<function_id>__<system_variant>__run<n>__test.py

function_03__Baseline_A__run1__test.py
function_21__Baseline_B__run3__test.py
```

`system_variant` matches the enum in `schema/execution_log_schema.json` exactly,
so a filename parses straight into a record. Mock output carries `__MOCK__` and
is gitignored — nothing in the repo is canned.

### Generation settings, fixed for the whole experiment

| | |
|---|---|
| Model | `gemini-3.5-flash-lite` |
| Temperature | 1.0 (brief §3.4 needs stochastic repeats for mean ± SD) |
| Doctests | stripped (Prof. Doaa, Week 3) |
| Unit of testing | all public functions per file |

**Do not change the model when scoring or re-running.** Mixing models compares
models rather than systems.

---

## 2. Each suite must be scored in isolation

A suite imports its module by bare name (`from function_03 import arc_length`),
and mutmut mutates whatever `source_paths` points at. Scoring all 30 in one
directory would mutate all of them at once and score every suite against every
other function's mutants.

One temp workspace per (function × system × run):

```
<workspace>/
├── function_03.py                      # copied from dataset/
├── setup.cfg                           # [mutmut] config, below
└── tests/
    └── test_function_03.py             # the generated suite
```

---

## 3. The mutmut recipe that works

Verified against **mutmut 3.6.0**. Three findings that cost real time:

**(a) mutmut 3.x will not start without config.** Even `mutmut --help` raises
`FileNotFoundError` with no `[mutmut]` section. A bare `mutmut run` — as in the
current `mutation_runner.py` — fails before doing any work.

**(b) The config keys were renamed in 3.x.** The old names still parse but emit
deprecation warnings:

| old | new |
|---|---|
| `paths_to_mutate` | `source_paths` |
| `tests_dir` | `pytest_add_cli_args_test_selection` |

```ini
[mutmut]
source_paths=function_03.py
pytest_add_cli_args_test_selection=tests/
```

**(c) Read results from JSON, not stdout.** `mutmut run` prints a live-updating
spinner that is not parseable, and `mutmut results` prints nothing when every
mutant is killed. The machine-readable output is `mutants/<file>.py.meta`:

```python
meta = json.loads(Path("mutants/function_03.py.meta").read_text())
exit_codes = meta["exit_code_by_key"]
killed = sum(1 for code in exit_codes.values() if code != 0)   # non-zero == killed
total  = len(exit_codes)
mutation_score_pct = killed / total * 100
```

A **non-zero** exit code means the suite failed against that mutant, i.e. the
mutant was **killed**. Zero means it survived.

A complete working implementation is `baselines/score.py` — copy from it freely.
It also computes line coverage (`coverage json` → `totals.percent_covered`) and
pass rate.

> `score.py` exists so the baselines could be validated while `evaluation/` was
> unavailable. It is **not** a replacement — the paper's numbers should come
> from the shared pipeline so all four systems are scored identically. The
> figures in §6 below are from `score.py` and are there as a reference to check
> your pipeline against, not as the final numbers.

---

## 4. Two things currently blocking `evaluation/`

**It does not import.** `evaluation/evaluator.py:5-6` carries a `.py` suffix in
the module path:

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
`schema/execution_log_schema.json` declares both as `"type": "number"`. Records
built from that output will not validate.

---

## 5. `function_18` cannot be imported — dataset issue

`dataset/function_18.py` reads a data file **at import time**:

```python
data: str = Path(__file__).parent.joinpath("words.txt").read_text(encoding="utf-8")
```

`words.txt` is not in `dataset/`, so importing raises `FileNotFoundError` before
any test runs. Checked across all 30 files — **it is the only one affected**.

Every suite for `function_18` therefore errors at collection, for both systems
and all three repeats. This is not a model failure and should not be counted as
one; the generated tests themselves are fine.

Worth noting: **half the file is fine.** `signature()` is a pure function and
perfectly testable — only `anagram()` needs the word list. Adding `words.txt`
would recover both functions rather than losing the benchmark item.

For Member 1 to decide: add the file, move the file-reading lines under
`if __name__ == "__main__":`, or drop the function and report n=29. Until then,
**exclude `function_18` from reported means** — it scores 0 for every system, so
it depresses all of them identically for a reason unrelated to oracle quality.

---

## 6. Reference figures to check your pipeline against

From `score.py` on the same 180 runs. If your pipeline lands close to these,
it is working; a large divergence means one of us has a bug worth finding
before the paper.

| | mutation score | line coverage |
|---|---|---|
| Baseline A | 94.5% ± 6.9 | 73.7% |
| Baseline B | 95.1% ± 5.7 | 73.0% |

Paired across all 30 functions (repeats averaged per function first):

```
difference        +0.6 points
tied              17 of 30 functions
Wilcoxon          W = 28.0, p = 0.2213  -- not significant
```

Two single-function anchors, useful as unit checks:

| function | system | expected |
|---|---|---|
| `function_03` (`arc_length`, 6 mutants) | Baseline A | 100% mutation |
| `function_21` (`binary_search`, 19 mutants) | Baseline A | ~89.5% (17/19) |

---

## 7. What Member 3 writes into `logs/`

```json
{
  "function_id": "function_03",
  "system_variant": "Baseline_A",
  "iteration_count": 1,
  "total_tokens_used": 902,
  "estimated_cost_usd": 0.002011,
  "line_coverage_pct": 80.0,
  "mutation_score_pct": 100.0,
  "num_llm_calls": 1,
  "pass_rate_pct": 100.0
}
```

`iteration_count` is always **1** for both baselines — neither iterates.
`iterations_detail` is left unset: it is mutant-centric and meant for Member 4's
refinement variants, whereas a baseline emits one suite scored against all
mutants at once.

Note that `num_llm_calls` and `pass_rate_pct` appear above but are **not in the
schema** — they survive only because nothing strips unknown keys on read.

### Schema request for Member 1

`ExecutionLog` in `baselines/schemas.py` emits six fields that
`schema/execution_log_schema.json` has no slot for:

| field | why |
|---|---|
| `num_llm_calls` | brief §3.5 requires it, and RQ1's cost-fairness claim cannot be made from tokens alone — Baseline B spends 5 calls to Baseline A's 1 |
| `pass_rate_pct` | listed as a metric in brief §3.5 |
| `branch_coverage_pct` | brief §3.5 says "line/branch"; only line exists |
| `input_tokens`, `output_tokens`, `thought_tokens` | see below |

The token breakdown matters for a reason we hit in practice. Cost is computed
from a per-model price, so a wrong price — or a model change — makes every
stored cost wrong with **no way to recompute from the total alone**, because
input and output bill at different rates. Our own figures were ~25% high until
the Flash-Lite price was corrected, and the 180 existing records cannot be
repaired without regenerating them.

The breakdown is now emitted, so **runs generated from here on carry it**; the
180 already logged do not.

---

## 8. If you want to re-run anything

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env          # then add your own Gemini API key

.venv/bin/python -m baselines.smoke_test        # no API key needed
.venv/bin/python -m baselines.toolchain_check   # no API key needed

.venv/bin/python -m baselines.baseline_a --all --repeats 3
.venv/bin/python -m baselines.score --update-logs
.venv/bin/python -m baselines.compare
```

Runs are **resumable** — anything already logged with its suite still present is
skipped, so an interrupted sweep continues rather than restarting.

Get a free key at <https://aistudio.google.com/apikey>. The free tier allows 500
requests/day on this model; a full Baseline A + B pass needs ~540, so either
enable billing or expect it to span two days.
