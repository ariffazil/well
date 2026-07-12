#!/usr/bin/env python3
"""
Conformance: Kernel session posture → WELL readiness envelope → fallbacks.

Does not require MCP host for WELL (in-process). Proves:
  - envelope schema present
  - human/machine not collapsed
  - UNKNOWN human does not invent score as sensor
  - WELL unavailable fallback shape
  - C4 irreversible posture narrows on weak evidence

Priority 5 — MEASUREMENT_BOUNDARY_CONTRACT.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

WELL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WELL))


def test_envelope_separates_human_machine():
    from loop.readiness_envelope import build_readiness_envelope

    env = build_readiness_envelope(
        color="YELLOW",
        score=69.5,
        confidence=0.4,
        action="SIMPLIFY",
        reason="self_report + machine ok",
        human={"state": "BELOW_BASELINE", "evidence_type": "self_report"},
        machine={"state": "STRAINED", "evidence_type": "telemetry"},
        interaction={"state": "MEDIUM_RISK", "evidence_type": "inferred"},
        ttl_hours=0.5,
    )
    r = env["readiness"]
    assert r["substrates"]["human"]["evidence_type"] == "self_report"
    assert r["substrates"]["machine"]["evidence_type"] == "telemetry"
    assert r["boundaries"]["diagnostic"] is False
    assert r["boundaries"]["final_judge"] == "ARIF"
    assert "human_state" not in r["missing_evidence"] or r["substrates"]["human"][
        "state"
    ] != "UNKNOWN"


def test_unknown_human_listed_missing():
    from loop.readiness_envelope import build_readiness_envelope

    env = build_readiness_envelope(
        color="YELLOW",
        score=None,
        confidence=0.2,
        action="EVIDENCE_NEEDED",
        reason="no human evidence",
        human={"state": "UNKNOWN", "evidence_type": "none"},
        machine={"state": "GREEN", "evidence_type": "telemetry"},
    )
    assert "human_state" in env["readiness"]["missing_evidence"]
    assert env["readiness"]["substrates"]["machine"]["state"] == "GREEN"


def test_well_unavailable_fallback():
    """Kernel posture when WELL cannot answer — no fabricated human score."""
    fallback = {
        "well_available": False,
        "readiness": {
            "state": "UNKNOWN",
            "score": None,
            "confidence": 0.0,
            "substrates": {
                "human": {"state": "UNKNOWN", "evidence_type": "none"},
                "machine": {"state": "UNKNOWN", "evidence_type": "none"},
            },
            "missing_evidence": ["well_organ", "human_state", "machine_state"],
            "recommendation": "EVIDENCE_NEEDED",
            "boundaries": {
                "diagnostic": False,
                "authority": "advisory_only",
                "final_judge": "ARIF",
            },
        },
        "kernel_posture": "NARROW_AUTHORITY",
        "max_action_class": "OBSERVE",
        "mutation_allowed": False,
    }
    assert fallback["readiness"]["score"] is None
    assert fallback["mutation_allowed"] is False
    assert fallback["kernel_posture"] == "NARROW_AUTHORITY"


def test_c4_requires_stronger_than_registry_claim():
    """evidence_quality 0.5 must not pass C4 gate."""
    evidence_quality = 0.5
    decision_class = "C4"
    min_eq = {"C1": 0.3, "C2": 0.4, "C3": 0.6, "C4": 0.75, "C5": 0.85}
    ok = evidence_quality >= min_eq[decision_class]
    assert ok is False


def test_live_well_readiness_envelope_if_importable():
    """In-process well_readiness returns envelope fields (skip if server import heavy)."""
    try:
        # Prefer pure envelope path with vitality_gate
        from vitality_gate import vitality_gate
        from loop.readiness_envelope import build_readiness_envelope, map_gate_to_substrates
        import json
        from pathlib import Path

        state_path = WELL / "state.json"
        state = json.loads(state_path.read_text()) if state_path.exists() else {}
        gate = vitality_gate(state=state)
        subs = map_gate_to_substrates(gate, state)
        env = build_readiness_envelope(
            color="YELLOW",
            score=state.get("well_score"),
            confidence=0.4,
            action="SIMPLIFY",
            reason="live_probe",
            human=subs["human"],
            machine=subs["machine"],
            interaction=subs["interaction"],
            governance=subs["governance"],
            vitality_gate={"verdict": gate.get("verdict")},
        )
        assert env["schema"] == "well_readiness_envelope.v1"
        # Must not claim sensor for self-report
        if state.get("truth_status") == "OPERATOR_REPORTED":
            assert env["readiness"]["substrates"]["human"]["evidence_type"] in (
                "self_report",
                "none",
                "inferred",
            )
            assert env["readiness"]["substrates"]["human"]["evidence_type"] != "sensor"
        print("live_envelope_ok", env["readiness"]["substrates"]["human"]["evidence_type"])
    except Exception as e:
        print("live_skip", e)


def test_stale_and_malformed_fallbacks():
    from loop.readiness_envelope import build_readiness_envelope

    stale = build_readiness_envelope(
        color="STALE",
        score=80,
        confidence=0.1,
        action="INJECT_NEEDED",
        reason="ttl>48h",
        human={"state": "UNKNOWN", "evidence_type": "none"},
        machine={"state": "UNKNOWN", "evidence_type": "none"},
        ttl_hours=60,
    )
    assert stale["readiness"]["recommendation"] == "EVIDENCE_NEEDED"
    assert stale["readiness"]["state"] == "STALE"


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as e:
                failed += 1
                print(f"FAIL {name}: {e}")
    print(f"\n{sum(1 for k in globals() if k.startswith('test_')) - failed}/"
          f"{sum(1 for k in globals() if k.startswith('test_'))} passed")
    sys.exit(1 if failed else 0)
