import json
import shutil
import tempfile
from pathlib import Path

from evaluation.coverage_runner import run_coverage
from evaluation.mutation_runner import (
    prepare_mutmut,
    run_mutation,
)


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET = BASE_DIR / "dataset"
GENERATED_TESTS = BASE_DIR / "generated_tests"
LOGS = BASE_DIR / "logs"


def update_log(result):
    """
    Write evaluation metrics back to the corresponding execution log.
    """

    function_id = result["function_id"]
    system_variant = result["system_variant"]

    # We currently evaluate one run at a time.
    # The run number is supplied separately.
    run_index = result["run_index"]

    log_file = (
        LOGS
        / f"{function_id}__{system_variant}__run{run_index}.json"
    )

    if not log_file.exists():
        print(f"Log not found: {log_file}")
        return False

    record = json.loads(
        log_file.read_text(encoding="utf-8")
    )

    record["line_coverage_pct"] = result[
        "line_coverage_pct"
    ]

    record["mutation_score_pct"] = result[
        "mutation_score_pct"
    ]

    record["pass_rate_pct"] = result[
        "pass_rate_pct"
    ]

    log_file.write_text(
        json.dumps(
            record,
            indent=2
        ) + "\n",
        encoding="utf-8",
    )

    return True


def evaluate_suite(test_file: Path):

    parts = test_file.stem.split("__")

    if len(parts) < 3:
        return None

    function_id = parts[0]
    system_variant = parts[1]
    run_index = int(
        parts[2].replace("run", "")
    )

    source_file = DATASET / f"{function_id}.py"

    if not source_file.exists():
        print(f"Missing source: {source_file}")
        return None

    test_source = test_file.read_text(
        encoding="utf-8"
    )

    with tempfile.TemporaryDirectory() as tmp:

        workdir = Path(tmp)

        # Create tests directory
        tests_dir = workdir / "tests"
        tests_dir.mkdir()

        # Copy target function
        shutil.copy(
            source_file,
            workdir / f"{function_id}.py",
        )

        # Write generated test
        (
            tests_dir / f"test_{function_id}.py"
        ).write_text(
            test_source,
            encoding="utf-8",
        )

        # Prepare mutmut configuration
        prepare_mutmut(
            workdir,
            function_id,
        )

        # Coverage + pytest
        coverage = run_coverage(
            workdir,
            function_id,
        )

        # Mutation testing
        mutation = run_mutation(
            workdir,
            function_id,
        )

    tests_collected = coverage["tests_collected"]
    tests_passed = coverage["tests_passed"]

    pass_rate = (
        tests_passed / tests_collected * 100
        if tests_collected
        else 0.0
    )

    result = {
        "function_id": function_id,
        "system_variant": system_variant,
        "run_index": run_index,

        "iteration_count": 1,
        "total_tokens_used": 0,
        "estimated_cost_usd": 0.0,

        "line_coverage_pct": coverage[
            "line_coverage_pct"
        ],

        "mutation_score_pct": mutation[
            "mutation_score_pct"
        ],

        "pass_rate_pct": pass_rate,

        "iterations_detail": [],
    }

    update_log(result)

    print(result)

    # print(
    #     f"{function_id:<14}"
    #     f"{system_variant:<15}"
    #     f"run{run_index:<5}"
    #     f"coverage={coverage['line_coverage_pct']:>6.1f}% "
    #     f"mutation={mutation['mutation_score_pct']:>6.1f}% "
    #     f"pass={pass_rate:>6.1f}%"
    # )

    return result


def evaluate_all():

    if not GENERATED_TESTS.exists():
        print("generated_tests/ not found.")
        return []

    results = []

    test_files = sorted(
        GENERATED_TESTS.glob("*__test.py")
    )

    for test_file in test_files:

        if "MOCK" in test_file.stem:
            continue

        result = evaluate_suite(test_file)

        if result is not None:
            results.append(result)

    return results


if __name__ == "__main__":

    print("Starting evaluation pipeline...")
    print(f"Dataset: {DATASET}")
    print(f"Generated tests: {GENERATED_TESTS}")

    # results = evaluate_all()

    # print()
    # print(f"Evaluated {len(results)} test suites.")

    test_file = GENERATED_TESTS / "function_03__Baseline_A__run1__test.py"

    result = evaluate_suite(test_file)

    print(result)
