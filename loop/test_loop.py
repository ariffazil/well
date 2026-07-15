"""Tests for closed decision loop — no network required for core logic."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

WELL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WELL))

from loop.a_effective import compute_a_effective  # noqa: E402
from loop.recommend import recommend  # noqa: E402
from loop.recovery_v1 import HARD_ALLOWLIST, run_recovery_loop  # noqa: E402
from loop.state_envelope import build_state_envelope  # noqa: E402


def _fake_gate(**over):
    base = {
        "verdict": "PROCEED",
        "weakest_substrate": "H_WELL",
        "peace_condition": True,
        "tool_routing": {"allowed": "all", "blocked": "none"},
        "H_WELL": {
            "state": "READY",
            "rank": 4,
            "evidence": "self_report_score=80",
            "uncertainty": 0.3,
            "source": "inject",
            "note": "OPERATOR_REPORTED",
        },
        "M_WELL": {
            "state": "STABLE",
            "rank": 4,
            "evidence": "ok",
            "uncertainty": 0.2,
            "source": "sensor",
        },
        "G_WELL": {
            "state": "COHERENT",
            "rank": 4,
            "evidence": "ok",
            "uncertainty": 0.1,
            "source": "cf",
        },
        "C_WELL": {
            "state": "LOW_RISK",
            "rank": 4,
            "evidence": "ok",
            "uncertainty": 0.2,
            "source": "c",
        },
    }
    base.update(over)
    return base


def test_envelope_labels_self_report():
    env = build_state_envelope(
        gate=_fake_gate(),
        state={"truth_status": "OPERATOR_REPORTED"},
        service="well-heartbeat.service",
        service_probe={"active": True, "unit": "well-heartbeat.service"},
    )
    assert env["schema"] == "state_envelope.v1"
    assert env["human"]["source"] == "SELF_REPORTED"
    assert env["envelope_hash"].startswith("sha256:")
    assert env["human"]["state"] != "INVENTED"


def test_a_effective_collapses_on_hold():
    env = build_state_envelope(
        gate=_fake_gate(
            verdict="HOLD",
            G_WELL={
                "state": "COMPROMISED",
                "rank": 1,
                "evidence": "floors",
                "uncertainty": 0.2,
                "source": "x",
            },
            H_WELL={
                "state": "UNKNOWN",
                "rank": 0,
                "evidence": "none",
                "uncertainty": 0.9,
                "source": "none",
            },
            M_WELL={
                "state": "CRITICAL",
                "rank": 1,
                "evidence": "down",
                "uncertainty": 0.5,
                "source": "x",
            },
            C_WELL={
                "state": "HIGH_RISK",
                "rank": 1,
                "evidence": "x",
                "uncertainty": 0.5,
                "source": "x",
            },
        ),
        state={},
    )
    a = compute_a_effective(env, a_granted="EXECUTE_REVERSIBLE")
    assert a["mutation_allowed"] is False
    assert a["effective_band"] in ("RED", "BLACK", "ORANGE", "YELLOW")


def test_a_effective_green_path():
    env = build_state_envelope(
        gate=_fake_gate(),
        state={"truth_status": "OPERATOR_REPORTED"},
        execution={"rollback_available": True, "blast_radius": "LOW"},
    )
    # High E from coherent machine+gov
    a = compute_a_effective(env, a_granted="EXECUTE_REVERSIBLE")
    assert a["score"] > 0
    assert a["max_action_class"] in (
        "EXECUTE_REVERSIBLE",
        "QUEUE",
        "SIMULATE",
        "OBSERVE",
    )


def test_recommend_voids_fabrication():
    env = build_state_envelope(gate=_fake_gate(), state={})
    rec = recommend(env)
    void_ids = {o["id"] for o in rec["options"] if o["verdict"] == "VOID"}
    assert "VOID_1" in void_ids
    assert "VOID_2" in void_ids
    assert rec["authority"] == "PROPOSE_ONLY"
    assert len(rec["options"]) >= 3


def test_non_allowlisted_void():
    r = run_recovery_loop(service="ssh.service", mutate=False)
    assert r["verdict"] == "VOID"


def test_observe_path_no_mutation():
    with patch("loop.recovery_v1.probe_service") as ps, patch(
        "loop.recovery_v1.build_state_envelope"
    ) as be:
        ps.return_value = {
            "unit": "well-heartbeat.service",
            "active": True,
            "is_active": "active",
            "failed": False,
        }
        be.return_value = build_state_envelope(
            gate=_fake_gate(),
            state={"truth_status": "OPERATOR_REPORTED"},
            service="well-heartbeat.service",
            service_probe=ps.return_value,
        )
        r = run_recovery_loop(service="well-heartbeat.service", mutate=False)
    assert r["mutation_count"] == 0
    assert r["final_verdict"] in ("OBSERVE", "RECOMMEND", "SEAL", "HOLD")
    assert Path(r["receipt_path"]).exists()


def test_fault_inject_hold_without_mutate_when_a_low():
    """Failed service without mutate → recommend/hold, never silent restart."""
    weak_gate = _fake_gate(
        verdict="HOLD",
        M_WELL={
            "state": "CRITICAL",
            "rank": 1,
            "evidence": "down",
            "uncertainty": 0.5,
            "source": "x",
        },
        G_WELL={
            "state": "COMPROMISED",
            "rank": 1,
            "evidence": "x",
            "uncertainty": 0.5,
            "source": "x",
        },
        C_WELL={
            "state": "HIGH_RISK",
            "rank": 1,
            "evidence": "x",
            "uncertainty": 0.5,
            "source": "x",
        },
    )
    with patch("loop.recovery_v1.build_state_envelope") as be, patch(
        "loop.recovery_v1.probe_service"
    ) as ps:
        probe = {
            "unit": "well-heartbeat.service",
            "active": False,
            "failed": True,
            "is_active": "failed",
        }
        ps.return_value = probe
        be.return_value = build_state_envelope(
            gate=weak_gate,
            state={},
            service="well-heartbeat.service",
            service_probe=probe,
            execution={"rollback_available": True, "blast_radius": "LOW"},
        )
        r = run_recovery_loop(
            service="well-heartbeat.service", mutate=True, force_failed_probe=True
        )
    assert r["mutation_count"] == 0
    assert r["final_verdict"] in ("HOLD", "RECOMMEND", "OBSERVE")


def test_hard_allowlist():
    assert "well-heartbeat.service" in HARD_ALLOWLIST
    assert "well.service" not in HARD_ALLOWLIST


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
