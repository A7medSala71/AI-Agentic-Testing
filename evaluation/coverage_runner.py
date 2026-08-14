import json
import subprocess
import sys
from pathlib import Path


def run_coverage(workdir: Path, function_id: str):
    """
    Run the generated pytest suite against the unmutated source
    and return coverage/pass-rate information.
    """

    venv_bin = Path(sys.executable).parent

    result = subprocess.run(
        [
            str(venv_bin / "python"),
            "-m",
            "coverage",
            "run",
            f"--source={function_id}",
            "-m",
            "pytest",
            "-q",
            "tests/",
        ],
        cwd=workdir,
        capture_output=True,
        text=True,
        timeout=300,
    )

    collected, passed = _parse_pytest_counts(result.stdout)

    subprocess.run(
        [
            str(venv_bin / "python"),
            "-m",
            "coverage",
            "json",
            "-o",
            "cov.json",
        ],
        cwd=workdir,
        capture_output=True,
        text=True,
        timeout=120,
    )

    coverage_pct = 0.0

    cov_path = workdir / "cov.json"

    if cov_path.exists():
        data = json.loads(cov_path.read_text(encoding="utf-8"))
        coverage_pct = data["totals"]["percent_covered"]

    return {
        "tests_collected": collected,
        "tests_passed": passed,
        "line_coverage_pct": round(coverage_pct, 1),
    }


def _parse_pytest_counts(stdout: str):
    passed = 0
    failed = 0
    errors = 0

    for line in reversed(stdout.strip().splitlines()):

        if " passed" in line or " failed" in line or " error" in line:

            for chunk in line.replace("=", " ").split(","):

                parts = chunk.split()

                for i, token in enumerate(parts):

                    if not token.isdigit():
                        continue

                    if i + 1 >= len(parts):
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