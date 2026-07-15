"""WELL public MCP tool surface — live SOT (27 tools).

Runtime truth: mcporter list well / tools/list / health tool_count.
Do not invent tools. Do not claim medical authority.
"""
from __future__ import annotations

# Live probe 2026-07-15 — 27 public tools (mcporter)
CANONICAL_TOOL_NAMES: tuple[str, ...] = (
    "well_health_check",
    "well_medical_boundary",
    "well_signal_coverage",
    "well_handoff_dignity_to_arifos",
    "well_handoff_livelihood_to_wealth",
    "well_attest_to_kernel",
    "well_classify_substrate",
    "well_trace_lineage",
    "well_detect_boundary",
    "well_measure_gradient",
    "well_assess_metabolism",
    "well_assess_homeostasis",
    "well_check_repair",
    "well_validate_vitality",
    "well_assess_livelihood",
    "well_assess_reliability",
    "well_compute_metabolic_flux",
    "well_assess_sovereign_entropy",
    "well_dark_geometry_mirror",
    "well_guard_dignity",
    "well_registry_status",
    "well_classify_state",
    "well_sabar_latency",
    "well_trust_compression",
    "well_niat_impact_mirror",
    "well_correction_capacity",
    "well_regulation_recovery",
)

# Alias for prompt compatibility
__all__ = ["CANONICAL_TOOL_NAMES", "list_public_tools"]


def list_public_tools() -> list[str]:
    return list(CANONICAL_TOOL_NAMES)
