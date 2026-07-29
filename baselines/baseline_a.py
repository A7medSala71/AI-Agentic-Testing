"""Baseline A -- single-shot LLM test generation (Member 3).

One prompt, one round, no feedback of any kind. Reproduces the most common
current practice and is the floor RQ1 measures against.

Run:  .venv/bin/python -m baselines.baseline_a function_03
      .venv/bin/python -m baselines.baseline_a --all --repeats 3
"""

from __future__ import annotations

from dataclasses import dataclass

from . import prompts
from .llm_client import LLMClient, UsageTracker
from .prompt_context import FunctionContext
from .schemas import ExecutionLog, GeneratedTestSuite


@dataclass
class BaselineResult:
    """One system run over one function, before evaluation."""

    function_id: str
    system_variant: str
    suite: GeneratedTestSuite
    test_source: str
    tracker: UsageTracker

    def to_log(self, mutation_score_pct: float = 0.0, **extra) -> ExecutionLog:
        """Build a schema-valid record. Scores come from Member 2's pipeline.

        `iteration_count` is 1: neither baseline iterates. `iterations_detail`
        is left unset -- it is mutant-centric and meant for Member 4's
        variants, whereas a baseline emits one suite scored against all mutants
        at once.
        """
        summary = self.tracker.summary()
        return ExecutionLog(
            function_id=self.function_id,
            system_variant=self.system_variant,
            iteration_count=1,
            total_tokens_used=summary["total_tokens_used"],
            estimated_cost_usd=summary["estimated_cost_usd"],
            num_llm_calls=summary["num_llm_calls"],
            mutation_score_pct=mutation_score_pct,
            **extra,
        )


def run(ctx: FunctionContext, client: LLMClient | None = None) -> BaselineResult:
    """Generate a test suite for one function in a single call."""
    tracker = UsageTracker()
    client = client or LLMClient(tracker=tracker)

    suite = client.generate(
        system_prompt=prompts.BASELINE_A_SYSTEM,
        user_prompt=prompts.BASELINE_A_USER.format(
            module=ctx.function_id,
            func=ctx.primary_function,
            targets=", ".join(f"`{name}`" for name in ctx.public_functions),
            source=ctx.source_for_prompt,
        ),
        label=f"A:{ctx.function_id}",
        response_model=GeneratedTestSuite,
    )

    return BaselineResult(
        function_id=ctx.function_id,
        system_variant="Baseline_A",
        suite=suite,
        test_source=suite.to_source(),
        tracker=client.tracker,
    )


def main() -> int:
    from . import runner

    parser = runner.build_parser("Baseline A -- single-shot generation")
    args = parser.parse_args()
    contexts = runner.resolve_contexts(args, parser)

    print(runner.logs_dir_status())
    return runner.sweep(
        run_one=lambda ctx, client: run(ctx, client=client),
        system_variant="Baseline_A",
        contexts=contexts,
        repeats=args.repeats,
        mock=args.mock,
        score=args.score,
        force=args.force,
    )


if __name__ == "__main__":
    raise SystemExit(main())
