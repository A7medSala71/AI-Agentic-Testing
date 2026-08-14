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

## 3a. Doctest policy — decided

**Doctests are stripped from every prompt.** Approved by Prof. Doaa in Week 3;
`config.INCLUDE_DOCTESTS = false`.

Every dataset function carries worked input→output examples in its docstring:

```python
def arc_length(angle: int, radius: int) -> float:
    """
    >>> arc_length(45, 5)
    3.9269908169872414
    """
    return 2 * pi * radius * (angle / 360)
```

Left in, a model can transcribe `assert arc_length(45, 5) == 3.9269908169872414`
without reasoning about the function at all. Two consequences:

1. **It measures the wrong thing.** Oracle correctness is what RQ2 asks about; transcription is not oracle reasoning.
2. **It starves the refinement loop.** Steps 3–5 of the pipeline operate on *surviving* mutants. Near-perfect initial suites leave none, so Variant 1 and Variant 2 have nothing to differentiate them — the added RQ becomes unanswerable.

### The comparability argument

The decisive point is that **CANDOR's benchmark has no worked examples**, so
stripping ours matches the system we compare against rather than diverging from
it:

| | worked examples in the prompt? |
|---|---|
| HumanEval (original Python) | yes — `>>>` blocks in the docstring |
| **HumanEvalJava — what CANDOR uses** | **no** — the Java translation drops the Javadoc entirely |
| CANDOR's stated input | source code + a prose natural-language description |
| **Our dataset (30 Python functions)** | **yes** — inherited from its source repository |

Our dataset differs from CANDOR's in exactly this respect, by accident of where
it came from. This belongs in the paper's methodology section rather than being
left implicit.

### Ablation considered and set aside

Treating the condition as an experimental parameter — running every system both
with and without doctests — was proposed and declined on cost grounds: it
doubles the experiment (~1,260 → ~2,520 calls), and
`schema/execution_log_schema.json` has no field recording which condition
produced a record, so the two would be indistinguishable in `logs/`.

`config.INCLUDE_DOCTESTS` remains configurable and `prompt_context.build_context()`
takes the flag per call, so the ablation is available if it is ever revisited —
but a schema field must be added first.

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

- **`evaluation/` does not run** — Member 2. `score.py` unblocks Baseline validation locally, but the paper's numbers must come from the shared pipeline.

## 8. Next, in order

1. Baseline B live on `function_03` — generation quality + panel-disagreement rate.
2. Both systems on 5–10 functions, scored — the first honest A vs B comparison.
3. Full scale: 30 functions × 3 repeats, once billing is confirmed.

---

## 9. Results — Baseline A vs Baseline B

Complete: 30 functions × 3 repeats × 2 systems = **180 runs**. Generated with
`gemini-3.5-flash-lite`, doctests stripped. Scored with `baselines/score.py`,
compared with `baselines/compare.py`.

| | runs | mutation score | line coverage |
|---|---|---|---|
| Baseline A | 90/90 | 94.5% ± 6.9 | 73.7% |
| Baseline B | 90/90 | 95.1% ± 5.7 | 73.0% |

Paired across all 30 functions, averaging the 3 repeats per function first:

```
difference        +0.6 points
Baseline B better  9 functions
Baseline A better  4 functions
tied              17 functions

Wilcoxon signed-rank (two-sided)
  non-zero differences  13 of 30
  W                     28.0
  p                     0.2213   -- not significant
```

### Why the panel does not help — measured, not assumed

Baseline B spends five times the calls for +0.6 points. The obvious question is
whether the panel is failing to resolve conflicts, or whether there are no
conflicts to resolve. `baselines/measure_panel.py` answers it directly:

| | panel disagreement |
|---|---|
| **CANDOR (reported)** | **> 70%** |
| **This project (measured, 12 functions)** | **1.4% mean, 0.0% median** |

**The three panelists were fully unanimous on 11 of 12 functions.** They are not
disagreeing and being badly merged — they simply agree. Consensus has nothing to
resolve, so the four extra calls buy almost nothing.

That is the sentence that explains the headline result. Without it, "+0.6 points,
p = 0.22" reads as an inconclusive experiment rather than a mechanism that has
been measured and understood.

Why the gap from CANDOR is plausible: their subjects are Java methods with a
separate natural-language specification, judged by a reasoning model that
produces long deliberations. Ours are short, self-contained Python functions
whose correct behaviour is largely unambiguous from the source, judged by a
small fast model. There is less for reasonable reviewers to disagree about.

### Reading this

**This is a result, not a failure.** RQ1 asks whether *mutation-guided
iteration* beats consensus alone; a Baseline B that had leapt ahead would have
undercut the premise of the refinement loop before Member 4 ran an experiment.
What this establishes is the floor the proposed variants have to clear:

```
single-shot generation      94.5%
+ 3-panelist consensus      95.1%   (+0.6, 5x the cost, p = 0.22)
+ mutation-guided loop         ?    <- Variants 1 and 2
```

**Report the tie rate and the disagreement rate alongside the p-value.** A
significance test cannot find a difference that mostly is not there, and the
p-value alone invites the reading that the study was underpowered rather than
that the systems genuinely match.

### Headroom for the refinement loop

Baseline A already kills every mutant on **13 of 30** functions, leaving the
refinement variants nothing to improve there. The other **17** have surviving
mutants, and those are where RQ1 and RQ4 can be answered at all. The richest:

| function | Baseline A mutation score |
|---|---|
| `function_11` | 74.1% |
| `function_19` | 76.8% |
| `function_04` | 85.7% |
| `function_12` | 87.7% |
| `function_21` (`binary_search`) | 89.5% |

This is also the argument against moving to a stronger model for the main
experiment: a model that kills more mutants leaves less for the loop to
demonstrate.

### Caveats

- `function_18` cannot be imported at all (see the integration note) and scores 0 for every system. It depresses both equally and should be excluded once Member 1 rules on it.
- These figures come from `score.py`, Member 3's local harness. The paper's numbers should come from Member 2's shared pipeline so all four systems are scored identically.
- Cost figures written before this pass used standard-Flash pricing rather than Flash-Lite, overstating spend by roughly 25%. Fixed in `config.py`, and the token breakdown is now stored per run so a price correction never again requires re-running anything.
