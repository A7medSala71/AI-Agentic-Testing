# Literature Survey — Member 3 (Baseline Systems Lead)

Week 1 deliverable. Covers every reading section of brief §1 that applies to
Member 3, read with a Baseline A / Baseline B lens:

| Brief section | Marked | Covered below |
|---|---|---|
| §1.1 Mutation testing fundamentals | essential for all | §A |
| §1.2 Python `ast` & pytest | **essential for Members 3 & 4** | §B |
| §1.3 LLM structured outputs | **essential for Members 3 & 4** | §C |
| §1.4 Prior work | required for all | §1–§3 |
| §1.5 Wilcoxon signed-rank | essential for Member 4 | out of scope, noted in §D |

---

## 1. CANDOR — the paper Baseline B is derived from

> **Hallucination to Consensus: Multi-Agent LLMs for End-to-End JUnit Test Generation**
> Qinghua Xu, Guancheng Wang, Lionel Briand, Kui Liu — [arXiv:2506.02943](https://arxiv.org/abs/2506.02943)

### Problem

LLMs write plausible test *prefixes* but hallucinate the **oracle** — the
assertion. A wrong oracle either fails on correct code (noise) or passes on
broken code (a **weak oracle**, exactly what our RQ2 targets).

The authors' bet: hallucinations are *inconsistent*, so consensus across
several models filters them out.

### Architecture — 9 agents, 3 steps

**Step I — Initialization**

- *Initializer* — basic LLM writes test file v0.
- *Validation* — compiles/runs, feeds errors back until v1 is syntactically valid.

**Step II — Test Prefix Generation** (iterative, coverage-driven)

- *Planner* — reads the Jacoco report, proposes new cases as JSON `{name, description, input, expected_output}`.
- *Tester* — renders each plan to code: `{test_name, test_code, new_import_statements}`.
- *Inspector* — classifies failures, returns `{failed_test_code, error_message, error_type, potential_fix}`.

**Step III — Oracle Fixing** (the part Baseline B reproduces)

- *Requirement Engineer* — extracts NL requirements + a predicate-logic spec.
- *Panelist ×3* — reasoning LLMs independently judge each oracle.
- *Interpreter ×3* — basic LLMs compressing each Panelist's output into `{oracle_correct, reasoning, confidence}`.
- *Curator* — merges the three verdicts into the final oracle.

### How the consensus actually works

The three Panelist+Interpreter pipelines run **in parallel, once**. There are
**no debate rounds** — panelists never see each other's opinions. The
"discussion" happens entirely inside the Curator, which cross-checks the
reasoning, inputs and outputs of each panelist rather than taking a vote.

Two numbers that shaped our Baseline B design:

- **Over 70% of cases contained clear panelist disagreement** — the Curator is doing real work.
- But **majority voting instead of the Curator costs only −0.014** oracle correctness, while **removing the panel entirely costs −0.086**. Having three independent opinions is what matters; the merge strategy is second-order.

### The dual-LLM trick — and why we drop it

DeepSeek R1 emitted outputs **over 10,000 tokens**, taking hours per file, full
of self-doubt loops. The fix was truncating panelists to **2,000 tokens** and
adding a cheap Interpreter to extract the signal.

This is an engineering workaround for a specific 2025 open-weight model, not a
scientific contribution. With native structured outputs our panelist returns
`{oracle_correct, reason, confidence}` directly, so **the Interpreter agents
are removed** — taking Baseline B from 8 calls to **5**, which matters for the
budget-comparability requirement in brief §3.3.

### Setup

Llama 3.1 70B (basic) + DeepSeek R1 distilled 70B (reasoning); **panel size 3**
(1–5 tested, no significant gain past 3); HumanEvalJava (160 programs) and
LeetCodeJava (100); baselines EvoSuite, LLM-Empirical, TOGLL; Wilcoxon
signed-rank + Vargha-Delaney A₁₂, 3 repetitions; Python + LangChain.

Our project mirrors this closely — same statistical test, same 3 repeats,
mutation score as headline metric.

### What CANDOR actually shows the model — checked, because it decided our prompt policy

CANDOR states it supplies two things per subject: *"the source code and its
natural language description"*. The description is prose — input types and
expected behaviour, which the Requirement Engineer turns into predicate logic.
**No worked input→output examples.**

This is worth verifying rather than assuming, because HumanEval's *original
Python* docstrings do carry `>>>` examples. The Java translation drops them: the
methods in [ASSERT-KTH/human-eval-java](https://github.com/ASSERT-KTH/human-eval-java)
carry no Javadoc at all.

| | worked examples in the prompt? |
|---|---|
| HumanEval (original Python) | yes |
| **HumanEvalJava — what CANDOR uses** | **no** |
| **Our dataset (30 Python functions)** | **yes**, inherited from its source repo |

Our dataset therefore differs from CANDOR's in exactly this respect, by accident
of where it came from. That is why doctests are stripped from every prompt in
this project — see `week2_baseline_design.md` §3a.

### Results

| Metric | Dataset | CANDOR | EvoSuite | LLM-Empirical |
|---|---|---|---|---|
| Line coverage | HumanEvalJava | 0.991 | 0.961 | 0.704 |
| Branch coverage | HumanEvalJava | 0.950 | 0.942 | 0.688 |
| **Mutation score** | HumanEvalJava | **0.980** | 0.858 | 0.823 |
| **Mutation score** | LeetCode-Medium | **0.939** | 0.845 | 0.868 |
| **Mutation score** | LeetCode-Hard | **0.937** | 0.888 | 0.778 |

**Coverage merely ties EvoSuite; mutation score beats it by 5–12 points.**
That gap *is* the weak-oracle phenomenon — same lines executed, far more faults
caught. This framing underpins our entire project.

Oracle correctness ≈ 0.91 vs ≈ 0.44 (LLM-Empirical), beating fine-tuned TOGLL
by **at least 21.1 points**; A₁₂ = 0.920 (correct code) / 0.960 (faulty code).

**Ablations:**

| Removed | Effect |
|---|---|
| Planner | line −0.099, branch −0.130, mutation −0.111 |
| Requirement Engineer | oracle correctness −0.028 |
| **Panel discussion** | **oracle correctness −0.086** |
| Curator → majority voting | oracle correctness −0.014 |

### Limitations

Never tested on real bugs at Defects4J scale (mutation score is a *proxy*);
only methods without external class dependencies; only two benchmarks; model
choice not exhaustively compared.

---

## 2. Mutation-Guided LLM-based Test Generation at Meta

> Foster, Gulati, Harman, Harper, Mao, Ritchey, Robert, Sengupta — [arXiv:2501.12862](https://arxiv.org/pdf/2501.12862)

Meta's production system **ACH**. The key inversion: rather than generating
*many* mutants and hoping some are useful, it generates **few targeted mutants
representing faults specific to a concern** (their example: privacy), then asks
an LLM to write tests killing those.

**Scale:** 10,795 Android Kotlin classes across 7 platforms → 9,095 mutants →
571 privacy tests. **73% of generated tests accepted by engineers**; 36% of
accepted ones judged privacy-relevant.

### The part that matters for our team: equivalent mutants

ACH includes an **equivalent-mutant detector**. Equivalent mutants change the
code but not its behaviour — they are *impossible* to kill, so they silently
depress every mutation score. Raw LLM detection: precision 0.79 / recall 0.47.
With preprocessing: **0.95 / 0.96**.

**Risk to our project.** If our 30 functions produce equivalent mutants, both
baselines *and* the proposed variants are penalised on mutants nobody could
ever kill, and Member 4's refinement loop can burn its entire 5-iteration
budget chasing one. Flagged to Members 2 and 4.

---

## 3. LogicHunter: Testing LLM Agent Frameworks with an Agentic Oracle

> Minghui Long, Yanjie Zhao, Haoyu Wang — [arXiv:2607.06195](https://arxiv.org/abs/2607.06195)

Different domain (testing LangChain / LlamaIndex / CrewAI themselves), included
for one idea: the **Agentic Oracle**. Instead of *passively classifying*
whether output looks right, it *actively investigates* — retrieving docs,
navigating source, inspecting runtime state — via a ReAct architecture with
dual-layer state management and dual-stream memory.

**Headline: 91.17% precision vs 29.27% for the best passive approach — a
61-point gap.** Found 40 unknown bugs (30 confirmed, 26 fixed) where SOTA
baselines found zero.

**Relevance to Baseline B.** Design inspiration for Member 4's variants, not
for our baselines. But the active-vs-passive distinction is a useful lens:
our panelists are deliberately **passive** judges — they see code plus
requirements and opine, without investigating runtime state. That is what keeps
Baseline B a clean non-investigating comparator. Worth one sentence in Related
Work.

---

## A. Mutation testing fundamentals (brief §1.1)

> [mutmut docs](https://mutmut.readthedocs.io/en/latest/index.html) ·
> [Codecov walkthrough](https://about.codecov.io/blog/getting-started-with-mutation-testing-in-python-with-mutmut/)

The published docs are thin — they list only a few example mutations and never
define "killed", "survived", or the mutation score. Everything below was
therefore **verified directly against mutmut 3.6.0 on our own dataset**, which
is stronger evidence anyway. Reproduce with
`.venv/bin/python -m baselines.toolchain_check`.

### How a mutant is generated

mutmut rewrites the source into a family of near-identical variants, one
mutation each. On `function_03`'s single line
`return 2 * pi * radius * (angle / 360)` it produced exactly six:

| Mutant | Result | Operator class |
|---|---|---|
| `__mutmut_1` | `2 * pi * radius / (angle / 360)` | arithmetic operator |
| `__mutmut_2` | `2 * pi / radius * (angle / 360)` | arithmetic operator |
| `__mutmut_3` | `2 / pi * radius * (angle / 360)` | arithmetic operator |
| `__mutmut_4` | `3 * pi * radius * (angle / 360)` | integer literal +1 |
| `__mutmut_5` | `2 * pi * radius * (angle * 360)` | arithmetic operator |
| `__mutmut_6` | `2 * pi * radius * (angle / 361)` | integer literal +1 |

On `function_21` (`binary_search`, which has conditionals) mutmut produced
**19** mutants, and comparison operators appear that cannot exist in
`function_03`: `==` → `!=`, `<` → `<=`, `len(a_list) == 0` → `== 1`.

**Consequence for RQ4.** The mutant-operator mix is a function of the code
under test, not a knob. Pure-arithmetic functions yield only arithmetic and
literal mutants; only functions with branching produce conditional-boundary
mutants. RQ4 asks whether refinement helps different operator classes
differently — that question is only answerable if the 30 functions span both
shapes. Worth checking with Member 1 before RQ4 is committed to.

### Killed vs survived

A mutant is **killed** when the test suite fails against it, and **survives**
when the suite still passes. mutmut records this per mutant in
`mutants/<file>.py.meta` under `exit_code_by_key`: a non-zero exit code means
the suite failed, i.e. killed.

```
mutation score = killed / total mutants
```

A surviving mutant means the code changed behaviour and **no assertion
noticed** — a weak oracle. That is precisely the signal Member 4's refinement
loop feeds back, and precisely what RQ2 counts.

### Configuration

mutmut 3.6 refuses to do anything — even `--help` raises `FileNotFoundError` —
without a `[mutmut]` section:

```ini
[mutmut]
source_paths=function_03.py
pytest_add_cli_args_test_selection=tests/
```

mutmut 3.x renamed its keys: `paths_to_mutate` → `source_paths`,
`tests_dir` → `pytest_add_cli_args_test_selection`. The old names still parse
but emit deprecation warnings.

### Equivalent mutants

The docs do not address them at all. An equivalent mutant changes the source
without changing behaviour, so **no test can ever kill it** and it permanently
depresses the mutation score. Meta's ACH paper (§2 above) had to build a
dedicated detector. Untreated, these penalise every system in our comparison
and can consume Member 4's whole 5-iteration budget chasing an unkillable
target. Flagged to Members 2 and 4.

---

## B. Python `ast` and pytest (brief §1.2 — essential for Member 3)

> [`ast` docs](https://docs.python.org/3/library/ast.html) ·
> [pytest docs](https://docs.pytest.org/en/stable/getting-started.html)

### `ast` — used to control what the model sees

`baselines/prompt_context.py` builds the prompt from the parse tree rather than
from raw text, because both policy decisions we need are structural, not
textual. The four APIs that matter:

| API | Use here |
|---|---|
| `ast.parse(src)` | Source → tree. |
| `ast.NodeTransformer` | Subclass and `visit_FunctionDef` to drop or rewrite nodes. |
| `ast.get_docstring(node)` | Reach a docstring without guessing at string positions. |
| `ast.unparse(tree)` | Tree → source, after edits. Python 3.9+. |

Two structural edits are applied before any prompt is built: the
`if __name__ == "__main__":` block is removed (not under test), and doctest
`>>>` blocks are stripped from docstrings when `INCLUDE_DOCTESTS=false`.
Doing this on the tree rather than with regex is what makes it safe — a `>>>`
inside a normal string is untouched.

`ast` is also the natural tool for Member 4's variants if they need to locate
the assertion that failed to catch a mutant.

### pytest — what generated tests must satisfy

- **Plain `assert`.** pytest rewrites assertions to produce readable failures; no `assertEqual` needed. Generated tests should use bare `assert`.
- **`pytest.approx`.** Essential for this dataset — `arc_length`, `radians`, `sin`, `mean` all return floats. An exact `==` on a float is a flaky oracle. The prompts must require `approx` for float comparisons.
- **`pytest.raises`.** Several functions raise deliberately (`perfect_cube_binary_search` raises `TypeError` on a non-int). Error paths are testable behaviour and mutants hide there.
- **`@pytest.mark.parametrize`.** Compact way to cover many inputs. Note for metrics: parametrize expands to one test *per case*, which changes the denominator of any pass-rate calculation.
- **Exit codes.** `0` = all passed, `1` = tests failed. This is the mechanism the whole project rests on: mutation testing is just "did the exit code become non-zero when the source was mutated".

**Collection gotcha — verified.** `function_25.py` ships its own
`class Test(unittest.TestCase)` containing `test_primes` and `test_not_primes`.
Because `function_25.py` does not match the `test_*.py` file pattern, pytest
ignores it normally. But if a generated test file uses a wildcard import, that
class is pulled into the test module's namespace and pytest collects its
methods:

```
from function_25 import is_prime   ->  1 test collected
from function_25 import *          ->  3 tests collected
                                       (Test::test_primes, Test::test_not_primes, test_small)
```

Two of those three "tests" came from the dataset, not from the model. Left
unhandled this inflates the test count and corrupts the pass rate for
`function_25` — and it would look like the model wrote passing tests it never
wrote. **Mitigation:** the prompt and the `GeneratedTestSuite.imports` contract
must require explicit named imports; wildcard imports are rejected at render
time. Applies to every system, so it is worth stating in the paper's threats to
validity.

---

## C. LLM structured outputs (brief §1.3 — essential for Member 3)

> [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output)

### Why this is the single most important setup item for this role

The full procedure is 30 functions × 3 systems × 3 repeats, and Baseline B
makes 5 calls per function. That is several hundred unattended calls whose
output has to become a runnable `.py` file with no human in the loop. If the
model returns prose with a fenced code block some of the time, the harness
breaks overnight and the run is lost. Constraining generation to a schema
removes that entire failure class: the response is a validated object, not text
to be scraped.

### How it works in practice

```python
config=types.GenerateContentConfig(
    system_instruction=system_prompt,
    response_mime_type="application/json",
    response_schema=GeneratedTestSuite,   # a pydantic model
)
...
suite = response.parsed        # already a GeneratedTestSuite instance
```

Verified against google-genai 2.14.0: `response_schema` accepts a pydantic
model directly, and `response.parsed` is populated with a validated instance.
Our contracts live in `baselines/schemas.py`.

### Two findings from setting this up

**1. Reasoning tokens are billed and must be counted.** Gemini 3.x models emit
thinking tokens, exposed as `usage_metadata.thoughts_token_count` separately
from `candidates_token_count`. Counting only prompt + candidates understates
both cost and the budget figures RQ1 depends on. `UsageTracker` records it as
its own field and bills it at the output rate.

**2. Structured output replaces one of CANDOR's agents.** CANDOR needed three
"Interpreter" agents purely to compress a reasoning model's rambling output
into `{oracle_correct, reasoning, confidence}`. A schema-constrained panelist
returns those fields directly, which is why Baseline B is **5 calls, not 8**.
This is a design simplification the paper should state explicitly.

**Caveat the brief raises.** Brief §4 warns that Gemini has "less consistent
structured-output reliability in practice — may need extra prompt engineering".
Not yet testable: everything so far ran in mock mode. **First live-API task is
to measure schema-conformance rate over ~20 real calls** before committing to
the model for full-scale runs.

---

## D. Note on brief §1.5 (Wilcoxon signed-rank)

Marked *essential for Member 4*, who owns the statistical comparison. Not
surveyed here. One point does reach back into Baseline design: the test is
**paired**, comparing systems function by function on the same 30 functions.
That only works if every system is run on an identical function set under an
identical prompt policy — which is why the doctest policy and the unit-of-
testing decision (see `week1_member3_report.md` §4) have to be settled once and
applied to all systems, not chosen per system.
