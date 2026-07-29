# Week 2 Design — Baseline A and Baseline B (Member 3)

**Scope per brief:** design Baseline A + Baseline B prompts and architecture.
**Status:** designed and implemented. Verified in mock mode across all 30
functions; live verification pending quota reset (Week 1 report §6.5).

---

## 1. Baseline A — single-shot

One prompt, one round, no feedback. The floor RQ1 measures against.

```
function source  ->  1 LLM call  ->  pytest suite
```

`baselines/baseline_a.py`, prompt in `baselines/prompts.py`.

**Cost:** 1 call per function. 30 functions × 3 repeats = **90 calls**.

---

## 2. Baseline B — one-shot multi-agent consensus

```
       propose (1 call)
          |
          +--> panelist 1 --+
          +--> panelist 2 --+--> curator (1 call) --> final suite
          +--> panelist 3 --+
               (3 calls, independent)
```

`baselines/baseline_b.py`.

**Cost:** 5 calls per function. 30 × 3 repeats = **450 calls**.

### Mapping to CANDOR

| Baseline B stage | CANDOR agent | Kept? |
|---|---|---|
| propose | Initializer | yes |
| — | Requirement Engineer | dropped, worth only −0.028 in their ablation |
| critique ×3 | Panelist ×3 | yes |
| — | Interpreter ×3 | **collapsed into structured output** |
| finalise | Curator | yes |
| — | Planner / Tester / Inspector (Step II) | dropped — iterative, forbidden here |

### Design decisions

**Panel size 3.** CANDOR tested 1–5 and reported no significant gain past 3.
Configurable via `config.PANEL_SIZE` and `--panel`, but 3 is the default and
should not be re-litigated without a reason.

**No Interpreter agents.** CANDOR ran a second cheap LLM after each panelist
purely to compress DeepSeek R1's 10k-token reasoning into
`{oracle_correct, reasoning, confidence}`. Schema-constrained output returns
those fields directly. This takes Baseline B from CANDOR's 8 calls to **5** —
material for the budget-comparability requirement in brief §3.3. The paper
should state this as a deliberate simplification, not omit it.

**The curator reasons, it does not vote.** CANDOR reports panelist disagreement
in over 70% of cases, and their ablation puts majority voting at −0.014 oracle
correctness versus −0.086 for dropping the panel entirely. The panel existing
matters more than the merge strategy, but the curator is implemented as a
reasoning merge as in the paper.

**Panelists are blind to each other.** No debate rounds, as in CANDOR. The
"panel discussion" happens inside the curator.

**Single pass, by design.** CANDOR's Step II is an iterative *coverage* loop
worth −0.111 mutation score in their ablation. RQ1 asks whether
mutation-guided iteration beats consensus alone, so the comparator must not
iterate. **Baseline B is therefore a consensus-only ablation of CANDOR, not a
reimplementation** — the paper must say so plainly and cite the −0.111 figure,
or a reviewer will read it as a straw man.

### Instrumentation

`panel_disagreement()` records the share of tests the panel did not
unanimously agree on. CANDOR reports over 70%. If our figure comes back near
zero, Baseline B is spending 5 calls to buy nothing — which is itself a
finding worth reporting, and better discovered now than in Week 5.

---

## 3. Prompt rules — three non-negotiables

All three were forced by Week 1 measurements, and all three must apply to
Baseline A, Baseline B **and Member 4's variants**. A system that omits them
scores badly for reasons unrelated to its design, which would silently
invalidate RQ1.

| Rule | Why | Evidence |
|---|---|---|
| **State the module name** | The model sees source, never a filename; left to guess it invents `solution`, `arc_length_module` | pass rate **0% → 80%** |
| **Explicit named imports only** | `from function_25 import *` makes pytest collect that file's own unittest class as if the model wrote it | 1 test becomes 3 |
| **`pytest.approx` for floats** | Most of this dataset returns floats; exact `==` is a flaky oracle | — |

Prompts also tell the model its tests will be mutation-scored, and that a test
which executes a line without checking the result detects nothing. That is the
weak-oracle failure mode RQ2 measures, stated directly in the prompt.

---

