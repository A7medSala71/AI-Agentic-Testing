"""Live-API verification -- the one Week 1 item that needs a real key.

Everything else in this folder is verified in mock mode. This closes the three
open items in docs/week1_member3_report.md section 6:

  1. Schema-conformance rate. Brief section 4 warns Gemini is "less consistent"
     at structured output. Baseline B depends on it for all 5 of its calls, so
     a rate materially below 100% means either a retry wrapper or a different
     model, and it is much cheaper to learn that now than in Week 4.
  2. Real token counts, including reasoning tokens.
  3. Whether generated tests actually run against the real source.

Run:  .venv/bin/python -m baselines.live_check          # 5 calls
      .venv/bin/python -m baselines.live_check 10       # 10 calls
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from . import config
from .llm_client import LLMClient, UsageTracker
from .prompt_context import build_context
from .schemas import GeneratedTestSuite

SYSTEM_PROMPT = (
    "You are an expert Python test engineer. Given a function, write a pytest "
    "suite that maximises fault detection: cover nominal cases, boundaries and "
    "error conditions. Use bare `assert`. Use pytest.approx for float "
    "comparisons. Use explicit named imports -- never `import *`.\n"
    "Import the module under test by the EXACT module name you are given. "
    "Never invent a module name."
)

# The model cannot see the filename, only the source. Left to guess it invents
# one -- observed: 'solution', 'arc_length_module' -- and every generated suite
# then fails with ModuleNotFoundError. The module name must be stated.
USER_PROMPT = """\
The module under test is saved as `{module}.py` and must be imported as `{module}`.
For example: `from {module} import {func}`.

Write a pytest suite for it:

```python
{source}
```"""

TARGET = "function_03"


def main(num_calls: int = 5) -> int:
    if not config.has_api_key():
        print("No API key found.\n")
        print("  1. Get a free key at https://aistudio.google.com/apikey")
        print("  2. cp .env.example .env")
        print(f"  3. Put it in .env as {config.API_KEY_ENV}=<your key>")
        print("\n.env is gitignored. Never commit a key to this repo -- it is public,")
        print("and GitHub's secret scanning will get the key auto-revoked by Google.")
        return 1

    ctx = build_context(config.DATASET_DIR / f"{TARGET}.py")
    tracker = UsageTracker()
    client = LLMClient(tracker=tracker)

    print("=" * 62)
    print("Live API check")
    print("=" * 62)
    print(f"  model       : {config.MODEL_ID}")
    print(f"  target      : {TARGET} ({', '.join(ctx.public_functions)})")
    print(f"  calls       : {num_calls}")
    print(f"  temperature : {config.TEMPERATURE}")
    print(f"  doctests    : {'included' if config.INCLUDE_DOCTESTS else 'stripped'}")

    conformant = 0
    failures: list[str] = []
    suites: list[GeneratedTestSuite] = []

    print("\nSchema conformance")
    print("-" * 62)
    for i in range(1, num_calls + 1):
        try:
            suite = client.generate(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=USER_PROMPT.format(
                    module=ctx.function_id,
                    func=ctx.primary_function,
                    source=ctx.source_for_prompt,
                ),
                response_model=GeneratedTestSuite,
                label=f"live:{i}",
            )
            suites.append(suite)
            conformant += 1
            print(f"  call {i}: OK -- {len(suite.tests)} tests")
        except Exception as exc:  # noqa: BLE001 - reporting, not handling
            failures.append(f"call {i}: {type(exc).__name__}: {exc}")
            print(f"  call {i}: FAILED -- {type(exc).__name__}")

    rate = conformant / num_calls * 100
    print(f"\n  conformance rate: {conformant}/{num_calls} ({rate:.0f}%)")
    if failures:
        print("\n  failures:")
        for f in failures:
            print(f"    {f}")

    # --- token accounting -------------------------------------------------
    print("\nToken accounting (real)")
    print("-" * 62)
    s = tracker.summary()
    for key, value in s.items():
        print(f"  {key:<20} {value}")
    if conformant:
        print(f"  {'avg tokens/call':<20} {s['total_tokens_used'] // conformant}")
        per_fn = s["estimated_cost_usd"] / conformant
        print(f"  {'cost per call':<20} ${per_fn:.6f}")
        # 30 functions x 3 repeats, Baseline A = 1 call, Baseline B = 5 calls
        projected = per_fn * 30 * 3 * (1 + config.BASELINE_B_EXPECTED_CALLS)
        print(f"  {'projected A+B total':<20} ${projected:.2f}  (30 fn x 3 repeats)")

    # --- do the generated tests actually run? -----------------------------
    print("\nGenerated tests run against real source")
    print("-" * 62)
    passing = 0
    for idx, suite in enumerate(suites, start=1):
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            (workdir / f"{TARGET}.py").write_text(
                (config.DATASET_DIR / f"{TARGET}.py").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            try:
                source = suite.to_source()
            except ValueError as exc:
                print(f"  suite {idx}: REJECTED -- {exc}")
                continue
            (workdir / f"test_{TARGET}.py").write_text(source, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", f"test_{TARGET}.py"],
                cwd=workdir, capture_output=True, text=True,
            )
            last = (result.stdout.strip().splitlines() or ["no output"])[-1]
            ok = result.returncode == 0
            passing += ok
            print(f"  suite {idx}: {'PASS' if ok else 'FAIL'} -- {last}")
            if not ok:
                for line in result.stdout.splitlines():
                    if "Error" in line or "error" in line.lower():
                        print(f"           {line.strip()[:100]}")
                        break

    if suites:
        print(f"\n  pass rate: {passing}/{len(suites)} ({passing / len(suites) * 100:.0f}%)")

    # --- sample -----------------------------------------------------------
    if suites:
        print("\nSample generated suite (first call)")
        print("-" * 62)
        for line in suites[0].to_source().splitlines():
            print(f"  {line}")

    # --- verdict ----------------------------------------------------------
    print("\n" + "=" * 62)
    if rate == 100:
        print("Structured output is reliable at this sample size. No retry wrapper")
        print("needed yet -- re-check if failures appear at full scale.")
    elif rate >= 80:
        print(f"Conformance {rate:.0f}% -- add a retry wrapper to LLMClient.generate")
        print("before full-scale runs, and report the rate in the paper.")
    else:
        print(f"Conformance {rate:.0f}% -- too low. Raise with the team: either")
        print("heavier prompt engineering or a different model (brief section 4).")
    print("=" * 62)
    return 0 if conformant else 1


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    raise SystemExit(main(count))
