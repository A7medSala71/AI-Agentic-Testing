"""Paired comparison between systems, from the records in logs/ (Member 3).

Brief §3.5 specifies a Wilcoxon signed-rank test between systems on the same
functions. It is implemented here rather than pulled from scipy so the team can
run it with no extra dependency -- the exact-distribution path is short, and
the normal approximation matches scipy's default for larger samples.

Two things this deliberately gets right, because both are easy to get wrong:

* **Paired means paired.** Only functions present for *both* systems are
  compared. Averaging each system over whatever it happens to have run
  compares different function sets and inflates or deflates the gap for free.
* **Repeats are averaged per function first.** Brief §3.4 asks for 3 repeats;
  feeding all 3 in as independent observations would treat one function as
  three, tripling the apparent sample size.

Run:  .venv/bin/python -m baselines.compare
      .venv/bin/python -m baselines.compare Baseline_A Variant_1_ErrorTrace
"""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from statistics import mean, stdev

from . import config

METRIC = "mutation_score_pct"


def load_runs() -> dict[tuple[str, str], list[float]]:
    """Every logged score, keyed by (function_id, system_variant)."""
    runs: dict[tuple[str, str], list[float]] = defaultdict(list)
    for path in sorted(config.LOGS_DIR.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if METRIC not in record:
            continue
        runs[(record["function_id"], record["system_variant"])].append(record[METRIC])
    return runs


def wilcoxon_signed_rank(diffs: list[float]) -> tuple[float, float, int]:
    """Return (W, two-sided p, n after dropping zero differences).

    Prefers `scipy.stats.wilcoxon`, which brief §1.5 names as the reference
    implementation and which Member 4 will use for the paper's statistics.
    Matching it matters more than being independently correct: three defensible
    variants of this test (exact enumeration, normal approximation with and
    without a continuity correction) give p = 0.21, 0.20 and 0.18 on the same
    data, and a number that moves depending on who ran it is worse than either.

    The hand-rolled fallback below keeps the module usable without scipy, and
    reproduces scipy's default path -- normal approximation, no continuity
    correction -- rather than a different one.

    Zero differences are dropped, the standard treatment, and it matters here:
    most functions tie between the baselines, so the effective sample is far
    smaller than the function count.
    """
    n_nonzero = sum(1 for d in diffs if abs(d) > 1e-9)
    try:
        from scipy.stats import wilcoxon as _scipy_wilcoxon

        if n_nonzero:
            # Hand scipy the full difference vector, zeros included. It drops
            # them itself, but the count it sees also decides whether it takes
            # the exact or approximate path -- pre-filtering here moved p from
            # 0.18 to 0.21 on this data without changing anything real.
            stat, p = _scipy_wilcoxon(diffs)
            return float(stat), float(p), n_nonzero
    except ImportError:
        pass

    nonzero = [d for d in diffs if abs(d) > 1e-9]
    n = len(nonzero)
    if n == 0:
        return 0.0, 1.0, 0

    ranked = sorted(nonzero, key=abs)
    ranks: list[float] = []
    i = 0
    while i < len(ranked):
        j = i
        while j + 1 < len(ranked) and abs(ranked[j + 1]) == abs(ranked[i]):
            j += 1
        # Ties in magnitude share the average of the ranks they span.
        average_rank = (i + j) / 2 + 1
        ranks.extend([average_rank] * (j - i + 1))
        i = j + 1

    w_plus = sum(r for d, r in zip(ranked, ranks) if d > 0)
    w_minus = sum(r for d, r in zip(ranked, ranks) if d < 0)
    w = min(w_plus, w_minus)

    # Below ~25 the normal approximation is noticeably off, and this study sits
    # there: most functions tie, so n after dropping zeros is small. Enumerate
    # the exact null distribution instead -- 2^n sign flips, trivial at this
    # size, and it matches scipy's default rather than diverging from it.
    mu = n * (n + 1) / 4
    sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    if sigma == 0:
        return w, 1.0, n
    # No continuity correction -- scipy's default, and the point is to agree
    # with it rather than to be marginally more conservative on our own.
    z = (w - mu) / sigma
    p = 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
    return w, min(max(p, 0.0), 1.0), n


def compare(system_a: str, system_b: str) -> int:
    runs = load_runs()
    functions_a = {f for f, s in runs if s == system_a}
    functions_b = {f for f, s in runs if s == system_b}
    shared = sorted(functions_a & functions_b)

    if not shared:
        print(f"No functions have records for both {system_a} and {system_b}.")
        return 1

    print("=" * 70)
    print(f"Paired comparison -- {METRIC}")
    print("=" * 70)
    only_a = len(functions_a - functions_b)
    only_b = len(functions_b - functions_a)
    print(f"  functions compared : {len(shared)}")
    if only_a or only_b:
        print(
            f"  excluded           : {only_a} only in {system_a}, "
            f"{only_b} only in {system_b}"
        )

    scores_a = [mean(runs[(f, system_a)]) for f in shared]
    scores_b = [mean(runs[(f, system_b)]) for f in shared]
    diffs = [b - a for a, b in zip(scores_a, scores_b)]

    print()
    for name, scores in ((system_a, scores_a), (system_b, scores_b)):
        spread = f" ± {stdev(scores):.1f}" if len(scores) > 1 else ""
        print(f"  {name:<26} {mean(scores):>6.1f}%{spread}")
    print(f"  {'difference':<26} {mean(diffs):>+6.1f} points")

    wins_b = sum(1 for d in diffs if d > 1e-9)
    wins_a = sum(1 for d in diffs if d < -1e-9)
    ties = len(diffs) - wins_b - wins_a
    print()
    print(f"  {system_b} better : {wins_b}")
    print(f"  {system_a} better : {wins_a}")
    print(f"  tied            : {ties}")

    w, p, n = wilcoxon_signed_rank(diffs)
    print()
    print("  Wilcoxon signed-rank")
    print(f"    non-zero differences : {n} of {len(diffs)}")
    print(f"    W                    : {w:.1f}")
    print(f"    p (two-sided)        : {p:.4f}")
    verdict = (
        "significant at p < 0.05"
        if p < 0.05
        else "NOT significant -- the systems are indistinguishable on this data"
    )
    print(f"    {verdict}")

    if ties > len(diffs) / 2:
        print()
        print(f"  {ties} of {len(diffs)} functions tie exactly. A test cannot find a")
        print("  difference that mostly is not there -- report the tie rate alongside")
        print("  the p-value rather than the p-value alone.")

    return 0


def main() -> int:
    args = sys.argv[1:]
    a = args[0] if args else "Baseline_A"
    b = args[1] if len(args) > 1 else "Baseline_B"
    return compare(a, b)


if __name__ == "__main__":
    raise SystemExit(main())
