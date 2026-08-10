# Member 4 Update — Proposed Refinement Loop

## What was fixed

1. **Proposed refinement iteration count**
   - `iteration_count` now means actual refinement rounds.
   - A seed suite that already kills all mutants reports `0`, not `1`.
   - The shared JSON schema now allows `0..5` for this field.

2. **Stop reason is logged**
   - `no_survivors`
   - `plateau`
   - `max_iterations`
   - `invalid_regeneration`
   - `completed`

3. **LLM-call accounting**
   - Refinement calls are counted by the loop.
   - `run_live.py` adds the initial seed-generation call.
   - `num_llm_calls` is written to the JSON log.

4. **Cost accounting**
   - Gemini and Groq text clients expose per-call cost.
   - Refinement-call cost is accumulated instead of charging only the seed call.
   - The seed call is added in `run_live.py`.

5. **Pass-rate and branch-coverage propagation**
   - The fallback mutation runner now records pass rate from pytest and branch coverage when available.
   - The fields are optional in the shared schema so older baseline tooling is not broken while Member 2 finalizes the shared evaluator.

6. **Mutation-run failure protection**
   - The fallback runner no longer silently interprets a failed `mutmut` run with no metadata as `0 mutants` / `100% mutation score`.
   - It raises an explicit error instead.

7. **Regeneration validation**
   - Generated refinement output is parsed with `ast`.
   - Syntax-invalid responses and responses with no `test_*` function are discarded.

8. **Test preservation**
   - If the LLM drops an existing test from its regenerated file, the loop restores the missing previous test functions using an AST merge.
   - If all previous tests are present, the model output is kept unchanged.

9. **No fabricated assertion attribution**
   - The temporary fallback mutation runner no longer claims that every assertion/test covered every surviving mutant.
   - Exact per-mutant assertion attribution must come from Member 2's final shared mutation pipeline, as required by the brief.

10. **Notebook cleanup**
    - Removed the malformed `-- all` command.
    - Separated the optional Variant 2 sweep from the core Variant 1 experiment.
    - Added schema validation and a no-API log audit cell.
    - Full sweeps remain resumable and are only run after the API quota is available.

## What is intentionally NOT replaced

Member 2 owns the authoritative mutation-score/coverage pipeline. The local `MutmutMutationRunner` remains a development fallback. The final experiment should connect Member 2's runner to the contract in `refinement_loop/interfaces.py`:

```text
MutationRunner.run(function_source, test_code) -> MutationResult
```

The final `MutationResult` should provide mutation score/survivors plus the metrics Member 2 already computes. In particular, exact mutant-to-assertion attribution should be supplied there rather than reconstructed or guessed by Member 4.

## Verification performed on this updated copy

- `python -m pytest refinement_loop/tests -q` → **12 passed**
- JSON Schema itself validates successfully.
- A Proposed zero-refinement sample validates against the updated schema.
- Python compilation succeeded for `refinement_loop`, `evaluation`, and `baselines`.

The sandbox used for this update did not have `mutmut` installed, so a fresh live mutation run was not fabricated. The uploaded notebook/logs were used to drive the changes, and the existing live Groq run remains validation evidence rather than being overwritten.
