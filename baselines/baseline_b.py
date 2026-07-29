"""Baseline B -- one-shot multi-agent consensus (Member 3).

A deliberately simplified CANDOR: propose -> critique x N -> finalise, in a
single pass with no mutation feedback.

    propose (1 call)
       |
       +--> panelist 1 --+
       +--> panelist 2 --+--> curator (1 call) --> final suite
       +--> panelist 3 --+
            (N calls, independent)

Design decisions and their justification:

* **Panel size 3.** CANDOR tested 1-5 and found no significant gain past 3.

* **No Interpreter agents.** CANDOR ran a second cheap LLM after each panelist
  purely to compress DeepSeek R1's 10k-token reasoning into
  {oracle_correct, reasoning, confidence}. Schema-constrained output returns
  those fields directly, so Baseline B is 5 calls rather than CANDOR's 8.

* **The curator reasons, it does not vote.** CANDOR reports panelist
  disagreement in over 70% of cases. Their ablation puts plain majority voting
  at -0.014 oracle correctness versus -0.086 for dropping the panel entirely,
  so the panel existing matters more than the merge strategy -- but the curator
  is implemented as a reasoning merge, as in the paper.

* **Panelists are blind to each other.** As in CANDOR, there are no debate
  rounds; the "discussion" happens inside the curator.

* **Single pass, by design.** CANDOR's Step II is an iterative coverage loop
  worth -0.111 mutation score in their ablation. RQ1 asks whether
  mutation-guided iteration beats consensus alone, so the comparator must not
  iterate. Baseline B is therefore a consensus-only ABLATION of CANDOR, not a
  reimplementation, and the paper must say so.

Run:  .venv/bin/python -m baselines.baseline_b function_03
      .venv/bin/python -m baselines.baseline_b --all --repeats 3
"""

from __future__ import annotations

from . import config, prompts
from .baseline_a import BaselineResult
from .llm_client import LLMClient, UsageTracker
from .prompt_context import FunctionContext
from .schemas import GeneratedTestSuite, PanelReview


def run(
    ctx: FunctionContext,
    client: LLMClient | None = None,
    panel_size: int | None = None,
) -> BaselineResult:
    """propose -> critique x N -> finalise, one pass."""
    panel_size = panel_size or config.PANEL_SIZE
    client = client or LLMClient(tracker=UsageTracker())

    common = {
        "module": ctx.function_id,
        "func": ctx.primary_function,
        "source": ctx.source_for_prompt,
    }

    # --- 1. propose ------------------------------------------------------
    proposed = client.generate(
        system_prompt=prompts.BASELINE_B_PROPOSE_SYSTEM,
        user_prompt=prompts.BASELINE_B_PROPOSE_USER.format(
            targets=", ".join(f"`{name}`" for name in ctx.public_functions),
            **common,
        ),
        response_model=GeneratedTestSuite,
        label=f"B:propose:{ctx.function_id}",
    )
    proposed_source = proposed.to_source()

    # --- 2. critique, independently --------------------------------------
    reviews: list[PanelReview] = []
    for panelist_id in range(1, panel_size + 1):
        review = client.generate(
            system_prompt=prompts.BASELINE_B_CRITIQUE_SYSTEM.format(
                panelist_id=panelist_id, panel_size=panel_size
            ),
            user_prompt=prompts.BASELINE_B_CRITIQUE_USER.format(
                tests=proposed_source, **common
            ),
            response_model=PanelReview,
            label=f"B:panel{panelist_id}:{ctx.function_id}",
        )
        reviews.append(review)

    # --- 3. finalise ------------------------------------------------------
    final = client.generate(
        system_prompt=prompts.BASELINE_B_FINALISE_SYSTEM.format(panel_size=panel_size),
        user_prompt=prompts.BASELINE_B_FINALISE_USER.format(
            tests=proposed_source,
            reviews=prompts.format_reviews(reviews),
            **common,
        ),
        response_model=GeneratedTestSuite,
        label=f"B:curator:{ctx.function_id}",
    )

    return BaselineResult(
        function_id=ctx.function_id,
        system_variant="Baseline_B",
        suite=final,
        test_source=final.to_source(),
        tracker=client.tracker,
    )


def panel_disagreement(reviews: list[PanelReview]) -> float:
    """Share of tests the panel did not unanimously agree on.

    CANDOR reports disagreement in over 70% of cases. Recording our own figure
    lets the paper state whether the panel is doing real work or rubber-stamping
    -- and if it is near zero, Baseline B is 5 calls buying nothing, which is
    itself a finding worth reporting.
    """
    verdicts: dict[str, set[bool]] = {}
    for review in reviews:
        for judgement in review.judgements:
            verdicts.setdefault(judgement.test_name, set()).add(judgement.oracle_correct)
    if not verdicts:
        return 0.0
    split = sum(1 for outcomes in verdicts.values() if len(outcomes) > 1)
    return split / len(verdicts) * 100


def main() -> int:
    from . import runner

    parser = runner.build_parser("Baseline B -- one-shot consensus")
    parser.add_argument("--panel", type=int, default=config.PANEL_SIZE)
    args = parser.parse_args()
    contexts = runner.resolve_contexts(args, parser)

    print(runner.logs_dir_status())
    return runner.sweep(
        run_one=lambda ctx, client: run(ctx, client=client, panel_size=args.panel),
        system_variant="Baseline_B",
        contexts=contexts,
        repeats=args.repeats,
        mock=args.mock,
        score=args.score,
        force=args.force,
    )


if __name__ == "__main__":
    raise SystemExit(main())
