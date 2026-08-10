"""Local scoring for generated test suites (Member 3).

Member 2 owns the shared evaluation pipeline that all four systems will be
scored with for the paper. This module is **not** a replacement for it — it
exists so Baseline A and B can be validated without being blocked, and so the
first RQ1 signal can be produced before that pipeline is fixed. Final reported
numbers should come from `evaluation/`.

The recipe (mutmut 3.x config keys, reading results from the `.meta` file
rather than scraping stdout) is the one verified in `toolchain_check.py`.

Run:  .venv/bin/python -m baselines.score                    # score everything
      .venv/bin/python -m baselines.score function_03        # one function
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from . import config

# Invoked as `-m mutmut` / `-m coverage` rather than a sibling console
# script, since sys.executable's directory and pip's installed
# console-script bin dir aren't guaranteed to be the same outside a venv
# (e.g. Colab's system Python has no `python`/`mutmut` binaries next to
# sys.executable at all).

# mutmut 3.x renamed its keys: paths_to_mutate -> source_paths, and
# tests_dir -> pytest_add_cli_args_test_selection. It refuses to run at all
# without this file -- even `mutmut --help` raises FileNotFoundError.
SETUP_CFG = """\
[mutmut]
source_paths={module}.py
pytest_add_cli_args_test_selection=tests/
"""


@dataclass
class Score:
    """One generated suite, evaluated."""

    function_id: str
    system_variant: str
    run_index: int
    tests_collected: int
    tests_passed: int
    mutants_total: int
    mutants_killed: int
    line_coverage_pct: float

    @property
    def mutation_score_pct(self) -> float:
        if not self.mutants_total:
            return 0.0
        return self.mutants_killed / self.mutants_total * 100

    @property
    def pass_rate_pct(self) -> float:
        if not self.tests_collected:
            return 0.0
        return self.tests_passed / self.tests_collected * 100


def _parse_pytest_counts(stdout: str) -> tuple[int, int]:
    """Return (collected, passed) from pytest's summary line."""
    passed = failed = errors = 0
    for line in reversed(stdout.strip().splitlines()):
        if " passed" in line or " failed" in line or " error" in line:
            for chunk in line.replace("=", " ").split(","):
                parts = chunk.split()
                for i, token in enumerate(parts):
                    if not token.isdigit() or i + 1 >= len(parts):
                        continue
                    label = parts[i + 1].rstrip("s")
                    if label == "passed":
                        passed = int(token)
                    elif label == "failed":
                        failed = int(token)
                    elif label == "error":
                        errors = int(token)
            break
    return passed + failed + errors, passed


def score_suite(function_id: str, test_source: str) -> Score | None:
    """Run coverage + mutmut on one suite in an isolated workspace."""
    source_file = config.DATASET_DIR / f"{function_id}.py"
    if not source_file.exists():
        return None

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        (workdir / "tests").mkdir()
        shutil.copy(source_file, workdir / f"{function_id}.py")
        (workdir / "tests" / f"test_{function_id}.py").write_text(
            test_source, encoding="utf-8"
        )
        (workdir / "setup.cfg").write_text(
            SETUP_CFG.format(module=function_id), encoding="utf-8"
        )

        # --- pass rate + coverage against the unmutated source -------------
        result = subprocess.run(
            [sys.executable, "-m", "coverage", "run",
             f"--source={function_id}", "-m", "pytest", "-q", "tests/"],
            cwd=workdir, capture_output=True, text=True, timeout=300,
        )
        collected, passed = _parse_pytest_counts(result.stdout)

        subprocess.run(
            [sys.executable, "-m", "coverage", "json", "-o", "cov.json"],
            cwd=workdir, capture_output=True, text=True, timeout=120,
        )
        coverage_pct = 0.0
        cov_path = workdir / "cov.json"
        if cov_path.exists():
            coverage_pct = json.loads(cov_path.read_text(encoding="utf-8"))[
                "totals"
            ]["percent_covered"]

        # --- mutation score ------------------------------------------------
        subprocess.run(
            [sys.executable, "-m", "mutmut", "run"],
            cwd=workdir, capture_output=True, text=True, timeout=1800,
        )
        killed = total = 0
        meta_path = workdir / "mutants" / f"{function_id}.py.meta"
        if meta_path.exists():
            exit_codes = json.loads(meta_path.read_text(encoding="utf-8"))[
                "exit_code_by_key"
            ]
            # Non-zero exit code == the suite failed against that mutant == killed.
            killed = sum(1 for code in exit_codes.values() if code != 0)
            total = len(exit_codes)

    return Score(
        function_id=function_id,
        system_variant="",
        run_index=0,
        tests_collected=collected,
        tests_passed=passed,
        mutants_total=total,
        mutants_killed=killed,
        line_coverage_pct=round(coverage_pct, 1),
    )


def score_generated(function_filter: str | None = None) -> list[Score]:
    """Score every suite in generated_tests/, skipping mock output."""
    scores: list[Score] = []
    if not config.GENERATED_TESTS_DIR.exists():
        return scores

    for path in sorted(config.GENERATED_TESTS_DIR.glob("*__test.py")):
        parts = path.stem.split("__")
        if len(parts) < 3:
            continue
        function_id, system_variant, run_part = parts[0], parts[1], parts[2]
        if "MOCK" in path.stem:
            continue  # canned output; scoring it measures nothing
        if function_filter and function_id != function_filter:
            continue

        score = score_suite(function_id, path.read_text(encoding="utf-8"))
        if score is None:
            continue
        score.system_variant = system_variant
        score.run_index = int(run_part.replace("run", "") or 1)
        scores.append(score)

    return scores


def main() -> int:
    function_filter = sys.argv[1] if len(sys.argv) > 1 else None
    scores = score_generated(function_filter)

    if not scores:
        print("No generated suites to score.")
        print("Run baseline_a / baseline_b first (without --mock).")
        return 1

    print("=" * 74)
    print("Local scoring -- Member 3 validation (final numbers come from evaluation/)")
    print("=" * 74)
    header = f"\n{'function':<14}{'system':<13}{'tests':>7}{'pass':>8}{'cov':>8}{'mutation':>11}"
    print(header)
    print("-" * 74)
    for s in scores:
        print(
            f"{s.function_id:<14}{s.system_variant:<13}"
            f"{s.tests_passed}/{s.tests_collected:<5}"
            f"{s.pass_rate_pct:>7.0f}%"
            f"{s.line_coverage_pct:>7.1f}%"
            f"{s.mutation_score_pct:>9.1f}% ({s.mutants_killed}/{s.mutants_total})"
        )

    # --- per-system means, the RQ1 shape --------------------------------
    by_system: dict[str, list[Score]] = {}
    for s in scores:
        by_system.setdefault(s.system_variant, []).append(s)

    if len(by_system) > 1:
        print("\nMean by system")
        print("-" * 74)
        for system, group in sorted(by_system.items()):
            mutation = sum(s.mutation_score_pct for s in group) / len(group)
            coverage = sum(s.line_coverage_pct for s in group) / len(group)
            print(
                f"  {system:<24} mutation {mutation:>6.1f}%   coverage {coverage:>6.1f}%"
                f"   (n={len(group)})"
            )
        print("\n  n is far too small to compare systems -- this is a smoke test,")
        print("  not a result. RQ1 needs 30 functions x 3 repeats and a Wilcoxon test.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
