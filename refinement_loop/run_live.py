"""Live runner for the two mutant-guided refinement variants.

The runner is intentionally diagnostic and resumable: one failed function does
not abort the remaining sweep, failures include full tracebacks, and a failed
run never produces a fake/partial experimental JSON record.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
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
    raise SystemExit("No API key found. Set GEMINI_API_KEY or GROQ_API_KEY.")


def _failure_path(function_id: str, variant: str, run_index: int, provider: str) -> Path:
    p = baselines_config.LOGS_DIR / "failures" / f"{function_id}__{variant}__run{run_index}__{provider}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _write_failure(function_id, variant, run_index, provider, exc):
    path = _failure_path(function_id, variant, run_index, provider)
    payload = {
        "function_id": function_id,
        "system_variant": variant,
        "repeat": run_index,
        "provider": provider,
        "model": getattr(exc, "model", None),
        "error_type": type(exc).__name__,
        "error": str(exc),
        "traceback": traceback.format_exc(),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def run_one(function_id: str, variant: str, run_index: int, provider: str, force: bool = False, model: str | None = None, output_dir: Path | None = None):
    output_dir = output_dir or baselines_config.LOGS_DIR
    out_path = output_dir / f"{function_id}__{variant}__run{run_index}__{provider}.json"
    generated_dir = baselines_config.GENERATED_TESTS_DIR
    out_path.parent.mkdir(parents=True, exist_ok=True)
    generated_dir.mkdir(parents=True, exist_ok=True)
    if not force and out_path.exists():
        print(f"[{function_id}] run{run_index} ({variant}, {provider}): skipped (already logged)")
        return False

    ctx = build_context(baselines_config.DATASET_DIR / f"{function_id}.py")
    actual_model = model or baselines_config.MODEL_ID if provider == "gemini" else (model or adapters.GROQ_MODEL_ID)

    print(f"[{function_id}] seed -> {provider}/{actual_model}")
    if provider == "groq":
        structured_client = GroqStructuredClient(model=actual_model)
        text_client = GroqTextClient(model=actual_model)
    else:
        structured_client = GeminiStructuredClient(model=actual_model)
        text_client = GeminiTextClient(model=actual_model)

    seed = baseline_a.run(ctx, client=structured_client)
    print(f"[{function_id}] refinement -> {variant}")
    loop = RefinementLoop(
        config=RefinementConfig(variant=variant),
        mutation_runner=MutmutMutationRunner(function_id),
        llm_client=text_client,
    )
    # RefinementLoop.run() returns a RunLog. The final merged test suite is
    # exposed separately through loop.final_test_code.
    run_log = loop.run(
        function_id=function_id,
        function_source=ctx.source_for_prompt,
        function_name=ctx.primary_function,
        initial_test_code=seed.test_source,
    )
    final_test_code = loop.final_test_code

    seed_summary = seed.tracker.summary()
    refinement_calls = int(getattr(text_client, "num_calls", 0))
    refinement_tokens = int(getattr(text_client, "total_tokens_used", run_log.total_tokens_used))
    refinement_cost = float(getattr(text_client, "total_cost_usd", 0.0))
    run_log.total_tokens_used = int(seed_summary["total_tokens_used"] + refinement_tokens)
    run_log.num_llm_calls = int(seed_summary["num_llm_calls"] + refinement_calls)
    seed_cost = adapters.groq_cost_usd(seed_summary["input_tokens"], seed_summary["output_tokens"]) if provider == "groq" else seed_summary["estimated_cost_usd"]
    run_log.estimated_cost_usd = round(float(seed_cost) + refinement_cost, 6)
    run_log.provider = provider
    run_log.model = actual_model

    validate_run_log(run_log)
    write_run_log(run_log, out_path)
    test_path = generated_dir / f"{function_id}__{variant}__run{run_index}__{provider}.py"
    test_path.write_text(final_test_code, encoding="utf-8")
    print(f"[{function_id}] done -- iterations={run_log.iteration_count}, mutation={run_log.mutation_score_pct}%, pass={run_log.pass_rate_pct}%, calls={run_log.num_llm_calls}, tokens={run_log.total_tokens_used}")
    print(f"  log: {out_path}")
    print(f"  tests: {test_path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Run mutant-guided refinement live.")
    parser.add_argument("function_id", nargs="?", help="e.g. function_01")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--variant", choices=list(VARIANT_ALIASES), default="error_trace")
    parser.add_argument("--provider", choices=["auto", "gemini", "groq"], default="auto")
    parser.add_argument("--model", default=None, help="Explicit model for the selected provider")
    parser.add_argument("--max-retry-wait", type=float, default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--smoke-test", action="store_true", help="Run exactly one real function/variant without creating a final experiment log")
    args = parser.parse_args()
    if not args.function_id and not args.all and not args.smoke_test:
        parser.error("pass a function_id, --all, or --smoke-test")
    if args.repeats < 1:
        parser.error("--repeats must be >= 1")

    provider = resolve_provider(args.provider)
    if args.max_retry_wait is not None:
        os.environ["GROQ_MAX_RETRY_WAIT_SECONDS"] = str(args.max_retry_wait)
    model = args.model
    print(f"Using provider: {provider}")
    print(f"Using model: {model or (baselines_config.MODEL_ID if provider == 'gemini' else adapters.GROQ_MODEL_ID)}")

    if args.smoke_test:
        function_id = args.function_id or "function_01"
        variant = VARIANT_ALIASES[args.variant]
        smoke_dir = baselines_config.LOGS_DIR / "smoke_tests"
        try:
            run_one(function_id, variant, 1, provider, force=True, model=model, output_dir=smoke_dir)
            print("SMOKE TEST: PASS")
            return 0
        except Exception as exc:
            path = _write_failure(function_id, variant, 1, provider, exc)
            print("SMOKE TEST: FAIL")
            print(traceback.format_exc())
            print(f"Failure diagnostics: {path}")
            return 1

    function_ids = sorted(p.stem for p in baselines_config.DATASET_DIR.glob("function_*.py")) if args.all else [args.function_id]
    variant = VARIANT_ALIASES[args.variant]
    baselines_config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    completed = skipped = failed = 0
    for function_id in function_ids:
        for run_index in range(1, args.repeats + 1):
            out_path = baselines_config.LOGS_DIR / f"{function_id}__{variant}__run{run_index}__{provider}.json"
            before = out_path.exists()
            try:
                made = run_one(function_id, variant, run_index, provider, force=args.force, model=model)
            except Exception as exc:
                failed += 1
                path = _write_failure(function_id, variant, run_index, provider, exc)
                print(f"[{function_id}] run{run_index}: FAILED -- {type(exc).__name__}: {exc}")
                print(traceback.format_exc())
                print(f"  Failure diagnostics: {path}")
                continue
            if before and not args.force:
                skipped += 1
            elif made:
                completed += 1

    print(f"\n{completed} completed, {skipped} skipped, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
