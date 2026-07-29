"""Writes run records into logs/ against the team schema (Member 3).

Every log is validated with jsonschema before it hits disk. A run that would
not validate is a run that has to be repeated, and at 30 functions x 3 systems
x 3 repeats that is expensive to discover late.
"""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft7Validator

from . import config
from .schemas import ExecutionLog

_validator: Draft7Validator | None = None


def _get_validator() -> Draft7Validator:
    global _validator
    if _validator is None:
        schema = json.loads(config.SCHEMA_PATH.read_text(encoding="utf-8"))
        _validator = Draft7Validator(schema)
    return _validator


def log_filename(function_id: str, system_variant: str, run_index: int) -> str:
    """`function_03__Baseline_A__run1.json` -- greppable and sortable."""
    return f"{function_id}__{system_variant}__run{run_index}.json"


def validate(log: ExecutionLog) -> list[str]:
    """Return schema violations, empty when the record is valid."""
    payload = log.model_dump(exclude_none=True)
    return [
        f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
        for e in _get_validator().iter_errors(payload)
    ]


def write(log: ExecutionLog, run_index: int, logs_dir: Path | None = None) -> Path:
    """Validate then write one run record. Raises if it does not conform."""
    errors = validate(log)
    if errors:
        raise ValueError(
            f"ExecutionLog for {log.function_id}/{log.system_variant} "
            f"violates the team schema: " + "; ".join(errors)
        )

    target_dir = logs_dir or config.LOGS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / log_filename(log.function_id, log.system_variant, run_index)
    path.write_text(
        json.dumps(log.model_dump(exclude_none=True), indent=2) + "\n",
        encoding="utf-8",
    )
    return path