## 4. Unit of testing — decided

**All public functions per file.** 17 of 30 files hold more than one
(`function_01` has `slow_primes`, `primes`, `fast_primes`).

Rationale: mutmut mutates the whole file. Testing only one function would leave
every other function's mutants alive, depressing the mutation score for reasons
unrelated to oracle quality — and it would do so unevenly, since only 17 of 30
files are affected.

Non-testable scaffolding (`benchmark`, `main`, `if __name__ == "__main__"`) is
stripped by `prompt_context.py` and excluded from the target list.

---

## 5. Call budget vs brief §3.3

| System | Calls/run | ×30 functions ×3 repeats |
|---|---|---|
| Baseline A | 1 | 90 |
| Baseline B | 5 | 450 |
| Variant 1 (ErrorTrace) | ~4 | ~360 |
| Variant 2 (StatePrediction) | ~4 | ~360 |

Baseline B at 5 calls sits in the same band as the proposed variants, which is
what §3.3 asks for. Baseline A at 1 call is deliberately far below — that is
what single-shot generation *is*, and the brief frames it as reproducing
current practice rather than as a budget-matched competitor. Worth one sentence
in the paper so the asymmetry reads as intentional.

---

## 6. Verified

### Mock mode — architecture

All 30 functions, both systems:

```
Baseline A: 30 calls, 30 files generated, no failures
Baseline B: 150 calls, 30 files generated, no failures
```

Call counts are exactly 1× and 5× the function count, confirming the
architecture matches the design.

### Live — Baseline A on `function_03`

First real run. 1 call, 2,532 tokens ($0.0069), 8 tests generated. Scored with
`baselines/score.py`:

| | tests passing | line coverage | mutation score |
|---|---|---|---|
| Baseline A | 8/8 (100%) | 80.0% | **100.0%** (6/6) |

All eight oracles are mathematically correct (verified by hand), imports are
explicit and correctly named, and floats use `pytest.approx`. **All three
prompt rules held on the first live run.**

**Baseline B not yet run live** — the free-tier quota ran out mid-run. Nothing
about its architecture is in doubt (150 mock calls, exact call counts), but its
generation quality and panel-disagreement rate are unmeasured.

### Local scoring

`baselines/score.py` runs coverage + mutmut on a generated suite and reports
pass rate, line coverage, and mutation score. It exists so the baselines can be
validated without waiting on `evaluation/`, which currently does not run. **It
is not a replacement** — final reported numbers must come from Member 2's
shared pipeline so all four systems are scored identically.

### Rate-limit handling

Baseline B issues 5 calls back to back, and Week 4 is hundreds in sequence, so
429s are routine rather than exceptional — paid tiers have per-minute caps too.
A 429 response carries the server's own `retryDelay`; `LLMClient` parses it and
waits that long rather than guessing a fixed backoff, capped at
`MAX_RETRIES` attempts and `MAX_RETRY_DELAY_SECONDS` each. Verified against
real 429 bodies captured from the API.

A daily-quota 429 is not recoverable by waiting, so the error is re-raised
after the cap rather than looped on.

---

## 7. Still blocked

**Billing not yet active.** A 429 during the live run named the quota
explicitly:

```
metric:  generativelanguage.googleapis.com/generate_content_free_tier_requests
quotaId: GenerateRequestsPerDayPerProjectPerModel-FreeTier
limit:   20
```

The `FreeTier` quota ID is the diagnostic — once billing is enabled on the
project the API key belongs to, that identifier changes. Until then everything
past ~20 calls/day is blocked, against a ~1,260-call requirement.

Also outstanding:

- **Doctest policy** (`config.INCLUDE_DOCTESTS`, currently `false`) — needs sign-off before results are generated, since changing it invalidates every prior run.
- **`evaluation/` does not run** — Member 2. `score.py` unblocks Baseline validation locally, but the paper's numbers must come from the shared pipeline.

## 8. Next, in order

1. Baseline B live on `function_03` — generation quality + panel-disagreement rate.
2. Both systems on 5–10 functions, scored — the first honest A vs B comparison.
3. Full scale: 30 functions × 3 repeats, once billing is confirmed.
