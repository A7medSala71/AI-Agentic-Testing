"""Shared sweep runner for Baseline A and B (Member 3).

Generation alone is not a deliverable. A run only counts once it has produced a
schema-valid record in `logs/` — that record is the contract Member 1's
analysis and Member 4's comparison both read from. This module wires the three
stages together:

    generate  ->  score (optional)  ->  write ExecutionLog

**Resume is the reason this exists.** Week 4 is 30 functions x 3 repeats per
system; Baseline B alone is 450 calls that take hours. A crash at run 78 must
not mean starting over, and re-running completed work costs real money. Any
run whose log already exists is skipped unless `--force` is passed.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path

from . import config, run_log
from .baseline_a import BaselineResult
from .llm_client import LLMClient, UsageTracker
from .prompt_context import FunctionContext, all_functions, build_context


def _already_done(function_id: str, system_variant: str, run_index: int) -> bool:
    """A run counts as done only when *both* its artefacts survive.

    Keying on the log alone is not enough: deleting generated_tests/ while
    keeping logs/ makes every run look complete, and the sweep then skips work
    whose output no longer exists -- leaving a log that points at nothing.
    """
    log = config.LOGS_DIR / run_log.log_filename(function_id, system_variant, run_index)
    suite = config.GENERATED_TESTS_DIR / (
        f"{function_id}__{system_variant}__run{run_index}__test.py"
    )
    return log.exists() and suite.exists()


def sweep(
    run_one: Callable[[FunctionContext, LLMClient], BaselineResult],
    system_variant: str,
    contexts: list[FunctionContext],
    repeats: int = 1,
    mock: bool = False,
    score: bool = False,
    force: bool = False,
) -> int:
    """Run one system over the given functions, logging every completed run."""
    config.GENERATED_TESTS_DIR.mkdir(parents=True, exist_ok=True)
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    total = UsageTracker()
    completed = skipped = failed = 0

    for ctx in contexts:
        for repeat in range(1, repeats + 1):
            if not force and _already_done(ctx.function_id, system_variant, repeat):
                skipped += 1
                print(f"  {ctx.function_id} run{repeat}: skipped (already logged)")
                continue

            client = LLMClient(tracker=UsageTracker(), force_mock=mock)
            try:
                result = run_one(ctx, client)
            except Exception as exc:  # noqa: BLE001 - one failure must not stop the sweep
                failed += 1
                print(
                    f"  {ctx.function_id} run{repeat}: FAILED -- "
                    f"{type(exc).__name__}: {str(exc)[:120]}"
                )
                continue

            out = config.GENERATED_TESTS_DIR / (
                f"{ctx.function_id}__{system_variant}__run{repeat}"
                f"{'__MOCK' if client.mocked else ''}__test.py"
            )
            out.write_text(result.test_source, encoding="utf-8")

            metrics: dict = {}
            if score:
                from .score import score_suite

                scored = score_suite(ctx.function_id, result.test_source)
                if scored is not None:
                    metrics = {
                        "mutation_score_pct": round(scored.mutation_score_pct, 2),
                        "line_coverage_pct": round(scored.line_coverage_pct, 2),
                        "pass_rate_pct": round(scored.pass_rate_pct, 2),
                    }

            log = result.to_log(**metrics)
            # Mock runs are canned output; logging them would put meaningless
            # numbers into the shared record the team analyses.
            if not client.mocked:
                run_log.write(log, run_index=repeat)

            total.records.extend(result.tracker.records)
            completed += 1

            summary = result.tracker.summary()
            detail = (
                f" mutation {metrics['mutation_score_pct']:.0f}%"
                if "mutation_score_pct" in metrics
                else ""
            )
            print(
                f"  {ctx.function_id} run{repeat}: {len(result.suite.tests)} tests, "
                f"{summary['num_llm_calls']} call(s), "
                f"{summary['total_tokens_used']} tokens{detail}"
            )

    print(
        f"\n{completed} completed, {skipped} skipped, {failed} failed"
        f"\nTotal: {total.summary()}"
    )
    if not mock and completed:
        print(f"Logs written to {config.LOGS_DIR}")
    return 1 if failed and not completed else 0


def build_parser(description: str) -> argparse.ArgumentParser:
    """The CLI both baselines share."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("function", nargs="?", help="e.g. function_03")
    parser.add_argument("--all", action="store_true", help="run every dataset function")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--mock", action="store_true", help="no API calls")
    parser.add_argument(
        "--score", action="store_true",
        help="score each suite (coverage + mutmut) and log the metrics",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="re-run and overwrite runs that are already logged",
    )
    return parser


def resolve_contexts(args: argparse.Namespace, parser: argparse.ArgumentParser):
    if not args.all and not args.function:
        parser.error("give a function id, or --all")
    if args.all:
        return all_functions()
    return [build_context(config.DATASET_DIR / f"{args.function}.py")]


def logs_dir_status() -> str:
    """One-line summary of what's already been logged — the resume view."""
    if not config.LOGS_DIR.exists():
        return "logs/: (missing)"
    by_system: dict[str, int] = {}
    for path in config.LOGS_DIR.glob("*.json"):
        parts = Path(path).stem.split("__")
        if len(parts) >= 2:
            by_system[parts[1]] = by_system.get(parts[1], 0) + 1
    if not by_system:
        return "logs/: empty"
    return "logs/: " + ", ".join(f"{k}={v}" for k, v in sorted(by_system.items()))
