"""Builds the source-code context handed to the model (Member 3).

Two dataset properties force decisions here, and both must be applied
identically across Baseline A, Baseline B and Member 4's variants or the RQ1
comparison stops being like-for-like:

1. Every function ships with doctests in its docstring, i.e. worked
   input -> output pairs. Those are oracles. Handing them to the model tests
   transcription, not oracle reasoning. Controlled by config.INCLUDE_DOCTESTS.

2. Several files hold more than one public function plus non-testable
   scaffolding (`benchmark`, `if __name__ == "__main__"`). Those are stripped.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

from . import config


@dataclass
class FunctionContext:
    """The prompt-ready view of one dataset file."""

    function_id: str
    source_path: Path
    public_functions: list[str]
    source_for_prompt: str

    @property
    def primary_function(self) -> str:
        return self.public_functions[0] if self.public_functions else self.function_id


def _strip_doctests(docstring: str) -> str:
    """Drop >>> example blocks, keep the prose description."""
    kept: list[str] = []
    in_example = False
    for line in docstring.splitlines():
        stripped = line.strip()
        if stripped.startswith(">>>"):
            in_example = True
            continue
        if in_example:
            # An example block runs until a blank line ends it.
            if not stripped:
                in_example = False
            continue
        kept.append(line)
    return "\n".join(kept).rstrip()


class _Transformer(ast.NodeTransformer):
    def __init__(self, include_doctests: bool):
        self.include_doctests = include_doctests
        self.public_functions: list[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):  # noqa: N802
        if node.name in config.EXCLUDE_FROM_PROMPT:
            return None
        if not node.name.startswith("_"):
            self.public_functions.append(node.name)
        if not self.include_doctests:
            self._rewrite_docstring(node)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef):  # noqa: N802
        if not node.name.startswith("_"):
            self.public_functions.append(node.name)
        if not self.include_doctests:
            self._rewrite_docstring(node)
        self.generic_visit(node)
        return node

    def _rewrite_docstring(self, node) -> None:
        doc = ast.get_docstring(node, clean=False)
        if doc is None:
            return
        cleaned = _strip_doctests(doc)
        if cleaned.strip():
            node.body[0] = ast.Expr(value=ast.Constant(value=cleaned))
        else:
            node.body.pop(0)
            if not node.body:
                node.body.append(ast.Pass())


def build_context(path: Path, include_doctests: bool | None = None) -> FunctionContext:
    """Parse a dataset file into the exact source text the model will see."""
    if include_doctests is None:
        include_doctests = config.INCLUDE_DOCTESTS

    tree = ast.parse(path.read_text(encoding="utf-8"))

    # Drop the `if __name__ == "__main__":` block; it is not under test.
    tree.body = [
        n
        for n in tree.body
        if not (
            isinstance(n, ast.If)
            and isinstance(n.test, ast.Compare)
            and isinstance(n.test.left, ast.Name)
            and n.test.left.id == "__name__"
        )
    ]

    transformer = _Transformer(include_doctests)
    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)

    return FunctionContext(
        function_id=path.stem,
        source_path=path,
        public_functions=transformer.public_functions,
        source_for_prompt=ast.unparse(tree),
    )


def all_functions() -> list[FunctionContext]:
    """Every dataset file, in stable function_01..function_30 order."""
    return [build_context(p) for p in sorted(config.DATASET_DIR.glob("function_*.py"))]
