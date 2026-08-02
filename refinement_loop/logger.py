"""
Writes a RunLog to disk in the shared JSON format Member 1's schema defines,
and validates it against execution_log_schema.json when the `jsonschema`
package is available (skips validation with a warning otherwise, so this
never becomes a hard dependency for people running the loop locally).
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import RunLog

DEFAULT_SCHEMA_PATH = (
    Path(__file__).resolve().parents[1] / "schema" / "execution_log_schema.json"
)


def write_run_log(run_log: RunLog, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(run_log.to_dict(), indent=2))
    return output_path


def validate_run_log(run_log: RunLog, schema_path: str | Path = DEFAULT_SCHEMA_PATH) -> bool:
    """
    Returns True if valid (or if jsonschema isn't installed, in which case it
    prints a warning and returns True so this never blocks a local run).
    """
    try:
        import jsonschema
    except ImportError:
        print("[refinement_loop.logger] jsonschema not installed; skipping validation.")
        return True

    schema = json.loads(Path(schema_path).read_text())
    jsonschema.validate(instance=run_log.to_dict(), schema=schema)
    return True
