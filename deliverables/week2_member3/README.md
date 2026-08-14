# Week 2 Deliverables — Member 3 (Baseline Systems Lead)

| | |
|---|---|
| **Project** | Agentic Testing — Team 1: Oracle-Quality Test Generation |
| **Supervisor** | Prof. Doaa Shawky |
| **Week 2 scope per brief** | design Baseline A + Baseline B prompts and architecture |
| **Status** | **complete** — 180 runs generated, scored and logged across all 30 functions |

---

## Contents

| File | What it is |
|---|---|
| `01_baseline_design.docx` / `.md` | Design and justification for both systems |
| `02_integration_note_member2.md` | Integration note: file format, working mutmut recipe |
| `03_handover_to_member2.md` | **Handover — everything Member 2 needs to take over scoring** |
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

## Results

**180 runs complete** — 30 functions x 3 repeats x 2 systems.

| | runs | mutation score | line coverage |
|---|---|---|---|
| Baseline A | 90/90 | 94.5% +/- 6.9 | 73.7% |
| Baseline B | 90/90 | 95.1% +/- 5.7 | 73.0% |

Paired across all 30 functions:

```
difference   +0.6 points
tied         17 of 30 functions
Wilcoxon     W = 28.0, p = 0.2213  -- not significant
```

### Why the panel does not help — measured

| | panel disagreement |
|---|---|
| CANDOR (reported) | > 70% |
| **This project (measured)** | **1.4% mean, 0.0% median** |

The three panelists were **fully unanimous on 11 of 12 functions**. They are not
disagreeing and being badly merged -- they simply agree, so consensus has
nothing to resolve and the four extra calls buy almost nothing.

That is the sentence that explains the headline result. Without it, "+0.6
points, p = 0.22" reads as an inconclusive experiment rather than a mechanism
that has been measured.

**This is a result, not a failure.** RQ1 asks whether mutation-guided iteration
beats consensus alone. A Baseline B that had leapt ahead would have undercut the
premise of the refinement loop before Member 4 ran an experiment. What this
establishes is the floor the variants must clear:

```
single-shot generation      94.5%
+ 3-panelist consensus      95.1%   (+0.6, 5x the cost, p = 0.22)
+ mutation-guided loop         ?    <- Variants 1 and 2
```

### Headroom for the refinement loop

Baseline A already kills every mutant on **13 of 30** functions. The other **17**
have surviving mutants, and those are where RQ1 and RQ4 can be answered at all.
The richest are `function_11` (74.1%), `function_19` (76.8%) and `function_04`
(85.7%).

This is also the argument against a stronger model for the main experiment: one
that kills more mutants leaves less for the loop to demonstrate.

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

**Doctest policy — decided.** Prof. Doaa approved stripping doctests from every
prompt (Week 3). The decisive argument was comparability: CANDOR's benchmark
carries no worked examples, so stripping ours matches the system we compare
against. See `01_baseline_design.md` §3a.

**Still outstanding:**

1. Three schema fields missing for brief §3.5 metrics (`num_llm_calls`, `pass_rate_pct`, `branch_coverage_pct`)
2. Equivalent-mutant handling — needs an owner
3. Baseline B must be described in the paper as a consensus-only *ablation* of CANDOR, not a reimplementation

---

## Reproducing

```bash
.venv/bin/python -m baselines.baseline_a function_03 --mock   # no API key needed
.venv/bin/python -m baselines.baseline_b function_03 --mock
.venv/bin/python -m baselines.score                           # score real output
```

`code/` is a snapshot for review. The working copy is `baselines/` at the
repository root.
