"""
WELL MCP Tools — M-WELL Machine Substrate Tools.

Domain Law: SUBSTRATE_LAW
Authority: REFLECT_ONLY — mirror, never judge

Sovereign: Muhammad Arif bin Fazil (F13)
Date: 2026-07-16
License: AGPL-3.0

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from fastmcp import Context
from typing import Literal, Optional

from ..replay.receipt import generate_replay_receipt
from .evidence import build_unknown_result


async def well_assess_reliability(
    ctx: Context,
    mode: Literal["health", "tools", "institutions"] = "health",
) -> dict:
    """Assess machine, tool, institution, and operational reliability."""
    result = build_unknown_result(
        "well_assess_reliability",
        missing=["machine_telemetry", "tool_health_probe", "institution_audit"],
        note="No Prometheus Node Exporter or machine telemetry sensor deployed. Machine state is UNKNOWN until telemetry pipeline is live.",
    )
    # TODO: P1 — wire to Prometheus Node Exporter metrics + systemd health probes

    # Generate replay receipt
    receipt = generate_replay_receipt(
        tool="well_assess_reliability",
        session_id="UNBOUND",
        actor_id=getattr(ctx, "actor_id", "unknown"),
        inputs={"mode": mode},
        outputs=result,
    )

    return {**result, "replay_receipt": receipt.model_dump()}


async def well_check_repair(
    ctx: Context,
    mode: Literal["precheck", "postcheck", "recovery"] = "precheck",
    task_description: Optional[str] = None,
    decision_class: Optional[str] = None,
    source: Optional[str] = None,
    intensity: Optional[float] = None,
    outcome: Optional[str] = None,
) -> dict:
    """Check repair, recovery, resilience, and forge cycle integrity."""
    result = build_unknown_result(
        "well_check_repair",
        missing=["repair_history", "service_state", "rollback_capability"],
        note="No repair allowlist or recovery history available. Repair readiness is UNKNOWN until P4 bounded-repair pipeline is built.",
    )
    # TODO: P4 — implement repair precheck against allowlist + service state

    # Generate replay receipt
    receipt = generate_replay_receipt(
        tool="well_check_repair",
        session_id="UNBOUND",
        actor_id=getattr(ctx, "actor_id", "unknown"),
        inputs={
            "mode": mode,
            "task_description": task_description,
            "decision_class": decision_class,
            "source": source,
            "intensity": intensity,
            "outcome": outcome,
        },
        outputs=result,
    )

    return {**result, "replay_receipt": receipt.model_dump()}


    # Generate replay receipt
    receipt = generate_replay_receipt(
        tool="well_health_check",
        session_id="UNBOUND",
        actor_id=getattr(ctx, "actor_id", "unknown"),
        inputs={"include_federation": include_federation},
        outputs=result,
    )

    return {**result, "replay_receipt": receipt.model_dump()}
