"""
WELL MCP Tools — G-WELL Governance Substrate Tools.

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


async def well_classify_substrate(
    ctx: Context,
    mode: Literal["classification", "boundary", "health"] = "classification",
    subject: Optional[str] = None,
    description: Optional[str] = None,
    evaluation_intent: Optional[str] = None,
    session_id: Optional[str] = None,
    actor_id: str = "well-substrate",
) -> dict:
    """Substrate classification and boundary sensing."""
    result = build_unknown_result(
        "well_classify_substrate",
        missing=["substrate_signal", "boundary_probe", "classification_model"],
        note="No classification model or substrate signal data. Substrate class is UNKNOWN.",
    )
    # TODO: P2 — implement substrate classification from session + identity metadata

    # Generate replay receipt
    receipt = generate_replay_receipt(
        tool="well_classify_substrate",
        session_id="UNBOUND",
        actor_id=actor_id,
        inputs={
            "mode": mode,
            "subject": subject,
            "description": description,
            "evaluation_intent": evaluation_intent,
        },
        outputs=result,
    )

    return {**result, "replay_receipt": receipt.model_dump()}


async def well_detect_boundary(
    ctx: Context,
    mode: Literal["boundary", "membrane", "body", "machine", "federation"] = "boundary",
    subject: Optional[str] = None,
    description: Optional[str] = None,
    evaluation_intent: Optional[str] = None,
    peer: Optional[str] = None,
) -> dict:
    """Boundary detection across membrane, body, machine, and federation."""
    result = build_unknown_result(
        "well_detect_boundary",
        missing=["boundary_sensor", "membrane_state", "federation_topology"],
        note="No boundary probe or membrane sensor data. Boundary state is UNKNOWN.",
    )
    # TODO: P3 — wire to federation health probes + consent boundary checks

    # Generate replay receipt
    receipt = generate_replay_receipt(
        tool="well_detect_boundary",
        session_id="UNBOUND",
        actor_id=getattr(ctx, "actor_id", "unknown"),
        inputs={
            "mode": mode,
            "subject": subject,
            "description": description,
            "evaluation_intent": evaluation_intent,
            "peer": peer,
        },
        outputs=result,
    )

    return {**result, "replay_receipt": receipt.model_dump()}
