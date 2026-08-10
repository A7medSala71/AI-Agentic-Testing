"""Proves the mutation toolchain works, and demonstrates the weak-oracle effect.

Runs two test suites against the same dataset function:

  strong -- asserts the exact returned value
  weak   -- only asserts the call returned something of the right type

Both execute the same lines. Only the strong suite detects the mutants. That
gap is the phenomenon RQ2 is about, and it is why mutation score rather than
coverage is the headline metric in brief section 3.5.

Run:  .venv/bin/python -m baselines.toolchain_check
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from . import config

STRONG = """\
import pytest
from function_03 import arc_length


def test_arc_length_quarter_circle():
    assert arc_length(90, 10) == pytest.approx(15.707963267948966)


def test_arc_length_zero_angle():
    assert arc_length(0, 10) == 0
"""

WEAK = """\
from function_03 import arc_length


def test_arc_length_runs():
    result = arc_length(90, 10)
    assert result is not None
    assert isinstance(result, float)
"""

# mutmut 3.x renamed its config keys. The old names still parse but emit
# DeprecationWarnings: paths_to_mutate -> source_paths, and
# tests_dir -> pytest_add_cli_args_test_selection.
SETUP_CFG = """\
[mutmut]
source_paths=function_03.py
pytest_add_cli_args_test_selection=tests/
"""

# VENV_BIN removed -- see baselines/score.py for why (Colab's system Python
# doesn't put mutmut/python in the same directory as sys.executable).


def mutation_score(workdir: Path) -> tuple[int, int, list[str]]:
    """Return (killed, total, surviving_mutant_ids) from mutmut's meta file.

    mutmut 3.x writes machine-readable results to mutants/<file>.py.meta.
    In `exit_code_by_key`, a non-zero exit code means the test suite failed
    against that mutant, i.e. the mutant was killed.
    """
    meta_path = workdir / "mutants" / "function_03.py.meta"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    exit_codes = meta["exit_code_by_key"]
    killed = sum(1 for code in exit_codes.values() if code != 0)
    survivors = [key for key, code in exit_codes.items() if code == 0]
    return killed, len(exit_codes), survivors


def line_coverage(workdir: Path) -> float:
    subprocess.run(
        [sys.executable, "-m", "coverage", "run",
         "--source=function_03", "-m", "pytest", "-q", "tests/"],
        cwd=workdir, capture_output=True, text=True,
    )
    subprocess.run(
        [sys.executable, "-m", "coverage", "json", "-o", "cov.json"],
        cwd=workdir, capture_output=True, text=True,
    )
    data = json.loads((workdir / "cov.json").read_text(encoding="utf-8"))
    return data["totals"]["percent_covered"]


def run_variant(name: str, test_source: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        (workdir / "tests").mkdir()
        shutil.copy(config.DATASET_DIR / "function_03.py", workdir / "function_03.py")
        (workdir / "tests" / "test_function_03.py").write_text(test_source, encoding="utf-8")
        (workdir / "setup.cfg").write_text(SETUP_CFG, encoding="utf-8")

        coverage_pct = line_coverage(workdir)
        subprocess.run(
            [sys.executable, "-m", "mutmut", "run"],
            cwd=workdir, capture_output=True, text=True,
        )
        killed, total, survivors = mutation_score(workdir)

    return {
        "variant": name,
        "line_coverage_pct": round(coverage_pct, 1),
        "mutation_score_pct": round(killed / total * 100, 1) if total else 0.0,
        "killed": killed,
        "total": total,
        "survivors": len(survivors),
    }


def main() -> int:
    print("=" * 62)
    print("Toolchain check -- mutmut + coverage on function_03 (arc_length)")
    print("=" * 62)

    results = [run_variant("strong oracle", STRONG), run_variant("weak oracle", WEAK)]

    print(f"\n{'variant':<16}{'coverage':>10}{'mutation':>10}{'killed':>10}")
    print("-" * 46)
    for r in results:
        print(
            f"{r['variant']:<16}"
            f"{r['line_coverage_pct']:>9}%"
            f"{r['mutation_score_pct']:>9}%"
            f"{r['killed']:>6}/{r['total']}"
        )

    strong, weak = results
    cov_gap = strong["line_coverage_pct"] - weak["line_coverage_pct"]
    mut_gap = strong["mutation_score_pct"] - weak["mutation_score_pct"]
    print(f"\n  coverage gap : {cov_gap:.1f} points")
    print(f"  mutation gap : {mut_gap:.1f} points")
    print("\n  Coverage barely separates the two suites; mutation score separates")
    print("  them completely. This is the weak-oracle effect behind RQ2.")

    ok = strong["mutation_score_pct"] > weak["mutation_score_pct"]
    print("\n" + ("TOOLCHAIN OK" if ok else "TOOLCHAIN PROBLEM: no separation"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
