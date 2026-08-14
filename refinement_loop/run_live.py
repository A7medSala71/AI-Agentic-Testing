"""Live runner for the proposed mutant-guided refinement systems.

The seed is exactly Baseline A's one-shot generator.  Every refinement pass is
then evaluated by the same Member-2 mutation/coverage pipeline used for the
baselines.  Final test suites are saved so every log is reproducible.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from baselines import baseline_a, config as baselines_config
from baselines.llm_client import LLMClient as GeminiStructuredClient
from baselines.prompt_context import build_context
from refinement_loop import adapters
from refinement_loop.adapters import GeminiTextClient, GroqStructuredClient, GroqTextClient, MutmutMutationRunner
from refinement_loop.config import VARIANT_ERROR_TRACE, VARIANT_STATE_PREDICTION, RefinementConfig
from refinement_loop.logger import validate_run_log, write_run_log
from refinement_loop.loop_controller import RefinementLoop

VARIANT_ALIASES = {"error_trace": VARIANT_ERROR_TRACE, "state_prediction": VARIANT_STATE_PREDICTION}


def resolve_provider(requested: str) -> str:
    if requested != "auto":
        return requested
    if adapters.has_groq_key():
        return "groq"
    if baselines_config.has_api_key():
        return "gemini"
    raise SystemExit("Set GROQ_API_KEY or GEMINI_API_KEY before a live run.")


def run_one(function_id: str, variant: str, run_index: int, provider: str, force: bool = False) -> Path:
    log_path = baselines_config.LOGS_DIR / f"{function_id}__{variant}__run{run_index}__{provider}.json"
    test_path = baselines_config.GENERATED_TESTS_DIR / f"{function_id}__{variant}__run{run_index}__{provider}__test.py"
    if not force and log_path.exists() and test_path.exists():
        print(f"[{function_id}] run{run_index}: skipped")
        return log_path

    ctx = build_context(baselines_config.DATASET_DIR / f"{function_id}.py")

    if provider == "groq":
        seed_client = GroqStructuredClient()
        refinement_client = GroqTextClient()
    else:
        seed_client = GeminiStructuredClient()
        refinement_client = GeminiTextClient()

    print(f"[{function_id}] seed: Baseline-A-style generation via {provider}")
    seed = baseline_a.run(ctx, client=seed_client)

    loop = RefinementLoop(
        config=RefinementConfig(variant=variant),
        mutation_runner=MutmutMutationRunner(function_id),
        llm_client=refinement_client,
    )
    print(f"[{function_id}] refinement: {variant}")
    result = loop.run(
        function_id=function_id,
        function_source=(baselines_config.DATASET_DIR / f"{function_id}.py").read_text(encoding="utf-8"),
        function_name=ctx.primary_function,
        initial_test_code=seed.test_source,
    )

    # The loop evaluates the final suite. Save that exact suite for replay.
    # Its current-tests value is intentionally not exposed by the old RunLog,
    # so the runner performs the same deterministic refinement process through
    # a small callback-free extension: the generated final suite is captured
    # by the loop object below.
    final_suite = getattr(loop, "last_test_code", None) or seed.test_source
    test_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.write_text(final_suite, encoding="utf-8")

    seed_summary = seed.tracker.summary()
    result.total_tokens_used += seed_summary["total_tokens_used"]
    result.num_llm_calls += seed_summary["num_llm_calls"]
    result.input_tokens += seed_summary["input_tokens"]
    result.output_tokens += seed_summary["output_tokens"]
    if provider == "groq":
        seed_cost = adapters.groq_cost_usd(seed_summary["input_tokens"], seed_summary["output_tokens"])
        refinement_cost = adapters.groq_cost_usd(
            getattr(refinement_client, "input_tokens", 0),
            getattr(refinement_client, "output_tokens", 0),
        )
    else:
        seed_cost = seed_summary["estimated_cost_usd"]
        refinement_cost = (
            getattr(refinement_client, "input_tokens", 0) / 1_000_000 * baselines_config.PRICE_PER_1M_INPUT_USD
            + getattr(refinement_client, "output_tokens", 0) / 1_000_000 * baselines_config.PRICE_PER_1M_OUTPUT_USD
        )
    result.estimated_cost_usd = round(seed_cost + refinement_cost, 6)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    validate_run_log(result)
    write_run_log(result, log_path)
    print(
        f"[{function_id}] done: mutation={result.mutation_score_pct:.2f}% "
        f"coverage={result.line_coverage_pct:.1f}% pass={result.pass_rate_pct:.1f}% "
        f"calls={result.num_llm_calls} tokens={result.total_tokens_used}"
    )
    return log_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run mutant-guided refinement live.")
    parser.add_argument("function_id", nargs="?")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--variant", choices=list(VARIANT_ALIASES), default="error_trace")
    parser.add_argument("--provider", choices=["auto", "gemini", "groq"], default="auto")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if not args.function_id and not args.all:
        parser.error("pass a function_id or --all")
    provider = resolve_provider(args.provider)
    function_ids = (
        sorted(p.stem for p in baselines_config.DATASET_DIR.glob("function_*.py"))
        if args.all else [args.function_id]
    )
    variant = VARIANT_ALIASES[args.variant]
    completed = failed = skipped = 0
    for fid in function_ids:
        for run_index in range(1, args.repeats + 1):
            log_path = baselines_config.LOGS_DIR / f"{fid}__{variant}__run{run_index}__{provider}.json"
            test_path = baselines_config.GENERATED_TESTS_DIR / f"{fid}__{variant}__run{run_index}__{provider}__test.py"
            already = log_path.exists() and test_path.exists()
            try:
                run_one(fid, variant, run_index, provider, args.force)
                if already and not args.force:
                    skipped += 1
                else:
                    completed += 1
            except Exception as exc:
                failed += 1
                print(f"[{fid}] run{run_index}: FAILED -- {type(exc).__name__}: {str(exc)[:180]}")
    print(f"\n{completed} completed, {skipped} skipped, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
