# Two-LLM Comparison

The final notebook includes a controlled one-call Gemini vs Groq comparison.

For the selected function, both providers receive:
- the same function source,
- the same Baseline-A system prompt,
- the same Baseline-A user prompt,
- the same structured output schema,
- exactly one generation call each.

The generated suites are then scored using the same `baselines.score.score_suite`
mutation/coverage/pytest evaluator.

These records are stored separately under `logs/llm_comparison/` and are not
included in the main repeated-experiment aggregation.

The notebook then runs the main 30-function x 3-repeat experiment using the
selected full-experiment provider. This preserves the project's existing
experimental design while giving the paper a direct cross-LLM comparison point.
