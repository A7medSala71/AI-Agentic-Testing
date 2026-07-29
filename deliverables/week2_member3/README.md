# Week 2 Deliverables — Member 3 (Baseline Systems Lead)

| | |
|---|---|
| **Project** | Agentic Testing — Team 1: Oracle-Quality Test Generation |
| **Supervisor** | Prof. Doaa Shawky |
| **Week 2 scope per brief** | design Baseline A + Baseline B prompts and architecture |
| **Status** | designed **and implemented**. Baseline A verified live; Baseline B verified in mock mode, live run pending API quota. |

---

## Contents

| File | What it is |
|---|---|
| `01_baseline_design.docx` / `.md` | Design and justification for both systems |
| `02_integration_note_member2.md` | Handover note to Member 2: file format, working mutmut recipe, timeline |
| `code/` | Both baselines plus supporting infrastructure |
| `sample_output/` | A real generated test suite (Baseline A, `function_03`) |
| `evidence/` | Captured output of every verification run |

---

## What was delivered

Week 2 asked for a design. Both systems were **built and verified** as well, putting
the Week 3 deliverable (build v0.1, test on toy files) largely complete.

**Baseline A** — single-shot generation, 1 LLM call per function.

**Baseline B** — one-shot multi-agent consensus, 5 calls per function:

```
       propose (1 call)
          |
          +--> panelist 1 --+
          +--> panelist 2 --+--> curator (1 call) --> final suite
          +--> panelist 3 --+
               (3 calls, independent)
```

A simplified CANDOR (arXiv:2506.02943): panel size 3 (their ablation shows no
significant gain past 3), Interpreter agents collapsed into structured output
(8 calls → 5), single-pass by design so RQ1's comparator does not iterate.

---

## Measured results

**Baseline A, live, `function_03`** — 1 call, 2,532 tokens ($0.0069), 8 tests:

| tests passing | line coverage | mutation score |
|---|---|---|
| 8/8 (100%) | 80.0% | **100.0%** (6/6) |

All eight oracles are mathematically correct, imports are explicit, floats use
`pytest.approx`. The generated suite is in `sample_output/`.

**Architecture, mock mode, all 30 functions** — Baseline A made exactly 30
calls, Baseline B exactly 150. Call counts of 1× and 5× the function count
confirm the architecture matches the design.

---

## Three prompt rules, each forced by a Week 1 measurement

These must apply to Baseline A, Baseline B **and Member 4's variants**. A
system that omits them scores badly for reasons unrelated to its design, which
would silently invalidate RQ1.

| Rule | Evidence |
|---|---|
| State the module name in the prompt | pass rate **0% → 80%** |
| Explicit named imports only | `import *` turns 1 test into 3 collected |
| `pytest.approx` for floats | most of this dataset returns floats |

---

## Infrastructure added

- **`runner.py`** — wires generate → score → log, and **resumes**: any run already logged is skipped. Week 4 is 540 calls over hours; a crash at run 78 must not mean starting over.
- **`score.py`** — local scoring (coverage + mutmut) so the baselines could be validated while `evaluation/` is unavailable. **Not a replacement** — the paper's numbers must come from the shared pipeline so all four systems are scored identically.
- **Rate-limit handling** — a 429 carries the server's own `retryDelay`; the client parses and honours it rather than guessing a fixed backoff. Baseline B fires 5 calls back to back and paid tiers have per-minute caps, so this matters beyond the free tier.

---

## Blocked

**API quota.** Billing is being enabled; until it is active the free tier caps
at ~20 calls/day. A 429 named the quota explicitly
(`GenerateRequestsPerDayPerProjectPerModel-FreeTier`, limit 20), which is how
we know billing has not taken effect yet.

Baseline A needs only **1 call per function**, so all 30 functions are
deliverable in about two days even on the free tier. Baseline B needs 5 per
function.

**Decisions outstanding** — carried over from Week 1, all still needed before
results are generated:

1. Doctest policy (currently stripped) — changing it later invalidates every prior run
2. Three schema fields missing for brief §3.5 metrics (`num_llm_calls`, `pass_rate_pct`, `branch_coverage_pct`)
3. Equivalent-mutant handling — needs an owner
4. Baseline B must be described in the paper as a consensus-only *ablation* of CANDOR, not a reimplementation

---

## Reproducing

```bash
.venv/bin/python -m baselines.baseline_a function_03 --mock   # no API key needed
.venv/bin/python -m baselines.baseline_b function_03 --mock
.venv/bin/python -m baselines.score                           # score real output
```

`code/` is a snapshot for review. The working copy is `baselines/` at the
repository root.
