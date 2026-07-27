from pathlib import Path

DATASET = Path(__file__).parent.parent / "dataset"

from evaluation.coverage_runner.py import run_coverage
from evaluation.mutation_runner.py import run_mutation


def evaluate(function_name):
    coverage = run_coverage()

    mutation = run_mutation()

    return {
        "function_id": function_name,
        "line_coverage_pct": coverage,
        "mutation_score_pct": mutation
    }


def evaluate_dataset():

    results = []

    for file in DATASET.glob("*.py"):
        results.append(evaluate(file.stem))

    print(DATASET)
    print(list(DATASET.glob("*.py")))

    return results


if __name__ == "__main__":
    results = evaluate_dataset()

    for result in results:
        print(result)

# if __name__ == "__main__":
#     print("Evaluator started")

#     print(DATASET)
#     print(list(DATASET.glob("*.py")))

#     results = evaluate_dataset()

#     for result in results:
#         print(result)