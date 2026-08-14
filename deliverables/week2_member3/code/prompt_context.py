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


def _is_test_class(node: ast.ClassDef) -> bool:
    """True for the dataset's own test scaffolding, e.g. function_25's
    `class Test(unittest.TestCase)`. It is importable, so the depth check does
    not catch it, but it is test code rather than code under test -- asking the
    model to write tests for it produces tests of tests."""
    for base in node.bases:
        name = base.attr if isinstance(base, ast.Attribute) else getattr(base, "id", "")
        if name == "TestCase":
            return True
    return node.name.startswith("Test") or node.name.endswith("Test")


class _Transformer(ast.NodeTransformer):
    """Strips scaffolding and doctests, and collects the importable targets.

    Only **module-level** names are collected. A nested helper is not
    importable -- `merge` inside `merge_sort` cannot be reached by
    `from function_15 import merge` -- and neither is a method inside a class.
    Listing one as a target makes the model write an import that raises
    ImportError, which fails the whole suite before a single assertion runs.
    """

    def __init__(self, include_doctests: bool):
        self.include_doctests = include_doctests
        self.public_functions: list[str] = []
        self._depth = 0

    def visit_FunctionDef(self, node: ast.FunctionDef):  # noqa: N802
        if self._depth == 0 and node.name in config.EXCLUDE_FROM_PROMPT:
            return None
        if self._depth == 0 and not node.name.startswith("_"):
            self.public_functions.append(node.name)
        if not self.include_doctests:
            self._rewrite_docstring(node)
        self._depth += 1
        self.generic_visit(node)
        self._depth -= 1
        return node

    def visit_AsyncFunctionDef(self, node):  # noqa: N802
        return self.visit_FunctionDef(node)

    def visit_ClassDef(self, node: ast.ClassDef):  # noqa: N802
        if self._depth == 0 and not node.name.startswith("_") and not _is_test_class(node):
            self.public_functions.append(node.name)
        if not self.include_doctests:
            self._rewrite_docstring(node)
        self._depth += 1
        self.generic_visit(node)
        self._depth -= 1
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
