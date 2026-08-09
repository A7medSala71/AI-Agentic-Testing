"""
Member 4 -- live run: RefinementLoop wired to the real mutmut adapter and the
real Gemini API, replacing the Fakes in examples/demo_run.py.

The initial test suite (round 0, before any refinement) is generated the
same way Baseline A does it, via baselines.baseline_a, so Proposed and
Baseline A start from a comparable seed and RQ1's comparison stays fair.

Run:
    .venv/bin/python -m refinement_loop.run_live function_25
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
from baselines.llm_client import LLMClient as StructuredLLMClient
from baselines.prompt_context import build_context
from refinement_loop.adapters import GeminiTextClient, MutmutMutationRunner
from refinement_loop.config import VARIANT_ERROR_TRACE, VARIANT_STATE_PREDICTION, RefinementConfig
from refinement_loop.logger import validate_run_log, write_run_log
from refinement_loop.loop_controller import RefinementLoop

VARIANT_ALIASES = {
    "error_trace": VARIANT_ERROR_TRACE,
    "state_prediction": VARIANT_STATE_PREDICTION,
}


def run_one(function_id: str, variant: str, run_index: int, force: bool = False) -> None:
    if not baselines_config.has_api_key():
        raise SystemExit(
            "GEMINI_API_KEY not set -- put your key in .env (see .env.example) "
            "or export it before running this script."
        )

    out_path = (
        baselines_config.LOGS_DIR
        / f"{function_id}__{variant}__run{run_index}.json"
    )
    if not force and out_path.exists():
        print(f"[{function_id}] run{run_index} ({variant}): skipped (already logged)")
        return

    ctx = build_context(baselines_config.DATASET_DIR / f"{function_id}.py")

    print(f"[{function_id}] seeding initial suite (Baseline-A-style, 1 call)...")
    structured_client = StructuredLLMClient()
    seed = baseline_a.run(ctx, client=structured_client)

    print(f"[{function_id}] running refinement loop ({variant})...")
    loop = RefinementLoop(
        config=RefinementConfig(variant=variant),
        mutation_runner=MutmutMutationRunner(function_id),
        llm_client=GeminiTextClient(),
    )
    run_log = loop.run(
        function_id=function_id,
        function_source=ctx.source_for_prompt,
        function_name=ctx.primary_function,
        initial_test_code=seed.test_source,
    )
    # fold in the seed call's usage so total_tokens_used reflects the whole run
    seed_summary = seed.tracker.summary()
    run_log.total_tokens_used += seed_summary["total_tokens_used"]
    run_log.estimated_cost_usd = round(
        run_log.estimated_cost_usd + seed_summary["estimated_cost_usd"], 6
    )

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
        "--force", action="store_true",
        help="re-run even if a log for this function/variant/run already exists",
    )
    args = parser.parse_args()

    if not args.function_id and not args.all:
        parser.error("pass a function_id or --all")

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
                / f"{function_id}__{variant}__run{run_index}.json"
            ).exists()
            try:
                run_one(function_id, variant, run_index, force=args.force)
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
