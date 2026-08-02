"""
RefinementLoop: generate -> run mutation testing -> identify surviving mutants
-> feed them back through a PromptStrategy -> regenerate -> repeat.

This is intentionally the only place that knows about iteration counting and
the plateau stopping rule; PromptStrategy only knows how to turn mutants into
text, and MutationRunner/LLMClient are injected so this class has no
dependency on mutmut, coverage.py, or a specific model provider.
"""

from __future__ import annotations

from .config import RefinementConfig
from .interfaces import LLMClient, MutationRunner
from .models import IterationRecord, MutationResult, RunLog
from .prompt_strategies import get_strategy


class RefinementLoop:
    def __init__(
        self,
        config: RefinementConfig,
        mutation_runner: MutationRunner,
        llm_client: LLMClient,
    ) -> None:
        self.config = config
        self.mutation_runner = mutation_runner
        self.llm_client = llm_client
        self.strategy = get_strategy(config.variant)

    def run(
        self,
        function_id: str,
        function_source: str,
        function_name: str,
        initial_test_code: str,
    ) -> RunLog:
        """
        Runs the full refinement procedure for one function and returns a
        RunLog ready to serialize against execution_log_schema.json.
        """
        current_tests = initial_test_code
        total_tokens = 0
        iterations_detail: list[IterationRecord] = []

        result = self.mutation_runner.run(function_source, current_tests)
        iteration = 0

        while iteration < self.config.max_iterations and result.survivors:
            iteration += 1
            targets = self.strategy._select_targets(result.survivors, self.config)

            system_prompt, user_prompt = self.strategy.build(
                function_source, function_name, current_tests, result.survivors, self.config
            )
            generated_code, tokens = self.llm_client.generate(user_prompt, system_prompt)
            total_tokens += tokens

            current_tests = self._merge_tests(current_tests, generated_code)
            new_result = self.mutation_runner.run(function_source, current_tests)

            still_surviving_ids = {m.mutant_id for m in new_result.survivors}
            for m in targets:
                iterations_detail.append(
                    IterationRecord(
                        iteration=iteration,
                        mutant_id=m.mutant_id,
                        mutant_operator=m.mutant_operator,
                        predicted_state=m.predicted_state,
                        generated_test_code=generated_code,
                        mutant_killed=m.mutant_id not in still_surviving_ids,
                    )
                )

            delta = new_result.mutation_score_pct - result.mutation_score_pct
            result = new_result

            if delta < self.config.plateau_threshold_pp:
                # RQ3: stop as soon as a round's gain drops below threshold,
                # this round's iteration count IS the plateau point for this file.
                break

        return RunLog(
            function_id=function_id,
            system_variant=self.config.variant,
            iteration_count=max(iteration, 1),
            total_tokens_used=total_tokens,
            mutation_score_pct=result.mutation_score_pct,
            line_coverage_pct=result.line_coverage_pct,
            iterations_detail=iterations_detail,
        )

    @staticmethod
    def _merge_tests(current_test_code: str, generated_code: str) -> str:
        """
        Combine the previous test file with the newly generated one.

        v0.1 policy: the LLM is prompted (see prompt_strategies.py) to return
        the *complete updated file*, so we simply take its output as the new
        current_tests, keeping the loop's job to just track history/tokens.
        If v0.1 testing (Week 3) shows the model tends to drop working tests
        instead of extending them, swap this for an AST-level merge (see
        Section 1.2 of the brief) that unions test functions by name instead
        of a full replace.
        """
        return generated_code
