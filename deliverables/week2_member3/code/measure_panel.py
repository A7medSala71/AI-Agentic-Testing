"""Measure how often Baseline B's panel actually disagrees (Member 3).

Baseline B scores within a point of Baseline A while spending five times the
LLM calls. The obvious question is *why the panel does not help*, and the
disagreement rate separates two very different answers:

  high disagreement  -> the panelists do find conflicting oracles, and the
                        curator is failing to resolve them usefully
  low disagreement   -> the panelists simply agree, so there is nothing for
                        consensus to add and the four extra calls are wasted

CANDOR reports disagreement in over 70% of cases, which is what motivated the
panel in the first place. If ours comes back near zero, that is a finding about
this code and this model rather than a flaw in the implementation -- and it is
the sentence that explains the headline result.

This runs a **separate sample** and writes nothing to logs/ or
generated_tests/: the reported runs must stay exactly as they were scored.

Run:  .venv/bin/python -m baselines.measure_panel        # 10 functions
      .venv/bin/python -m baselines.measure_panel 30     # all of them
"""

from __future__ import annotations

import sys
from statistics import mean, median

from .baseline_b import run
from .llm_client import LLMClient, UsageTracker
from .prompt_context import all_functions


def main(sample_size: int = 10) -> int:
    contexts = all_functions()[:sample_size]

    print("=" * 66)
    print("Panel disagreement -- Baseline B")
    print("=" * 66)
    print(f"  sample: {len(contexts)} functions, 1 run each")
    print("  (separate sample; logs/ and generated_tests/ are not touched)")
    print()

    rates: list[float] = []
    total = UsageTracker()

    for ctx in contexts:
        client = LLMClient(tracker=UsageTracker())
        try:
            result = run(ctx, client=client)
        except Exception as exc:  # noqa: BLE001 - one failure must not stop the sample
            print(f"  {ctx.function_id:<14} FAILED -- {type(exc).__name__}")
            continue
        rate = result.panel_disagreement_pct or 0.0
        rates.append(rate)
        total.records.extend(result.tracker.records)
        print(f"  {ctx.function_id:<14} {rate:>5.1f}%  ({len(result.suite.tests)} tests)")

    if not rates:
        print("\nNo runs completed.")
        return 1

    print()
    print(f"  mean   {mean(rates):>5.1f}%")
    print(f"  median {median(rates):>5.1f}%")
    print(f"  min    {min(rates):>5.1f}%     max {max(rates):.1f}%")
    unanimous = sum(1 for r in rates if r == 0.0)
    print(f"  fully unanimous: {unanimous} of {len(rates)} functions")

    print()
    print(f"  CANDOR reports >70% disagreement.")
    if mean(rates) < 20:
        print("  Ours is far below that: the panelists mostly agree, so consensus")
        print("  has little to resolve and Baseline B's four extra calls buy little.")
        print("  That explains the headline A-vs-B result rather than contradicting it.")
    elif mean(rates) > 50:
        print("  Comparable to CANDOR: the panel does surface conflicting oracles,")
        print("  so a flat A-vs-B result points at the curator rather than the panel.")
    else:
        print("  Between the two regimes -- report the figure and let it stand.")

    print(f"\n  cost of this sample: {total.summary()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 10))
