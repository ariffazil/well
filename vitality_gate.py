"""
WELL Vitality Gate — Constitutional Fusion Layer
═════════════════════════════════════════════════

Four mirrors → one gate. Weakest substrate determines response.
Same pattern as ART → Kernel → ACT, but for substrate readiness.

The gate does NOT diagnose. It reads four states and applies
floor dominance: the weakest dimension decides.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

WELL_DIR = Path(__file__).parent
SCHEMA_PATH = WELL_DIR / "WELL_STATE_SCHEMA.json"

# ── Rank map: state → numeric rank (higher = healthier) ──────────────────────
_RANK_MAP = {
    # H-WELL
    "READY": 4,
    "BELOW_BASELINE": 3,
    "DEGRADED": 2,
    "CRITICAL": 1,
    "UNKNOWN": 0,
    # M-WELL
    "STABLE": 4,
    "STRAINED": 3,
    "DEGRADED": 2,
    "CRITICAL": 1,
    # G-WELL
    "COHERENT": 4,
    "UNCERTAIN": 3,
    "DRIFTING": 2,
    "COMPROMISED": 1,
    "HOLD": 1,
    # C-WELL
    "LOW_RISK": 4,
    "MEDIUM_RISK": 3,
    "HIGH_RISK": 2,
    "RECOVERY": 2,
}

_VERDICT_MAP = {
    4: "PROCEED",
    3: "REDUCE_LOAD",
    2: "RECOVER",
    1: "HOLD",
    0: "INSUFFICIENT_DATA",
}


def _rank(state: str) -> int:
    return _RANK_MAP.get(state, 0)


def assess_h_well(state: dict[str, Any]) -> dict[str, Any]:
    """
    Assess H-WELL (human substrate) from state.json.
    Uses biometric inject data + freshness.
    Returns state enum + evidence + uncertainty.
    """
    ts = state.get("timestamp", "")
    truth = state.get("truth_status", "UNVERIFIED")
    well_score = state.get("well_score")

    # Freshness check
    age_hours = None
    if ts:
        try:
            dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            age_hours = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
        except Exception:
            pass

    if truth == "INSUFFICIENT_DATA" or age_hours is None:
        return {
            "state": "UNKNOWN",
            "rank": 0,
            "evidence": "no_biometric_data",
            "uncertainty": 0.9,
            "source": "none",
        }

    if age_hours > 48:
        return {
            "state": "UNKNOWN",
            "rank": 0,
            "evidence": f"stale_{age_hours:.0f}h",
            "uncertainty": 0.8,
            "source": "stale_inject",
        }

    if truth == "OPERATOR_REPORTED":
        # Self-report — use well_score as proxy
        if well_score is not None:
            if well_score >= 70:
                h_state = "READY"
            elif well_score >= 50:
                h_state = "BELOW_BASELINE"
            elif well_score >= 30:
                h_state = "DEGRADED"
            else:
                h_state = "CRITICAL"
        else:
            h_state = "UNKNOWN"

        return {
            "state": h_state,
            "rank": _rank(h_state),
            "evidence": f"self_report_score={well_score}",
            "uncertainty": 0.4,
            "source": "biometric_inject.sh",
            "note": "OPERATOR_REPORTED — not sensor verified",
        }

    # If we get here with VERIFIED (future wearable)
    return {
        "state": "READY",
        "rank": 4,
        "evidence": "verified_telemetry",
        "uncertainty": 0.1,
        "source": "wearable",
    }


def _load_machine_sensor() -> dict[str, Any] | None:
    """Auto-collect machine_human_substrate signals when not injected."""
    try:
        from sensors.machine_human_substrate import collect_substrate_signals

        return collect_substrate_signals()
    except Exception as exc:  # pragma: no cover — sensor optional at import time
        return {"_sensor_error": str(exc)}


def _probe_vps_machine() -> dict[str, Any] | None:
    """Optional pure VPS probe (cpu/mem/disk/organs) for M-WELL truth."""
    try:
        from vps_compute import probe_machine

        return probe_machine()
    except Exception:
        return None


def assess_m_well(sensor_data: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Assess M-WELL (machine substrate).

    Primary: machine_human_substrate (session/load/circadian telemetry).
    Secondary: vps_compute.probe_machine (cpu/mem/disk/organs) when available.
    Weakest of available signals wins (floor dominance).
    """
    if sensor_data is None:
        sensor_data = _load_machine_sensor()

    ranks: list[int] = []
    evidence_parts: list[str] = []
    sources: list[str] = []
    uncertainty = 0.9

    if sensor_data and not sensor_data.get("_sensor_error"):
        readiness = float(sensor_data.get("readiness_score", 0) or 0)
        fatigue = sensor_data.get("fatigue", {}) or {}
        sessions = sensor_data.get("sessions", {}) or {}
        if readiness >= 0.7:
            s_rank = 4
        elif readiness >= 0.5:
            s_rank = 3
        elif readiness >= 0.3:
            s_rank = 2
        else:
            s_rank = 1
        ranks.append(s_rank)
        evidence_parts.append(
            f"substrate_readiness={readiness}, fatigue={fatigue.get('level', '?')}, "
            f"human_sessions={sessions.get('human', 0)}"
        )
        sources.append("machine_human_substrate")
        uncertainty = min(uncertainty, 0.25)

    vps = _probe_vps_machine()
    if vps:
        v_state = str(vps.get("state", "UNKNOWN"))
        v_rank = _rank(v_state) if v_state in _RANK_MAP else 0
        if v_rank:
            ranks.append(v_rank)
        signals = vps.get("signals", {}) or {}
        evidence_parts.append(
            f"vps_state={v_state}, score={vps.get('score')}, "
            f"cpu={signals.get('cpu_pct')}, mem={signals.get('memory_pct')}, "
            f"organs={signals.get('organs_up')}"
        )
        sources.append("vps_compute.probe_machine")
        uncertainty = min(uncertainty, 0.2)

    if not ranks:
        err = (sensor_data or {}).get("_sensor_error")
        return {
            "state": "UNKNOWN",
            "rank": 0,
            "evidence": f"no_sensor_data{': ' + err if err else ''}",
            "uncertainty": 0.9,
            "source": "none",
        }

    # Floor dominance: weakest available machine signal determines state
    min_rank = min(ranks)
    inv = {4: "STABLE", 3: "STRAINED", 2: "DEGRADED", 1: "CRITICAL", 0: "UNKNOWN"}
    m_state = inv.get(min_rank, "UNKNOWN")

    return {
        "state": m_state,
        "rank": min_rank,
        "evidence": "; ".join(evidence_parts),
        "uncertainty": uncertainty,
        "source": "+".join(sources),
    }


