"""
Member 4 -- live run: RefinementLoop wired to a real mutation runner and a
real LLM provider (Gemini or Groq), replacing the Fakes in examples/demo_run.py.

The initial test suite (round 0, before any refinement) is generated the
same way Baseline A does it, so Proposed and Baseline A start from a
comparable seed and RQ1's comparison stays fair.

Provider selection (--provider auto|gemini|groq, default auto):
    auto prefers Groq if GROQ_API_KEY is set, else Gemini if GEMINI_API_KEY
    is set. Explicit auto-preference for Groq exists because the Gemini
    Cloud project used for this run started returning
    403 PERMISSION_DENIED ("project has been denied access") independent of
    the key's validity -- switching provider was a response to that, not a
    style preference, so auto shouldn't silently fall back to a project
    that's known to be blocked.

Run:
    .venv/bin/python -m refinement_loop.run_live function_25
    .venv/bin/python -m refinement_loop.run_live function_25 --provider groq
    .venv/bin/python -m refinement_loop.run_live function_25 --variant state_prediction
    .venv/bin/python -m refinement_loop.run_live --all --repeats 3
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from baselines import baseline_a, config as baselines_config
from baselines.llm_client import LLMClient as GeminiStructuredClient
from baselines.prompt_context import build_context
from refinement_loop import adapters
from refinement_loop.adapters import (
    GeminiTextClient,
    GroqStructuredClient,
    GroqTextClient,
    MutmutMutationRunner,
)
from refinement_loop.config import VARIANT_ERROR_TRACE, VARIANT_STATE_PREDICTION, RefinementConfig
from refinement_loop.logger import validate_run_log, write_run_log
from refinement_loop.loop_controller import RefinementLoop

VARIANT_ALIASES = {
    "error_trace": VARIANT_ERROR_TRACE,
    "state_prediction": VARIANT_STATE_PREDICTION,
}


def resolve_provider(requested: str) -> str:
    if requested != "auto":
        return requested
    if adapters.has_groq_key():
        return "groq"
    if baselines_config.has_api_key():
        return "gemini"
    raise SystemExit(
        "No API key found. Set GROQ_API_KEY or GEMINI_API_KEY (.env or "
        "environment) before running this script."
    )


def run_one(
    function_id: str, variant: str, run_index: int, provider: str, force: bool = False
) -> None:
    out_path = (
        baselines_config.LOGS_DIR
        / f"{function_id}__{variant}__run{run_index}__{provider}.json"
    )
    if not force and out_path.exists():
        print(f"[{function_id}] run{run_index} ({variant}, {provider}): "
              f"skipped (already logged)")
        return

    ctx = build_context(baselines_config.DATASET_DIR / f"{function_id}.py")

    print(f"[{function_id}] seeding initial suite via {provider} "
          f"(Baseline-A-style, 1 call)...")
    if provider == "groq":
        structured_client = GroqStructuredClient()
        text_client = GroqTextClient()
    else:
        structured_client = GeminiStructuredClient()
        text_client = GeminiTextClient()
    seed = baseline_a.run(ctx, client=structured_client)

    print(f"[{function_id}] running refinement loop ({variant}, {provider})...")
    loop = RefinementLoop(
        config=RefinementConfig(variant=variant),
        mutation_runner=MutmutMutationRunner(function_id),
        llm_client=text_client,
    )
    run_log = loop.run(
        function_id=function_id,
        function_source=ctx.source_for_prompt,
        function_name=ctx.primary_function,
        initial_test_code=seed.test_source,
    )
    # fold in the seed call's usage so total_tokens_used/cost reflect the whole run
    seed_summary = seed.tracker.summary()
    run_log.total_tokens_used += seed_summary["total_tokens_used"]
    run_log.num_llm_calls = (run_log.num_llm_calls or 0) + seed_summary["num_llm_calls"]
    if provider == "groq":
        # UsageTracker.summary() prices against baselines.config's Gemini
        # figures regardless of who made the call -- recompute with Groq's
        # own price table instead of trusting that number here.
        seed_cost = adapters.groq_cost_usd(
            seed_summary["input_tokens"], seed_summary["output_tokens"]
        )
    else:
        seed_cost = seed_summary["estimated_cost_usd"]
    run_log.estimated_cost_usd = round(run_log.estimated_cost_usd + seed_cost, 6)

    validate_run_log(run_log)
    write_run_log(run_log, out_path)

    print(
        f"[{function_id}] done -- {run_log.iteration_count} iteration(s), "
        f"mutation {run_log.mutation_score_pct}%, "
        f"{run_log.total_tokens_used} tokens -> {out_path}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the refinement loop live.")
    parser.add_argument("function_id", nargs="?", help="e.g. function_25")
    parser.add_argument("--all", action="store_true", help="run every dataset function")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument(
        "--variant", choices=list(VARIANT_ALIASES), default="error_trace",
    )
    parser.add_argument(
        "--provider", choices=["auto", "gemini", "groq"], default="auto",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="re-run even if a log for this function/variant/run already exists",
    )
    args = parser.parse_args()

    if not args.function_id and not args.all:
        parser.error("pass a function_id or --all")

    provider = resolve_provider(args.provider)
    print(f"Using provider: {provider}")

    function_ids = (
        sorted(p.stem for p in baselines_config.DATASET_DIR.glob("function_*.py"))
        if args.all
        else [args.function_id]
    )
    variant = VARIANT_ALIASES[args.variant]

    baselines_config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    completed = skipped = failed = 0
    for function_id in function_ids:
        for run_index in range(1, args.repeats + 1):
            before = (
                baselines_config.LOGS_DIR
                / f"{function_id}__{variant}__run{run_index}__{provider}.json"
            ).exists()
            try:
                run_one(function_id, variant, run_index, provider, force=args.force)
            except Exception as exc:  # noqa: BLE001 -- one function must not kill the sweep
                failed += 1
                print(f"[{function_id}] run{run_index}: FAILED -- "
                      f"{type(exc).__name__}: {str(exc)[:160]}")
                continue
            if before and not args.force:
                skipped += 1
            else:
                completed += 1

    print(f"\n{completed} completed, {skipped} skipped, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
