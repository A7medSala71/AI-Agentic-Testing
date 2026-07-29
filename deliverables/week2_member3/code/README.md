# baselines/ — Member 3 (Baseline Systems Lead)

Baseline A (single-shot generation) and Baseline B (one-shot multi-agent
consensus), plus the shared infrastructure both sit on.

## Layout

| File | Purpose |
|---|---|
| `baseline_a.py` | **Baseline A** — single-shot generation. 1 call per function. |
| `baseline_b.py` | **Baseline B** — propose → 3× critique → finalise. 5 calls per function. |
| `prompts.py` | All prompt templates, kept together so wording can be quoted in the paper. |
| `config.py` | Every experimental knob in one place, so settings can be cited in the paper. |
| `schemas.py` | Structured-output contracts + `ExecutionLog` mirroring the team schema. |
| `llm_client.py` | LLM wrapper with per-call token/cost accounting. Runs mocked without a key. |
| `prompt_context.py` | Turns a dataset file into the exact source text the model sees. |
| `run_log.py` | Validates a run against `schema/execution_log_schema.json`, then writes it. |
| `smoke_test.py` | Week 1 acceptance check — proves the environment end to end. |
| `toolchain_check.py` | Proves mutmut/coverage work, and demonstrates the weak-oracle effect. |
| `live_check.py` | Live-API check: schema-conformance rate, real token counts, cost projection. |
| `score.py` | Local scoring (coverage + mutmut) for validating generated suites. |
| `runner.py` | Shared sweep: generate → score → log, with resume so a crashed run continues. |

## Running the baselines

```bash
.venv/bin/python -m baselines.baseline_a function_03            # one function
.venv/bin/python -m baselines.baseline_b function_03            # one function
.venv/bin/python -m baselines.baseline_a --all --repeats 3      # full sweep
.venv/bin/python -m baselines.baseline_a --all --repeats 3 --score   # full sweep, scored + logged
.venv/bin/python -m baselines.baseline_b --all --mock                # no API calls
```

Generated suites land in `generated_tests/` as
`<function_id>__<system>__run<n>__test.py`.

Use `--mock` while developing: it exercises the whole pipeline without
consuming the daily free-tier quota (~20 calls/day — see
`docs/week1_member3_report.md` §6.5).

## Setup — every team member does this once

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
```

Then get **your own** free API key at
<https://aistudio.google.com/apikey> and put it in `.env`:

```
GEMINI_API_KEY=your_key_here
```

No quotes, no spaces around the `=`. `config.py` loads it automatically.

### Why each member needs their own key, not a shared one

**This repo is public.** GitHub scans public commits for API keys, reports
Google keys to Google, and Google auto-revokes them — usually within minutes.
A key committed here dies before anyone can use it, and stays in git history
permanently even after it is deleted. `.env` is gitignored for that reason;
leave it that way.

Separately, the Gemini free tier is rate-limited **per account**. Four people
sharing one key share one rate limit, which will throttle everyone during the
Week 4 full-scale runs (30 functions × 4 systems × 3 repeats, and Baseline B
spends 5 calls per function). Separate keys are simply faster.

If a key ever does get committed, treat it as burned: revoke it in AI Studio
and issue a new one. Deleting the file in a later commit does not remove it.

## Run

```bash
.venv/bin/python -m baselines.smoke_test        # environment acceptance (no key needed)
.venv/bin/python -m baselines.toolchain_check   # mutation toolchain + RQ2 demo (no key needed)
.venv/bin/python -m baselines.live_check        # live API (needs a key)
```

`smoke_test` runs in **mock mode** without an API key, so the whole pipeline is
verifiable before spending anything.

## Why the usage tracker exists

Brief §3.5 requires reporting *calls and cost per file*, and RQ1 only holds if
the systems are compared at a comparable budget — Baseline B spends 5 calls per
function where Baseline A spends 1. Token counts that are not recorded at call
time cannot be reconstructed afterwards, so every call goes through
`LLMClient.generate`, which folds usage into a `UsageTracker`.

Gemini 3.x emits reasoning tokens; `thoughts_token_count` is billed and is
counted separately here rather than dropped.

## Configuration that is still an open team decision

`config.INCLUDE_DOCTESTS` — every dataset function ships doctests, i.e. worked
input→output oracles, in its docstring. Currently `false` (stripped). Whatever
is chosen must be identical across Baseline A, Baseline B and both proposed
variants. See `docs/week1_member3_report.md`.
