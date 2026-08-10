"""
RefinementLoop: generate -> run mutation testing -> identify surviving mutants
-> feed them back through a PromptStrategy -> regenerate -> repeat.

This is intentionally the only place that knows about iteration counting and
the plateau stopping rule; PromptStrategy only knows how to turn mutants into
text, and MutationRunner/LLMClient are injected so this class has no
dependency on mutmut, coverage.py, or a specific model provider.
"""

from __future__ import annotations

import ast

from .config import RefinementConfig
from .interfaces import LLMClient, MutationRunner
from .models import IterationRecord, MutationResult, RunLog
from .prompt_strategies import get_strategy


def _is_valid_pytest_module(code: str) -> bool:
    """Return True only for syntactically valid Python containing test functions."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    return any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
        for node in tree.body
    )


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
        total_cost = 0.0
        llm_calls = 0
        iterations_detail: list[IterationRecord] = []

        result = self.mutation_runner.run(function_source, current_tests)
        initial_score = result.mutation_score_pct
        iteration = 0
        stop_reason = "no_survivors" if not result.survivors else None

        while iteration < self.config.max_iterations and result.survivors:
            iteration += 1
            targets = self.strategy._select_targets(result.survivors, self.config)

            system_prompt, user_prompt = self.strategy.build(
                function_source, function_name, current_tests, result.survivors, self.config
            )
            generated_code, tokens = self.llm_client.generate(user_prompt, system_prompt)
            total_tokens += tokens
            total_cost += float(getattr(self.llm_client, "last_call_cost_usd", 0.0) or 0.0)
            llm_calls += 1

            if self.config.discard_invalid_regeneration and not _is_valid_pytest_module(
                generated_code
            ):
                # Round produced no usable test code. Keep the existing suite
                # rather than overwrite it with prose/an empty response, but
                # still charge the round against iterations/tokens and record
                # that none of this round's targets were killed.
                for m in targets:
                    iterations_detail.append(
                        IterationRecord(
                            iteration=iteration,
                            mutant_id=m.mutant_id,
                            mutant_operator=m.mutant_operator,
                            predicted_state=m.predicted_state,
                            generated_test_code=generated_code,
                            mutant_killed=False,
                        )
                    )
                stop_reason = "invalid_regeneration"
                break  # no point continuing rounds if generation is broken

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
                # RQ3: stop as soon as a round's gain drops below threshold.
                stop_reason = "plateau"
                break

            if not result.survivors:
                stop_reason = "no_survivors"
                break

        if stop_reason is None:
            stop_reason = "max_iterations" if iteration >= self.config.max_iterations else "completed"

        return RunLog(
            function_id=function_id,
            system_variant=self.config.variant,
            # This is the number of *refinement* rounds, so a seed suite that
            # already kills every mutant correctly reports 0.
            iteration_count=iteration,
            total_tokens_used=total_tokens,
            mutation_score_pct=result.mutation_score_pct,
            line_coverage_pct=result.line_coverage_pct,
            estimated_cost_usd=round(total_cost, 6),
            iterations_detail=iterations_detail,
            num_llm_calls=llm_calls,
            pass_rate_pct=result.pass_rate_pct,
            branch_coverage_pct=result.branch_coverage_pct,
            initial_mutation_score_pct=initial_score,
            stop_reason=stop_reason,
        )

    @staticmethod
    def _merge_tests(current_test_code: str, generated_code: str) -> str:
        """Use the regenerated suite while preserving tests the model dropped.

        The prompt asks the model for a complete updated file, but an LLM can
        accidentally omit an existing test. We therefore keep the model output
        when it already contains every previous test function; otherwise we
        append only the missing previous test functions using the AST. This is
        deliberately conservative: imports/helpers remain model-controlled and
        only lost test functions are restored.
        """
        try:
            current_tree = ast.parse(current_test_code)
            generated_tree = ast.parse(generated_code)
        except SyntaxError:
            # Invalid output is handled before this method is called.
            return generated_code

        def tests(tree: ast.Module) -> dict[str, ast.AST]:
            return {
                node.name: node
                for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name.startswith("test_")
            }

        current_tests = tests(current_tree)
        generated_tests = tests(generated_tree)
        missing = [node for name, node in current_tests.items() if name not in generated_tests]
        if not missing:
            return generated_code

        # Append missing tests at module level. ast.unparse is available on all
        # supported Python versions for this project (3.10+).
        generated_tree.body.extend(missing)
        return ast.unparse(generated_tree) + "\n"
