# Week 1 Deliverables — Member 3 (Baseline Systems Lead)

| | |
|---|---|
| **Project** | Agentic Testing — Team 1: Oracle-Quality Test Generation |
| **Supervisor** | Prof. Doaa Shawky |
| **Role** | Member 3 — Baseline Systems Lead (Baseline A, Baseline B, prompt design) |
| **Week 1 scope per brief** | environment setup + literature survey |
| **Status** | complete, verified against the live API |

---

## Contents

| File | What it is |
|---|---|
| `01_literature_survey.md` | Literature survey covering brief §1.1–§1.4 |
| `02_week1_report.md` | Week 1 report: what was built, measured results, open decisions |
| `code/` | The environment and infrastructure both baselines sit on |
| `evidence/` | Captured output of every verification check |

---

## Summary

### Delivered

- Python 3.12 environment with pinned dependencies (pytest 9.1.1, mutmut 3.6.0, coverage 7.15.2, google-genai 2.14.0).
- Schema-constrained LLM client with per-call token, reasoning-token and cost accounting.
- Prompt-context builder that applies the doctest and scaffolding policies via the AST.
- Run logging validated against the team's `execution_log_schema.json`.
- Three verification harnesses: `smoke_test` (offline), `toolchain_check` (offline), `live_check` (live API).
- Literature survey covering every reading section of the brief that applies to this role.

### Measured results

**Coverage does not detect weak oracles.** Two suites on the same function:

| Suite | Line coverage | Mutation score |
|---|---|---|
| Strong oracle | 80.0% | **100.0%** (6/6) |
| Weak oracle | 80.0% | **0.0%** (0/6) |

Coverage identical, mutation score 100 points apart. This is RQ2's premise
demonstrated on the project's own dataset.

**Structured output is reliable.** 10/10 live calls conformant. The brief's
concern about Gemini's structured-output consistency did not materialise.

**Reasoning tokens are 63% of generated tokens** (5,319 vs 3,149 visible
output). A wrapper counting only prompt + output would understate cost by
roughly 2.7×.

**The prompt must state the module name.** The model never sees the filename
and invents one when not told, killing every generated suite with
`ModuleNotFoundError`. Adding one line moved the pass rate from **0% to 80%**.

**Wildcard imports corrupt the pass rate.** `function_25.py` ships its own
`unittest` class; `from function_25 import *` makes pytest collect the
dataset's tests as if the model had written them (1 test becomes 3). Blocked in
code.

### Escalations

1. **Free tier cannot run the experiment.** ~20 calls/day against a ~1,260-call requirement. Enabling billing costs an estimated $5–15 total. Needs a decision now, not in Week 4.
2. **`evaluation/` does not run** — import error plus four further issues; a working reference implementation is included.
3. **Four team decisions** — doctest policy, unit of testing (17 of 30 files hold more than one function), three schema fields missing for §3.5 metrics, and equivalent-mutant ownership.

Full detail in `02_week1_report.md`.

---

## Reproducing

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m baselines.smoke_test        # no API key needed
.venv/bin/python -m baselines.toolchain_check   # no API key needed
```

Both run offline. `live_check` additionally needs a key in `.env` — see
`code/README.md`.

`code/` is a snapshot for review. The working copy lives in `baselines/` at the
repository root.
