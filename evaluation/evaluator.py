"""Shared evaluation entry point.

The full experiment runners own their per-function isolated evaluation. This
module provides a lightweight compatible wrapper for callers that still use
the historical evaluation API.
"""
from pathlib import Path
from evaluation.coverage_runner import run_coverage
from evaluation.mutation_runner import run_mutation

DATASET = Path(__file__).resolve().parent.parent / "dataset"

def evaluate(function_name):
    return {
        "function_id": function_name,
        "line_coverage_pct": run_coverage(),
        "mutation_score_pct": run_mutation(),
    }

def evaluate_dataset():
    return [evaluate(p.stem) for p in DATASET.glob("function_*.py")]

if __name__ == "__main__":
    for result in evaluate_dataset():
        print(result)
