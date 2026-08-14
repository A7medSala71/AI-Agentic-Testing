# Agentic Testing — Oracle-Quality Test Generation

Research project investigating whether an **iterative, mutant-survival-guided
refinement loop** produces higher-quality test oracles than single-shot LLM
generation or one-shot multi-agent consensus.

**Supervisor:** Prof. Doaa Shawky · **Team of 4** · Jul–Aug 2026

---

## The question

LLMs write plausible-looking tests, but they hallucinate the **oracle** — the
assertion about what the answer should be. A test with a wrong assertion is
worse than no test: it either fails on correct code, or silently passes on
broken code.

That second failure is a **weak oracle**, and coverage cannot detect it.
Measured on this project's own dataset:

| Test suite for `arc_length` | Line coverage | Mutation score |
|---|---|---|
| Strong oracle — `== pytest.approx(15.707963267948966)` | 80.0% | **100.0%** (6/6) |
| Weak oracle — `is not None`, `isinstance(result, float)` | 80.0% | **0.0%** (0/6) |

Identical coverage. A hundred points of difference in faults caught. This is
why the project's headline metric is mutation score rather than coverage.

Reproduce with `python -m baselines.toolchain_check`.

---

## Systems compared

| System | Description | LLM calls per function |
|---|---|---|
| **Baseline A** | Single-shot generation — one prompt, no feedback | 1 |
| **Baseline B** | One-shot multi-agent consensus (simplified CANDOR) | 5 |
| Variant 1 | Mutant-guided refinement, error-trace feedback | up to 5 iterations |
| Variant 2 | Mutant-guided refinement, state prediction | up to 5 iterations |

Baseline B's pipeline:

```
       propose (1 call)
          |
          +--> panelist 1 --+
          +--> panelist 2 --+--> curator (1 call) --> final suite
          +--> panelist 3 --+
               (3 calls, independent)
```

---

## Final merged architecture

The final repository combines the three member deliverables behind one evaluation
contract:

```text
Baseline A/B ───────┐
                    ├──> shared evaluation/ (pytest + coverage.py + mutmut)
Refinement seed ────┤
                    │
                    └──> RefinementLoop
                           ├─ surviving mutant extraction
                           ├─ ErrorTrace strategy
                           └─ StatePrediction strategy
```

The proposed system uses the **same Baseline-A-style seed** and then feeds the
same shared mutation/coverage results back into the refinement loop. Final
generated suites are saved under `generated_tests/`, and every live run writes
a schema-validated JSON record under `logs/`.

## Repository layout

| Path | Contents | Owner |
|---|---|---|
| `dataset/` | 30 Python functions under test | Member 1 |
| `schema/` | Shared execution-log contract | Member 1 |
| `evaluation/` | Shared mutation + coverage pipeline | Member 2 |
| `baselines/` | **Baseline A & B, prompts, scoring, run harness** | **Member 3** |
| `docs/` | **Design documents and weekly reports** | **Member 3** |
| `deliverables/` | **Weekly submission packages (Markdown + Word)** | **Member 3** |
| `generated_tests/` | Generated test suites, one file per run | — |
| `logs/` | Schema-validated run records | — |

This repository is maintained by **Member 3 (Baseline Systems Lead)**. The
`dataset/`, `schema/`, and `evaluation/` directories are teammates' work,
included because the baselines build on them; commit history preserves
authorship.

---

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env          # then add your own Gemini API key
```

Get a free key at <https://aistudio.google.com/apikey>. `.env` is gitignored —
never commit a key to this repository.

### Verify the environment (no API key needed)

```bash
.venv/bin/python -m baselines.smoke_test        # end-to-end acceptance check
.venv/bin/python -m baselines.toolchain_check   # mutation toolchain + the table above
```

Both run fully offline in mock mode.

### Generate and score

```bash
.venv/bin/python -m baselines.baseline_a function_03           # one function
.venv/bin/python -m baselines.baseline_a --all --score         # all 30, scored + logged
.venv/bin/python -m baselines.baseline_b --all --score
.venv/bin/python -m baselines.score                            # score what exists
```

Runs are **resumable** — anything already logged is skipped, so a sweep
interrupted by an API quota picks up where it stopped.

---

## Proposed refinement commands

```bash
python -m refinement_loop.run_live function_03 --provider groq --variant error_trace
python -m refinement_loop.run_live function_03 --provider groq --variant state_prediction
python -m refinement_loop.run_live --all --repeats 3 --provider groq --variant error_trace
python -m refinement_loop.run_live --all --repeats 3 --provider groq --variant state_prediction
```

For Gemini, replace `--provider groq` with `--provider gemini`.

The proposed run counts the **seed generation call plus refinement calls** in
`num_llm_calls` and token totals. The final suite is persisted, so the exact
suite used for the logged mutation score can be replayed.

## Colab / notebook

Use `notebooks/final_experiment.ipynb`. It installs the pinned dependencies,
runs the offline acceptance tests first, accepts an API key without storing it
in the notebook, provides one-function smoke runs, and contains the resumable
30-function × 3-repeat commands for the final experiment.

## Prompt rules (non-negotiable across all four systems)

Each was forced by a measurement, not a preference. A system that omits any of
them scores badly for reasons unrelated to its design, which would invalidate
the comparison.

| Rule | Why | Measured effect |
|---|---|---|
| State the module name in the prompt | The model never sees the filename and invents one | pass rate **0% → 80%** |
| Explicit named imports only | `from function_25 import *` drags that file's own `unittest` class in | 1 test becomes 3 collected |
| `pytest.approx` for floats | Most of the dataset returns floats | exact `==` is a flaky oracle |

---

## Key reading

- **CANDOR** — [arXiv:2506.02943](https://arxiv.org/abs/2506.02943) — the multi-agent consensus design Baseline B is derived from
- **Mutation-Guided LLM Test Generation at Meta** — [arXiv:2501.12862](https://arxiv.org/pdf/2501.12862) — equivalent-mutant detection
- **LogicHunter** — [arXiv:2607.06195](https://arxiv.org/abs/2607.06195) — agentic oracles

Full survey with architecture breakdowns and ablation figures:
[`docs/literature_survey.md`](docs/literature_survey.md).

---

## Stack

Python 3.12 · pytest 9.1 · mutmut 3.6 · coverage 7.15 · Gemini
(`gemini-3.6-flash`) via `google-genai`, with schema-constrained structured
outputs.