def assess_g_well(state: dict[str, Any]) -> dict[str, Any]:
    """
    Assess G-WELL (governance coherence) from state + carry_forward.
    Checks identity drift, seal chain, floor compliance.
    """
    carry_forward_path = Path("/root/.local/share/arifos/carry_forward.json")
    drift = "UNKNOWN"
    try:
        cf = json.loads(carry_forward_path.read_text())
        drift = cf.get("identity_drift", "UNKNOWN")
    except Exception:
        pass

    floors_violated = state.get("floors_violated", [])
    truth = state.get("truth_status", "UNVERIFIED")

    if floors_violated:
        g_state = "COMPROMISED"
    elif drift == "DRIFT":
        g_state = "DRIFTING"
    elif truth in ("VOID", "TEST"):
        g_state = "UNCERTAIN"
    else:
        g_state = "COHERENT"

    return {
        "state": g_state,
        "rank": _rank(g_state),
        "evidence": f"drift={drift}, floors_violated={len(floors_violated)}, truth={truth}",
        "uncertainty": 0.15,
        "source": "carry_forward + state.json",
    }


def assess_c_well(h: dict, m: dict, g: dict) -> dict[str, Any]:
    """
    Assess C-WELL (coupled state) from H, M, G assessments.
    Weakest substrate + interaction risk.
    """
    h_rank = h["rank"]
    m_rank = m["rank"]
    g_rank = g["rank"]

    min_rank = min(h_rank, m_rank, g_rank)
    degraded_count = sum(1 for r in [h_rank, m_rank, g_rank] if r <= 2)

    if min_rank <= 1 or degraded_count >= 2:
        c_state = "HIGH_RISK"
    elif min_rank == 2 or degraded_count == 1:
        c_state = "MEDIUM_RISK"
    elif min_rank == 0:
        c_state = "RECOVERY"
    else:
        c_state = "LOW_RISK"

    return {
        "state": c_state,
        "rank": _rank(c_state),
        "evidence": f"H={h['state']}({h_rank}) M={m['state']}({m_rank}) G={g['state']}({g_rank}), "
        f"degraded_count={degraded_count}",
        "uncertainty": max(h["uncertainty"], m["uncertainty"], g["uncertainty"]),
        "source": "coupled_analysis",
    }


