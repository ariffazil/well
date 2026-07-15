"""WELL public MCP tool surface (canonical names).

SOT for *count* is live tools/list / health tool_count (**27**).
Names below are decorator-extracted (partial); runtime may register more modes.
Runtime registration remains in root server.py until full membrane split.
"""
from __future__ import annotations

# Live probe 2026-07-15: 27 tools. Names from server registration patterns.
CANONICAL_TOOL_NAMES: tuple[str, ...] = (
    "well_assess_homeostasis",
    "well_assess_livelihood",
    "well_assess_metabolism",
    "well_assess_reliability",
    "well_check_repair",
    "well_classify_substrate",
    "well_compute_metabolic_flux",
    "well_daily_checkin",
    "well_detect_boundary",
    "well_get_readiness",
    "well_guard_dignity",
    "well_measure_gradient",
    "well_reflect_intelligence",
    "well_state",
    "well_trace_lineage",
    "well_validate_vitality",
)

def list_public_tools() -> list[str]:
    return list(CANONICAL_TOOL_NAMES)

__all__ = ["CANONICAL_TOOL_NAMES", "list_public_tools"]
