"""Week 1 acceptance check for Member 3's environment.

Proves, end to end and without needing a Baseline built yet:
  1. the dataset parses and prompt context is constructed as configured,
  2. structured output round-trips into a validated pydantic object,
  3. usage accounting records calls and tokens,
  4. a rendered suite is real pytest that passes against the real function,
  5. a run record validates against the team's JSON schema.

Run:  .venv/bin/python -m baselines.smoke_test
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from . import config
from .llm_client import LLMClient, UsageTracker
from .prompt_context import all_functions, build_context
from .run_log import validate, write
from .schemas import ExecutionLog, GeneratedTestSuite, PanelReview, TestCase

PASS = "  [PASS]"
FAIL = "  [FAIL]"
failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    print(f"{PASS if condition else FAIL} {name}" + (f" -- {detail}" if detail else ""))
    if not condition:
        failures.append(name)


def section(title: str) -> None:
    print(f"\n{title}\n{'-' * len(title)}")


def main() -> int:
    print("=" * 62)
    print("Member 3 -- Week 1 environment acceptance check")
    print("=" * 62)
    print(f"  model            : {config.MODEL_ID}")
    print(f"  api key present  : {config.has_api_key()}")
    print("  mode             : MOCK (forced -- live coverage is in live_check)")
    print(f"  include_doctests : {config.INCLUDE_DOCTESTS}")
    print(f"  temperature      : {config.TEMPERATURE}")
    print(f"  panel size       : {config.PANEL_SIZE}")

    # --- 1. dataset -------------------------------------------------------
    section("1. Dataset and prompt context")
    contexts = all_functions()
    check("all 30 dataset files parse", len(contexts) == 30, f"{len(contexts)} found")

    multi = [c for c in contexts if len(c.public_functions) > 1]
    check(
        "multi-function files identified",
        len(multi) > 0,
        f"{len(multi)} files hold >1 public function",
    )

    f03 = build_context(config.DATASET_DIR / "function_03.py")
    check(
        "scaffolding stripped from prompt",
        "__main__" not in f03.source_for_prompt,
        "no __main__ block",
    )
    doctests_gone = ">>>" not in f03.source_for_prompt
    check(
        f"doctest policy applied (INCLUDE_DOCTESTS={config.INCLUDE_DOCTESTS})",
        doctests_gone is not config.INCLUDE_DOCTESTS,
        "doctests absent" if doctests_gone else "doctests present",
    )

    # --- 2. structured output --------------------------------------------
    section("2. Structured output")
    # Always mocked: this check verifies plumbing, not model behaviour. Keeping
    # it deterministic means it stays reproducible and never eats the daily
    # free-tier quota. Live behaviour is covered by baselines/live_check.py.
    tracker = UsageTracker()
    client = LLMClient(tracker=tracker, force_mock=True)

    suite = client.generate(
        system_prompt="You are an expert Python test engineer.",
        user_prompt=f"Write a pytest suite for:\n\n{f03.source_for_prompt}",
        response_model=GeneratedTestSuite,
        label="smoke:generate",
    )
    check(
        "response parsed into GeneratedTestSuite",
        isinstance(suite, GeneratedTestSuite),
        f"{len(suite.tests)} tests",
    )

    wildcard = GeneratedTestSuite(
        module_under_test="function_25",
        imports=["from function_25 import *"],
        tests=[TestCase(test_name="test_x", test_code="def test_x():\n    pass", rationale="-")],
    )
    rejected = False
    try:
        wildcard.to_source()
    except ValueError:
        rejected = True
    check(
        "wildcard imports rejected at render time",
        rejected,
        "protects function_25 pass rate",
    )

    review = client.generate(
        system_prompt="You are a meticulous test reviewer.",
        user_prompt="Review these oracles.",
        response_model=PanelReview,
        label="smoke:critique",
    )
    check(
        "response parsed into PanelReview",
        isinstance(review, PanelReview),
        f"{len(review.judgements)} judgements",
    )

    # --- 3. usage accounting ---------------------------------------------
    section("3. Usage accounting")
    s = tracker.summary()
    check("calls counted", s["num_llm_calls"] == 2, f"{s['num_llm_calls']} calls")
    check("tokens counted", s["total_tokens_used"] > 0, f"{s['total_tokens_used']} tokens")
    check("cost estimated", s["estimated_cost_usd"] >= 0, f"${s['estimated_cost_usd']}")

    # --- 4. generated tests actually run ---------------------------------
    section("4. Rendered suite runs under pytest")
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        (tmpdir / "function_03.py").write_text(
            (config.DATASET_DIR / "function_03.py").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (tmpdir / "test_function_03.py").write_text(suite.to_source(), encoding="utf-8")

        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "test_function_03.py"],
            cwd=tmpdir,
            capture_output=True,
            text=True,
        )
        check(
            "generated suite passes against real source",
            result.returncode == 0,
            (result.stdout.strip().splitlines() or ["no output"])[-1],
        )

    # --- 5. team schema ---------------------------------------------------
    section("5. Team schema conformance")
    log = ExecutionLog(
        function_id="function_03",
        system_variant="Baseline_A",
        iteration_count=1,
        total_tokens_used=s["total_tokens_used"],
        mutation_score_pct=0.0,
        estimated_cost_usd=s["estimated_cost_usd"],
        line_coverage_pct=100.0,
        num_llm_calls=s["num_llm_calls"],
    )
    errors = validate(log)
    check("ExecutionLog validates against team schema", not errors, "; ".join(errors))

    with tempfile.TemporaryDirectory() as tmp:
        path = write(log, run_index=1, logs_dir=Path(tmp))
        check("log written to disk", path.exists(), path.name)

    # --- verdict ----------------------------------------------------------
    print("\n" + "=" * 62)
    if failures:
        print(f"FAILED ({len(failures)}): " + ", ".join(failures))
    else:
        print("ALL CHECKS PASSED -- Week 1 environment is ready.")
    print("=" * 62)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
