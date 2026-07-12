"""Typed state envelope — structured evidence for decisions (not prose)."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

SCHEMA = "state_envelope.v1"

# Evidence source labels (HARD — no silent upgrade)
SOURCE_LABELS = frozenset(
    {
        "OBSERVED",
        "SELF_REPORTED",
        "SENSOR_MEASURED",
        "INFERRED",
        "UNKNOWN",
    }
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_payload(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode()
    return f"sha256:{hashlib.sha256(raw).hexdigest()}"


def _map_h_source(h: dict[str, Any], state: dict[str, Any]) -> str:
    truth = str(state.get("truth_status", "")).upper()
    note = str(h.get("note", "") + h.get("source", "")).lower()
    if truth in ("OPERATOR_REPORTED", "SELF_REPORT") or "self_report" in note:
        return "SELF_REPORTED"
    if "wearable" in note or truth in ("SENSOR_VERIFIED", "VERIFIED"):
        return "SENSOR_MEASURED"
    if h.get("state") == "UNKNOWN":
        return "UNKNOWN"
    return "INFERRED"


def build_state_envelope(
    task: str = "substrate_readiness",
    gate: dict[str, Any] | None = None,
    state: dict[str, Any] | None = None,
    service: str | None = None,
    service_probe: dict[str, Any] | None = None,
    capital: dict[str, Any] | None = None,
    execution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a typed decision state from vitality_gate (+ optional service probe)."""
    if gate is None:
        from vitality_gate import vitality_gate

        gate = vitality_gate(state=state)

    if state is None:
        from pathlib import Path

        p = Path(__file__).resolve().parent.parent / "state.json"
        state = json.loads(p.read_text()) if p.exists() else {}

    h = gate.get("H_WELL") or {}
    m = gate.get("M_WELL") or {}
    g = gate.get("G_WELL") or {}
    c = gate.get("C_WELL") or {}

    human = {
        "state": h.get("state", "UNKNOWN"),
        "source": _map_h_source(h, state),
        "confidence": round(1.0 - float(h.get("uncertainty", 0.9)), 3),
        "evidence": h.get("evidence"),
        "rank": h.get("rank", 0),
    }
    machine = {
        "state": m.get("state", "UNKNOWN"),
        "source": "OBSERVED" if m.get("rank", 0) > 0 else "UNKNOWN",
        "confidence": round(1.0 - float(m.get("uncertainty", 0.9)), 3),
        "evidence": m.get("evidence"),
        "rank": m.get("rank", 0),
        "observations": [],
    }
    if service_probe:
        machine["service"] = service_probe
        if service_probe.get("active") is False:
            machine["observations"].append("service_inactive")
        if service_probe.get("failed"):
            machine["observations"].append("service_failed")

    governance = {
        "state": g.get("state", "UNKNOWN"),
        "source": "OBSERVED",
        "confidence": round(1.0 - float(g.get("uncertainty", 0.5)), 3),
        "evidence": g.get("evidence"),
        "rank": g.get("rank", 0),
        "session_valid": True,
        "authority_band_hint": _band_hint(gate),
    }
    coupling = {
        "state": c.get("state", "UNKNOWN"),
        "source": "INFERRED",
        "confidence": round(1.0 - float(c.get("uncertainty", 0.5)), 3),
        "rank": c.get("rank", 0),
    }

    envelope: dict[str, Any] = {
        "schema": SCHEMA,
        "timestamp": _now(),
        "task": task,
        "service": service,
        "human": human,
        "machine": machine,
        "governance": governance,
        "coupling": coupling,
        "capital": capital
        or {
            "expected_cost_rm": 0.0,
            "downside": "LOW",
            "source": "INFERRED",
        },
        "execution": execution
        or {
            "rollback_available": True,
            "blast_radius": "LOW",
            "max_mutations": 1,
        },
        "gate": {
            "verdict": gate.get("verdict"),
            "weakest_substrate": gate.get("weakest_substrate"),
            "peace_condition": gate.get("peace_condition"),
            "tool_routing": gate.get("tool_routing"),
        },
        "evidence_quality": _evidence_quality(human, machine, governance),
        "w0": "OPERATOR_VETO_INTACT",
        "authority": "REFLECT_ONLY_FOR_HUMAN",
    }
    envelope["envelope_hash"] = _hash_payload(
        {k: v for k, v in envelope.items() if k != "envelope_hash"}
    )
    return envelope


def _band_hint(gate: dict[str, Any]) -> str:
    v = gate.get("verdict")
    if v == "PROCEED":
        return "GREEN"
    if v in ("REDUCE_LOAD",):
        return "YELLOW"
    if v in ("RECOVER",):
        return "ORANGE"
    if v == "HOLD":
        return "RED"
    return "YELLOW"  # INSUFFICIENT_DATA → caution, not invent GREEN


def _evidence_quality(human: dict, machine: dict, governance: dict) -> float:
    """E ∈ [0,1] — multiplies A_effective. UNKNOWN human is OK if human not required."""
    parts = [machine.get("confidence", 0.0), governance.get("confidence", 0.0)]
    # Human confidence only counts when present
    if human.get("source") != "UNKNOWN":
        parts.append(human.get("confidence", 0.0))
    if not parts:
        return 0.0
    return round(sum(parts) / len(parts), 3)
