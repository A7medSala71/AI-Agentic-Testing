"""Central configuration for Baseline A and Baseline B (Member 3).

Every knob the two baselines depend on lives here so that experimental
settings are declared in one place and can be cited directly in the paper.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

# --- Paths -----------------------------------------------------------------
DATASET_DIR = REPO_ROOT / "dataset"
LOGS_DIR = REPO_ROOT / "logs"
SCHEMA_PATH = REPO_ROOT / "schema" / "execution_log_schema.json"
GENERATED_TESTS_DIR = REPO_ROOT / "generated_tests"

# --- LLM -------------------------------------------------------------------
PROVIDER = "gemini"
API_KEY_ENV = "GEMINI_API_KEY"

# The project brief names "Gemini 3 Flash", but that ID has since been
# superseded. gemini-3.6-flash is the current GA Flash model.
# https://ai.google.dev/gemini-api/docs/latest-model
MODEL_ID = os.getenv("MODEL_ID", "gemini-3.6-flash")

# Section 3.4 of the brief requires 3 repeats per function and reports
# mean +/- standard deviation, which only carries information if generation
# is actually stochastic. Temperature 0 would make the three repeats
# near-identical and the reported deviation meaningless, so we keep the
# model's default sampling temperature.
TEMPERATURE = float(os.getenv("TEMPERATURE", "1.0"))
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "8192"))

# Rate limiting. Baseline B fires PANEL_SIZE + 2 calls back to back, and a
# full-scale run is hundreds in sequence, so 429s are routine rather than
# exceptional -- paid tiers have per-minute caps too. A 429 carries the
# server's own `retryDelay`, which the client honours; these bound how long it
# is willing to wait before giving up on a call.
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
MAX_RETRY_DELAY_SECONDS = float(os.getenv("MAX_RETRY_DELAY_SECONDS", "90"))

# --- Cost ------------------------------------------------------------------
# USD per 1M tokens. These are the figures quoted in the project brief for
# "Gemini 3 Flash".
# TODO(team): re-verify against current pricing for MODEL_ID before any cost
# number goes into the paper. On the free tier real spend is $0, so treat
# estimated_cost_usd as a list-price equivalent, not an invoice.
PRICE_PER_1M_INPUT_USD = float(os.getenv("PRICE_IN", "0.50"))
PRICE_PER_1M_OUTPUT_USD = float(os.getenv("PRICE_OUT", "3.00"))

# --- Experimental policy ---------------------------------------------------
# DECIDED -- Prof. Doaa, Week 3: doctests are stripped from every prompt.
#
# Every dataset function ships with doctests in its docstring, i.e. worked
# input -> output examples. Handing those to the model measures transcription
# rather than oracle reasoning, and it removes the surviving mutants the
# refinement-loop RQs need in order to have anything to work on.
#
# The decisive argument was comparability with CANDOR. HumanEval's Python
# docstrings do carry worked examples, but the Java translation CANDOR uses
# drops the Javadoc entirely, and the paper describes its input as source code
# plus a prose description. Stripping ours matches the system we compare
# against; keeping them would not.
#
# The flag stays configurable because an ablation over this condition was
# considered and set aside on cost grounds: it doubles the run (~1,260 ->
# ~2,520 calls) and the shared log schema has no field recording which
# condition produced a record. Do not flip it for a production run without
# adding that field first -- the two conditions would be indistinguishable in
# logs/.
INCLUDE_DOCTESTS = os.getenv("INCLUDE_DOCTESTS", "false").lower() == "true"

# OPEN TEAM DECISION: several dataset files hold more than one public function
# (function_01 has slow_primes/primes/fast_primes plus a benchmark helper).
# Non-testable scaffolding is excluded from prompts regardless.
EXCLUDE_FROM_PROMPT = ("benchmark", "main", "__main__")

# --- Baseline B ------------------------------------------------------------
# CANDOR tested 1-5 panelists and found no significant gain beyond 3.
PANEL_SIZE = int(os.getenv("PANEL_SIZE", "3"))

# CANDOR needed separate "Interpreter" agents purely to compress DeepSeek R1's
# very long reasoning. With native structured outputs the panelist returns a
# compact verdict directly, so Baseline B is 1 propose + PANEL_SIZE critique
# + 1 finalise call.
BASELINE_B_EXPECTED_CALLS = 1 + PANEL_SIZE + 1


def api_key() -> str | None:
    """Return the configured API key, or None when running without one."""
    return os.getenv(API_KEY_ENV) or None


def has_api_key() -> bool:
    return bool(api_key())
