"""Mutation-guided iterative refinement controller."""

from __future__ import annotations

from .config import RefinementConfig
from .interfaces import LLMClient, MutationRunner
from .models import IterationRecord, RunLog
from .prompt_strategies import get_strategy


def _looks_like_pytest(code: str) -> bool:
    import ast
    try:
        tree = ast.parse(code or "")
    except SyntaxError:
        return False
    return any(isinstance(node, ast.FunctionDef) and node.name.startswith("test_") for node in tree.body)


class RefinementLoop:
    def __init__(self, config: RefinementConfig, mutation_runner: MutationRunner, llm_client: LLMClient) -> None:
        self.config = config
        self.mutation_runner = mutation_runner
        self.llm_client = llm_client
        self.strategy = get_strategy(config.variant)
        self.final_test_code = ""

    def run(self, function_id: str, function_source: str, function_name: str, initial_test_code: str) -> RunLog:
        current_tests = initial_test_code
        total_tokens = 0
        iterations_detail: list[IterationRecord] = []

        result = self.mutation_runner.run(function_source, current_tests)
        if result.total_mutants <= 0:
            raise RuntimeError(
                f"{function_id}: mutation evaluation produced zero mutants; "
                "refusing to report a 100% mutation score."
            )

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

            if self.config.discard_invalid_regeneration and not _looks_like_pytest(generated_code):
                for m in targets:
                    iterations_detail.append(IterationRecord(
                        iteration=iteration, mutant_id=m.mutant_id,
                        mutant_operator=m.mutant_operator, predicted_state=m.predicted_state,
                        generated_test_code=generated_code, mutant_killed=False))
                stop_reason = "invalid_regeneration"
                break

            current_tests = self._merge_tests(current_tests, generated_code)
            new_result = self.mutation_runner.run(function_source, current_tests)
            if new_result.total_mutants <= 0:
                raise RuntimeError(f"{function_id}: refinement evaluation produced zero mutants.")

            still_surviving_ids = {m.mutant_id for m in new_result.survivors}
            for m in targets:
                iterations_detail.append(IterationRecord(
                    iteration=iteration, mutant_id=m.mutant_id,
                    mutant_operator=m.mutant_operator, predicted_state=m.predicted_state,
                    generated_test_code=generated_code,
                    mutant_killed=m.mutant_id not in still_surviving_ids))

            delta = new_result.mutation_score_pct - result.mutation_score_pct
            result = new_result

            if not result.survivors:
                stop_reason = "no_survivors"
                break
            if delta < self.config.plateau_threshold_pp:
                stop_reason = "plateau"
                break

        if stop_reason is None:
            stop_reason = "max_iterations" if iteration >= self.config.max_iterations and result.survivors else "completed"

        self.final_test_code = current_tests
        return RunLog(
            function_id=function_id,
            system_variant=self.config.variant,
            iteration_count=iteration,
            total_tokens_used=total_tokens,
            mutation_score_pct=result.mutation_score_pct,
            line_coverage_pct=result.line_coverage_pct,
            iterations_detail=iterations_detail,
            pass_rate_pct=result.pass_rate_pct,
            branch_coverage_pct=result.branch_coverage_pct,
            initial_mutation_score_pct=initial_score,
            stop_reason=stop_reason,
            num_llm_calls=int(getattr(self.llm_client, "num_calls", 0)),
        )

    @staticmethod
    def _merge_tests(current_test_code: str, generated_code: str) -> str:
        """Keep newly generated tests while preserving existing test functions.

        The model may accidentally omit a previously useful test. This merge
        avoids silently deleting coverage from earlier rounds.
        """
        import re
        def blocks(code: str):
            matches=list(re.finditer(r"(?m)^def\s+(test_\w+)\s*\(.*?(?=^def\s+test_|\Z)", code, re.S))
            return {m.group(1): m.group(0).rstrip() for m in matches}
        generated=blocks(generated_code)
        existing=blocks(current_test_code)
        missing=[existing[name] for name in existing if name not in generated]
        if not missing:
            return generated_code
        return generated_code.rstrip()+"\n\n"+"\n\n".join(missing)+"\n"
