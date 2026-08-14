import json
import subprocess
import sys
from pathlib import Path


SETUP_CFG = """\
[mutmut]
source_paths={module}.py
pytest_add_cli_args_test_selection=tests/
"""


def prepare_mutmut(workdir: Path, function_id: str):
    """
    Create the mutmut 3.x configuration required for this
    isolated evaluation workspace.
    """

    (workdir / "setup.cfg").write_text(
        SETUP_CFG.format(module=function_id),
        encoding="utf-8",
    )


def run_mutation(workdir: Path, function_id: str):
    """
    Run mutmut inside the isolated workspace and calculate
    the mutation score from mutmut's .meta JSON file.

    Returns:
        {
            "mutants_total": int,
            "mutants_killed": int,
            "mutation_score_pct": float
        }
    """

    # Invoke mutmut through the active interpreter. This is reliable in
    # Colab and virtual environments where the console-script directory is
    # not necessarily on PATH.
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mutmut",
            "run",
        ],
        cwd=workdir,
        capture_output=True,
        text=True,
        timeout=1800,
    )

    # mutmut can return a non-zero exit code depending on
    # the mutation results, so we do NOT use check=True here.
    #
    # The actual mutation score is determined from the .meta
    # file below, not from stdout/stderr.

    meta_path = (
        workdir
        / "mutants"
        / f"{function_id}.py.meta"
    )

    if not meta_path.exists():
        raise RuntimeError(
            "mutmut did not produce the expected metadata file:\n"
            f"{meta_path}\n\n"
            f"mutmut stdout:\n{result.stdout}\n\n"
            f"mutmut stderr:\n{result.stderr}"
        )

    # Read mutmut's JSON metadata.
    meta = json.loads(
        meta_path.read_text(
            encoding="utf-8"
        )
    )

    exit_codes = meta.get(
        "exit_code_by_key",
        {}
    )

    total = len(exit_codes)

    # Non-zero exit code means the generated test suite
    # failed against the mutant, therefore the mutant
    # was killed.
    killed = sum(
        1
        for code in exit_codes.values()
        if code != 0
    )

    mutation_score = (
        killed / total * 100
        if total
        else 0.0
    )

    return {
        "mutants_total": total,
        "mutants_killed": killed,
        "mutation_score_pct": round(
            mutation_score,
            2,
        ),
    }