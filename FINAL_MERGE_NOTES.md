# Final merge notes

This package is the integrated final project:
- Member 2 shared evaluation: `evaluation/`
- Member 3 Baseline A/B: `baselines/`
- Member 4 proposed refinement: `refinement_loop/`
- 30-function dataset: `dataset/`
- shared execution schema: `schema/execution_log_schema.json`
- generated suites: `generated_tests/`
- run records: `logs/`
- final Colab/local notebook: `notebooks/final_experiment.ipynb`

Validation performed in this environment:
- Python compilation: all project `.py` files compile.
- Offline acceptance tests: 9 passed.
- Refinement-loop fake integration demo: both variants completed and produced schema-valid sample logs.

The live mutation toolchain was not executed in this environment because the
current runtime did not have the pinned `mutmut` executable installed. The
repository invokes mutmut through the active Python interpreter and the pinned
`requirements.txt` installs it for the target environment.

Important experimental rule:
reported mutation score/coverage/pass-rate numbers must come from the shared
evaluation pipeline, not from mock runs.