def vitality_gate(
    state: dict[str, Any] | None = None,
    sensor_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    The constitutional vitality gate.
    Four mirrors → one verdict. Weakest substrate determines response.

    Returns:
        verdict: PROCEED | REDUCE_LOAD | RECOVER | HOLD | INSUFFICIENT_DATA
        H_WELL, M_WELL, G_WELL, C_WELL: individual assessments
        weakest: which substrate is the bottleneck
        tool_routing: what tools are allowed
        peace_condition: whether peace is achievable
    """
    if state is None:
        state_path = WELL_DIR / "state.json"
        if state_path.exists():
            state = json.loads(state_path.read_text())
        else:
            state = {}
    _state: dict[str, Any] = state  # ensure non-None for type checker

    # Auto-feed machine_human_substrate when caller does not inject sensor_data
    if sensor_data is None:
        sensor_data = _load_machine_sensor()

    # Assess all four mirrors
    h = assess_h_well(_state)
    m = assess_m_well(sensor_data)
    g = assess_g_well(_state)
    c = assess_c_well(h, m, g)

    # Weakest substrate = gate
    all_dims = {"H_WELL": h, "M_WELL": m, "G_WELL": g, "C_WELL": c}
    weakest_name = min(all_dims, key=lambda k: all_dims[k]["rank"])
    weakest_rank = all_dims[weakest_name]["rank"]

    verdict = _VERDICT_MAP.get(weakest_rank, "INSUFFICIENT_DATA")

    # Tool routing
    routing = {
        "PROCEED": {"allowed": "all", "blocked": "none"},
        "REDUCE_LOAD": {
            "allowed": "observe, plan, reflect, low-risk edits",
            "blocked": "C4 irreversible, new deps, prod deploy",
        },
        "RECOVER": {
            "allowed": "observe only, reflection, health checks",
            "blocked": "all mutations, all seals, all deploys",
        },
        "HOLD": {
            "allowed": "health probes only",
            "blocked": "everything else",
            "requires": "sovereign ack to release",
        },
        "INSUFFICIENT_DATA": {
            "allowed": "observe, inject, sensor read",
            "blocked": "mutations, seals",
            "action": "request sovereign inject or wait for sensor",
        },
    }

    # Peace condition
    peace = (
        h["rank"] >= 2  # recovery capacity intact
        and (
            m["rank"] >= 3 or m["state"] == "STRAINED"
        )  # machine stable or safely degraded
        and g["rank"] >= 3  # governance coherent or merely uncertain
        and c["rank"] >= 3  # low or medium coupling risk
    )

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "weakest_substrate": weakest_name,
        "weakest_rank": weakest_rank,
        "H_WELL": h,
        "M_WELL": m,
        "G_WELL": g,
        "C_WELL": c,
        "tool_routing": routing.get(verdict, routing["INSUFFICIENT_DATA"]),
        "peace_condition": peace,
        "peace_note": "Peace = recoverable homeostasis with preserved sovereignty. "
        "Not permanent calm. Not optimized predictability.",
        "gate_rule": "Weakest substrate determines response. Floor dominance.",
        "schema_version": "1.0.0",
    }


def main():
    """CLI entry point — run the vitality gate."""
    import sys

    # Optionally load sensor data
    sensor_data = None
    sensor_path = WELL_DIR / "sensors" / "machine_human_substrate.py"
    if sensor_path.exists():
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location("mhs", sensor_path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                sensor_data = mod.collect_substrate_signals()
        except Exception:
            pass

    result = vitality_gate(sensor_data=sensor_data)

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"═══ WELL VITALITY GATE ═══")
        print(f"Verdict:           {result['verdict']}")
        print(
            f"Weakest substrate: {result['weakest_substrate']} (rank {result['weakest_rank']})"
        )
        print(f"Peace:             {'YES' if result['peace_condition'] else 'NO'}")
        print()
        for dim in ["H_WELL", "M_WELL", "G_WELL", "C_WELL"]:
            d = result[dim]
            print(
                f"  {dim}: {d['state']:20s} rank={d['rank']}  Ω={d['uncertainty']:.2f}  {d['evidence']}"
            )
        print()
        print(f"Tool routing: {result['tool_routing']['allowed']}")
        if result["tool_routing"].get("blocked") != "none":
            print(f"Blocked:      {result['tool_routing']['blocked']}")


if __name__ == "__main__":
    main()
