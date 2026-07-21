"""
WELL MCP Replay Receipt Generator — Audit trail for constitutional organ.

Domain Law: SUBSTRATE_LAW
Authority: REFLECT_ONLY — mirror, never judge

Sovereign: Muhammad Arif bin Fazil (F13)
Date: 2026-07-16
License: AGPL-3.0

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from datetime import datetime
from typing import Any, Literal
import json

from ..transport.types import ReplayReceipt


def generate_replay_receipt(
    tool: str,
    session_id: str = "UNBOUND",
    actor_id: str = "UNBOUND",
    inputs: dict[str, Any] | None = None,
    outputs: dict[str, Any] | None = None,
    truth_class: Literal["LIVE", "CACHED", "INFERRED", "STALE"] = "STALE",
    evidence_label: Literal["OBS", "DER", "INT", "SPEC", "NONE"] = "NONE",
    friction_score: float | None = None,
    cost_estimate: float | None = None,
    reversibility_class: Literal["REVERSIBLE", "IRREVERSIBLE", "UNKNOWN"] = "UNKNOWN",
    novelty_tags: list[str] | None = None,
) -> ReplayReceipt:
    """Generate a typed replay receipt for audit trail.

    P0 TRUTH ENFORCEMENT (2026-07-21):
      - session_id defaults to "UNBOUND" — real sessions must be explicitly bound
      - truth_class defaults to "STALE" — LIVE must be earned with telemetry
      - evidence_label defaults to "NONE" — OBS/DER/INT must be earned with evidence
      - reversibility_class defaults to "UNKNOWN" — not assumed reversible
    """
    return ReplayReceipt(
        tool=tool,
        timestamp=datetime.utcnow(),
        session_id=session_id,
        actor_id=actor_id,
        inputs=inputs or {},
        outputs=outputs or {},
        truth_class=truth_class,
        evidence_label=evidence_label,
        friction_score=friction_score,
        cost_estimate=cost_estimate,
        reversibility_class=reversibility_class,
        novelty_tags=novelty_tags or [],
    )


def receipt_to_json(receipt: ReplayReceipt) -> str:
    """Convert replay receipt to JSON string."""
    return receipt.model_dump_json(indent=2)


def receipt_to_dict(receipt: ReplayReceipt) -> dict[str, Any]:
    """Convert replay receipt to dictionary."""
    return receipt.model_dump()
