# refinement_loop/ — Member 4 (Proposed Pipeline & Evaluation Lead)

Design of the mutant-guided iterative refinement loop for **Agentic Testing —
Team 1: Oracle-Quality Test Generation**, and specifically the piece Week 2
asked for: **how surviving mutants map back to a regeneration prompt.**

This is not the full pipeline (that's Week 3–4). It is the architecture,
implemented against fakes/stubs so it's fully testable and demonstrable
before Member 2's real `mutmut` pipeline and a live LLM API are wired in.

## Why two variants?

`execution_log_schema.json` (Member 1's shared logging contract) already
defines two `system_variant` values for the proposed system:

- `Variant_1_ErrorTrace`
- `Variant_2_StatePrediction`

So this design treats "Proposed" from the brief as a family with a shared
loop and a swappable feedback strategy, rather than one fixed prompt design.
That also gives Member 4 a natural extra data point for the paper (which
feedback style converges faster / cheaper) without changing RQ1's headline
comparison — both variants are still "mutant-guided iterative refinement,"
just with different feedback content.

| Variant | Feedback content | Inspiration |
|---|---|---|
| `Variant_1_ErrorTrace` | Mutated line, original line, and the specific assertion(s) that ran but failed to catch the mutant. | Brief Section 3.3, "Feedback content." |
| `Variant_2_StatePrediction` | Same diff context, plus an explicit reasoning step asking the model to predict the runtime state divergence (which variable's value changes, and how) before writing an assertion that targets that divergence directly. | LogicHunter (brief 1.4) — an agentic oracle that reasons about runtime state rather than passively classifying. Aimed at RQ2 (weak-oracle tests). |

## Module layout

```
refinement_loop/                (repo root)
  models.py            Data model — mirrors schema/execution_log_schema.json exactly
  interfaces.py         Protocols for the two things this module depends on
                         but doesn't own: MutationRunner (Member 2) and
                         LLMClient (the API wrapper)
  config.py              RefinementConfig — stopping rule + prompt-size knobs
  prompt_strategies.py   THE CORE PIECE: SurvivingMutant list -> prompt text
  loop_controller.py      RefinementLoop — the generate/mutate/feedback/repeat
                          orchestration
  logger.py               Serializes a RunLog to JSON, validates against
                          schema/execution_log_schema.json
  examples/
    demo_run.py           End-to-end demo using fake mutation runner + LLM,
                          on dataset/function_25.py (is_prime)
  tests/
    test_prompt_strategies.py
    test_loop_controller.py
```

This package sits alongside `baselines/` (Member 3), and reuses the repo's
existing `dataset/` and `schema/` folders rather than duplicating them.

## How a surviving mutant becomes a prompt

1. **`MutationRunner.run()`** (Member 2's pipeline, injected via the
   `MutationRunner` Protocol) returns a `MutationResult`: total mutants,
   killed count, and a list of `SurvivingMutant` objects. Each one carries
   the mutant id, operator type, line number, original/mutated source line,
   and the assertions that ran against it but didn't fail.

2. **Target selection** (`PromptStrategy._select_targets`) caps how many
   mutants go into one prompt (`max_mutants_per_prompt`, default 8) to keep
   token cost bounded per Section 3.3's cost-fairness constraint. When there
   are more survivors than the cap, selection round-robins across distinct
   `mutant_operator` types first, so one round doesn't burn its whole budget
   on ten near-identical boundary mutants on one line — this also directly
   feeds RQ4 (whether refinement disproportionately helps certain mutant
   classes) by keeping early-round sampling operator-diverse.

3. **`PromptStrategy.build()`** turns the selected mutants into a system
   prompt + user prompt pair. `ErrorTraceStrategy` renders each mutant as a
   diff block with its failing assertions. `StatePredictionStrategy` adds an
   instruction to reason about state divergence first, and threads any prior
   `predicted_state` value back in on later rounds so the model can build on
   its own earlier reasoning instead of re-deriving it each iteration.

4. **`RefinementLoop.run()`** calls the LLM with that prompt, replaces the
   test file with the regenerated one, re-runs mutation testing, and checks
   two stopping conditions from Section 3.3 (both locked in `config.py`):
   - `max_iterations = 5` (hard cap per file)
   - `plateau_threshold_pp = 2.0` (stop early if a round's score gain is
     under 2 percentage points)

   Each targeted mutant's outcome (`mutant_killed`) is recorded per
   iteration, matching `iterations_detail` in the schema.

5. **`logger.write_run_log()`** dumps the finished `RunLog` to JSON in the
   exact shape `execution_log_schema.json` expects, and
   `logger.validate_run_log()` checks it against the schema if `jsonschema`
   is installed.

## Integration points for other members

- **Member 2**: implement `MutationRunner.run(function_source, test_code) ->
  MutationResult` on top of mutmut/coverage.py. `RefinementLoop` never
  imports mutmut directly, so this is a drop-in.
- **Member 3**: `Baseline A`/`Baseline B` don't use this module at all (no
  mutation feedback by design), but can reuse `models.MutationResult` /
  `logger.py` so all three systems log to the identical JSON shape, per the
  brief's "shared JSON logging format ... analysis code written once."
- **Whoever wires the LLM client**: implement `LLMClient.generate(user_prompt,
  system_prompt) -> (test_code, tokens_used)` against the Claude API
  (structured outputs recommended — see brief Section 1.3) and pass it into
  `RefinementLoop`.

## Known simplification to revisit in Week 3

`RefinementLoop._merge_tests()` currently just takes the model's regenerated
file as-is (the prompt asks for the complete updated file each round). If
Week 3 testing shows the model tends to drop previously-passing tests
instead of extending them, swap this for an AST-level merge that unions test
functions by name (see brief Section 1.2, `ast` module) instead of a full
replace.

## Running the demo

Run from the repo root (`pytest` and `jsonschema` are already in the root
`requirements.txt`):

```bash
.venv/bin/python refinement_loop/examples/demo_run.py   # runs both variants against dataset/function_25.py
.venv/bin/python -m pytest refinement_loop/tests/ -v      # 8 tests covering prompt construction + stopping rule
```
