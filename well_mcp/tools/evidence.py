"""
WELL Evidence Baseline — P0 Truth Enforcement.

When a tool has no real telemetry, sensor data, or external evidence,
it MUST return UNKNOWN, not STABLE / READY / LIVE / 0.85.

This module provides the canonical baseline for all WELL tools.
DITEMPA BUKAN DIBERI — Forged, Not Given.

Sovereign: Muhammad Arif bin Fazil (F13)
Date: 2026-07-21
License: AGPL-3.0
"""

from typing import Any

# ── Canonical UNKNOWN baseline ──────────────────────────────────────────────
# Every field that was previously hardcoded is now explicitly UNKNOWN.
# Tools MAY override individual fields when they have real evidence.
# Tools MUST NOT override the baseline to claim confidence without evidence.

UNKNOWN_BASELINE: dict[str, Any] = {
    "verdict": "UNKNOWN",
    "confidence": None,           # None = no evidence at all; 0.0 = evidence says "no signal"
    "truth_class": "STALE",       # STALE = no live telemetry; LIVE = real-time sensor data flowing
    "evidence_label": "NONE",     # NONE = no evidence; OBS/DER/INT when evidence exists
    "missing_evidence": [
        "no_telemetry",
        "no_sensor_data",
        "no_self_report",
        "no_external_verification",
    ],
    "evidence_age_hours": None,
    "friction_score": None,
    "cost_estimate": None,
    "reversibility_class": "UNKNOWN",
    "novelty_tags": [],
}


def build_unknown_result(
    tool_name: str,
    overrides: dict[str, Any] | None = None,
    missing: list[str] | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    """Build a WELL result dict from the UNKNOWN baseline.

    Args:
        tool_name: Name of the calling tool (for provenance)
        overrides: Fields to override on the baseline (e.g., when some evidence exists)
        missing: Specific evidence gaps for this tool call
        note: Human-readable note explaining why UNKNOWN

    Returns:
        A dict safe to return from any WELL tool.
    """
    result = dict(UNKNOWN_BASELINE)  # shallow copy
    result["tool"] = tool_name
    if missing:
        result["missing_evidence"] = missing
    if note:
        result["note"] = note
    if overrides:
        result.update(overrides)
    return result
