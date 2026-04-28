"""
WELL MCP Server — Human Substrate Governance Layer
Phase 1: Immutable Ledger & Observability

W0 Sovereignty Invariant: WELL holds a mirror, not a veto.
WELL informs. arifOS judges. A-FORGE executes. Hierarchy is invariant.
"""

from __future__ import annotations

import hashlib
import json
import datetime
from pathlib import Path
from typing import Any

from fastmcp import FastMCP, Context

# ── Paths ──────────────────────────────────────────────────────────────────────
import os as _os
WELL_DIR = Path(__file__).parent
STATE_PATH = Path(_os.environ.get("WELL_STATE_PATH", "/root/WELL/state.json"))
EVENTS_PATH = Path(_os.environ.get("WELL_EVENTS_PATH", "/root/WELL/events.jsonl"))
VAULT_LEDGER_PATH = Path(
    _os.environ.get("WELL_VAULT_PATH", "/root/WELL/vault_ledger.jsonl")
)

# ── Server ─────────────────────────────────────────────────────────────────────
mcp = FastMCP(
    name="AFWELL",

    instructions=(
        "WELL is the Human–Machine Readiness Mirror for arifOS. "
        "H-WELL reflects operator Arif's biological and cognitive state. "
        "M-WELL reflects system reliability, tool health, context integrity, and compute limits. "
        "C-WELL evaluates coupled risk between human state and machine state. "
        "The WELL–FORGE bridge lets A-FORGE adapt execution intensity to Arif's readiness. "
        "W0: WELL holds a mirror, not a veto. Operator sovereignty is invariant. "
        "DITEMPA BUKAN DIBERI — Forged, Not Given."
    ),
)

# ── Helpers ────────────────────────────────────────────────────────────────────

def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "operator_id": "arif",
            "metrics": {},
            "well_score": 50,
            "floors_violated": [],
        }
    with open(STATE_PATH) as f:
        return json.load(f)


def _save_state(state: dict[str, Any]) -> None:
    state["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2))


def _append_event(event: dict[str, Any]) -> None:
    event["epoch"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(EVENTS_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")


def _compute_score(metrics: dict[str, Any]) -> tuple[float, list[str]]:
    """Compute WELL score (0-100) and floor violations from metrics."""
    score = 100.0
    violations: list[str] = []

    sleep = metrics.get("sleep", {})
    cognitive = metrics.get("cognitive", {})
    stress = metrics.get("stress", {})
    metabolic = metrics.get("metabolic", {})

    # W1 — Sleep Integrity
    debt = sleep.get("sleep_debt_days", 0)
    quality = sleep.get("quality_score", 10)
    hours = sleep.get("last_night_hours", 8)
    score -= min(debt * 8, 24)
    score -= max(0, (7 - hours) * 3)
    score -= max(0, (8 - quality) * 1.5)
    if debt > 2:
        violations.append("W1_SLEEP_DEBT")

    # W5 — Cognitive Entropy
    clarity = cognitive.get("clarity", 10)
    fatigue = cognitive.get("decision_fatigue", 0)
    score -= max(0, (8 - clarity) * 2)
    score -= fatigue * 1.5
    if clarity < 4:
        violations.append("W5_COGNITIVE_ENTROPY")

    # Stress load
    load = stress.get("subjective_load", 0)
    restless = stress.get("restlessness", 0)
    score -= load * 1.2
    score -= restless * 0.8

    # Metabolic
    stability = metabolic.get("perceived_stability", 10)
    score -= max(0, (7 - stability) * 1.5)
    if metabolic.get("hydration_status") == "DEHYDRATED":
        score -= 5

    # W6 — Incentive Decoupling (static floor, Phase 3)
    score = round(max(0.0, min(100.0, score)), 1)
    return score, violations


def readiness_score(metrics: dict[str, Any]) -> dict[str, Any]:
    """
    Phase 2 Readiness Score Engine.
    Computes a 0.0-1.0 score and determines color tier using canonical _compute_score.
    """
    score_100, violations = _compute_score(metrics)
    score = round(score_100 / 100.0, 2)

    if score >= 0.7 and not violations:
        tier = "GREEN"
        recommendation = "Full action allowed. Substrate optimal."
    elif score >= 0.4:
        tier = "AMBER"
        recommendation = f"Soft warning: {', '.join(violations) if violations else 'Low capacity'}. Proceed with caution."
    else:
        tier = "RED"
        recommendation = f"CRITICAL: {', '.join(violations)}. Block strategic forge actions. Route to arifOS 888 HOLD."

    return {
        "score": score,
        "tier": tier,
        "w_floors_triggered": violations,
        "recommendation": recommendation,
        "human_decision_required": tier in ("AMBER", "RED"),
    }


def _compose_verdict(
    mcp: str,
    task: str,
    status: str,  # PASS | CAUTION | HOLD | VOID
    domain_verdict: str,
    confidence: str = "HIGH",
    epistemic: str = "CLAIM",
    epistemic_integrity: float = 1.0,
    authority_level: str = "advisory_only",
    risk_level: str = "GREEN",
    human_readiness: str = "OPTIMAL",
    machine_readiness: str = "HEALTHY",
    failure_class: str | None = None,
    failure_severity: str = "LOW",
    impact_summary: str | None = None,
    recommended_mode: str = "full",
    human_required: bool = False,
    assumptions: list[str] | None = None,
    failure_flags: list[str] | None = None,
    next_safe_action: str | None = None,
) -> dict[str, Any]:
    """Canonical arifOS MCP verdict schema (Spec v1.0) with Failure Doctrine v1.0."""
    
    # Failure Doctrine Overrides
    if failure_class:
        status = "HOLD" if status != "VOID" else "VOID"
        recommended_mode = "pause" if failure_severity in ("HIGH", "CRITICAL") else "draft_only"
        epistemic_integrity = min(epistemic_integrity, 0.1)
        confidence = "LOW"
        human_required = True

    return {
        "mcp": mcp,
        "task": task,
        "status": status,
        "domain_verdict": domain_verdict,
        "confidence": confidence,
        "epistemic": {
            "class": epistemic,
            "integrity_score": epistemic_integrity,
        },
        "failure": {
            "class": failure_class,
            "severity": failure_severity,
            "impact": impact_summary or ("N/A" if not failure_class else "Subsystem failure"),
        } if failure_class else None,
        "authority": {
            "level": authority_level,
            "boundary": "W0 — Mirror only" if mcp == "AFWELL" else "Domain Expert",
        },
        "readiness": {
            "human": human_readiness,
            "machine": machine_readiness,
        },
        "risk": {
            "level": risk_level,
            "coupled": "UNKNOWN",
        },
        "execution": {
            "recommended_mode": recommended_mode,
            "human_confirmation_required": human_required,
            "next_safe_action": next_safe_action or "Consult arifOS 888_JUDGE",
        },
        "assumptions": assumptions or [],
        "failure_flags": failure_flags or [],
        "reversibility": "REVERSIBLE" if task.startswith("read") or "check" in task else "UNKNOWN",
        "final_authority": "Arif",
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
        "receipt_hash": hashlib.sha256(str(datetime.datetime.now()).encode()).hexdigest()[:16]
    }


# ── Tools ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def well_state(ctx: Context | None = None) -> dict[str, Any]:
    """
    Get the current WELL state — biological telemetry snapshot for operator Arif.
    Returns score, floor violations, and all metric dimensions.
    """
    state = _load_state()
    return {
        "ok": True,
        "operator_id": state.get("operator_id", "arif"),
        "timestamp": state.get("timestamp"),
        "well_score": state.get("well_score", 50),
        "floors_violated": state.get("floors_violated", []),
        "metrics": state.get("metrics", {}),
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


@mcp.tool()
def well_log(
    # Sleep
    sleep_hours: float | None = None,
    sleep_debt_days: float | None = None,
    sleep_quality: float | None = None,
    # Stress
    stress_load: float | None = None,
    restlessness: float | None = None,
    hrv_proxy: float | None = None,
    # Cognitive
    clarity: float | None = None,
    decision_fatigue: float | None = None,
    focus_durability: float | None = None,
    # Metabolic
    fasting_hours: float | None = None,
    metabolic_stability: float | None = None,
    hydration: str | None = None,
    # Structural
    pain_sites: list[str] | None = None,
    movement_count: float | None = None,
    # Optional note
    note: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Log a biological telemetry update for operator Arif.
    Updates state.json, recomputes WELL score, checks floor violations.
    Only provide dimensions you're logging — omitted fields are unchanged.
    """
    state = _load_state()
    metrics = state.get("metrics", {})

    # ── Merge incoming readings ────────────────────────────────────
    if any(v is not None for v in [sleep_hours, sleep_debt_days, sleep_quality]):
        sleep = dict(metrics.get("sleep", {}))
        if sleep_hours is not None:
            sleep["last_night_hours"] = sleep_hours
        if sleep_debt_days is not None:
            sleep["sleep_debt_days"] = sleep_debt_days
        if sleep_quality is not None:
            sleep["quality_score"] = sleep_quality
        metrics["sleep"] = sleep

    if any(v is not None for v in [stress_load, restlessness, hrv_proxy]):
        stress = dict(metrics.get("stress", {}))
        if stress_load is not None:
            stress["subjective_load"] = stress_load
        if restlessness is not None:
            stress["restlessness"] = restlessness
        if hrv_proxy is not None:
            stress["hrv_proxy"] = hrv_proxy
        metrics["stress"] = stress

    if any(v is not None for v in [clarity, decision_fatigue, focus_durability]):
        cog = dict(metrics.get("cognitive", {}))
        if clarity is not None:
            cog["clarity"] = clarity
        if decision_fatigue is not None:
            cog["decision_fatigue"] = decision_fatigue
        if focus_durability is not None:
            cog["focus_durability"] = focus_durability
        metrics["cognitive"] = cog

    if any(v is not None for v in [fasting_hours, metabolic_stability, hydration]):
        meta = dict(metrics.get("metabolic", {}))
        if fasting_hours is not None:
            meta["fasting_window_hours"] = fasting_hours
        if metabolic_stability is not None:
            meta["perceived_stability"] = metabolic_stability
        if hydration is not None:
            meta["hydration_status"] = hydration.upper()
        metrics["metabolic"] = meta

    if any(v is not None for v in [pain_sites, movement_count]):
        struct = dict(metrics.get("structural", {}))
        if pain_sites is not None:
            struct["pain_map"] = pain_sites
        if movement_count is not None:
            struct["movement_frequency_daily"] = movement_count
        metrics["structural"] = struct

    # ── Recompute score ────────────────────────────────────────────
    score, violations = _compute_score(metrics)

    # Readiness tiering (Phase 2)
    r_score = readiness_score(metrics)

    state["metrics"] = metrics
    state["well_score"] = score
    state["floors_violated"] = violations
    _save_state(state)

    event: dict[str, Any] = {
        "event": "WELL_LOG",
        "well_score": score,
        "floors_violated": violations,
        "tier": r_score["tier"],
    }
    if note:
        event["note"] = note
    _append_event(event)

    return {
        "ok": True,
        "well_score": score,
        "floors_violated": violations,
        "status": "DEGRADED" if violations else "STABLE",
        "tier": r_score["tier"],
        "recommendation": r_score["recommendation"],
        "human_decision_required": r_score["human_decision_required"],
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


@mcp.tool()
def well_pressure(
    load_delta: float,
    source: str = "forge",
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Signal cognitive pressure/load from an external source (e.g. A-FORGE).
    Increments decision_fatigue and potentially triggers W6 Metabolic Pause.
    """
    state = _load_state()
    metrics = state.get("metrics", {})
    cog = dict(metrics.get("cognitive", {"clarity": 10, "decision_fatigue": 0}))
    
    # Increment fatigue
    old_fatigue = cog.get("decision_fatigue", 0)
    new_fatigue = min(10.0, old_fatigue + load_delta)
    cog["decision_fatigue"] = new_fatigue
    metrics["cognitive"] = cog
    
    # W6 Logic: Repetitive Pressure Spike
    # If fatigue jumps > 2.0 in a single signal, flag as high-frequency loop
    violations = state.get("floors_violated", [])
    if load_delta > 2.0 and "W6_METABOLIC_PAUSE" not in violations:
        violations.append("W6_METABOLIC_PAUSE")
    
    # Recompute overall score
    score, new_violations = _compute_score(metrics)
    # Merge violations
    for v in new_violations:
        if v not in violations:
            violations.append(v)
            
    state["metrics"] = metrics
    state["well_score"] = score
    state["floors_violated"] = violations
    _save_state(state)
    
    _append_event({
        "event": "PRESSURE_SIGNAL",
        "source": source,
        "load_delta": load_delta,
        "new_fatigue": new_fatigue,
        "w6_triggered": "W6_METABOLIC_PAUSE" in violations
    })
    
    return {
        "ok": True,
        "well_score": score,
        "decision_fatigue": new_fatigue,
        "w6_active": "W6_METABOLIC_PAUSE" in violations,
        "message": "Metabolic Pause active. Step away for 15 minutes." if "W6_METABOLIC_PAUSE" in violations else "Pressure logged."
    }


@mcp.tool()
def well_readiness(ctx: Context | None = None) -> dict[str, Any]:
    """
    Reflect current biological readiness for arifOS JUDGE context.
    Returns score, floor status, and a readiness verdict for the constitutional kernel.
    W0: This is informational only — WELL never blocks unilaterally.
    """
    state = _load_state()
    score = state.get("well_score", 50)
    violations = state.get("floors_violated", [])
    metrics = state.get("metrics", {})

    if violations:
        verdict_str = "DEGRADED"
        status = "HOLD"
        message = f"Substrate flagging: {', '.join(violations)}. Strategic forge bandwidth throttled."
        risk = "RED"
        mode = "draft_only"
    elif score >= 80:
        verdict_str = "OPTIMAL"
        status = "PASS"
        message = "Substrate stable and high-capacity. Full forge bandwidth available."
        risk = "GREEN"
        mode = "full"
    elif score >= 60:
        verdict_str = "FUNCTIONAL"
        status = "PASS"
        message = "Substrate functional. Normal forge operations permitted."
        risk = "GREEN"
        mode = "structured"
    else:
        verdict_str = "LOW_CAPACITY"
        status = "CAUTION"
        message = "Substrate low-capacity. Recommend rest before strategic decisions."
        risk = "AMBER"
        mode = "draft_only"

    return _compose_verdict(
        mcp="AFWELL",
        task="readiness_reflection",
        status=status,
        domain_verdict=verdict_str,
        confidence="HIGH",
        risk_level=risk,
        recommended_mode=mode,
        human_required=score < 60 or bool(violations),
        next_safe_action=message
    )


@mcp.tool()
async def well_init(
    session_id: str | None = None,
    actor_id: str = "well-substrate",
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Open a WELL governance session — writes a 000_INIT event to VAULT999.
    Call this at the start of any WELL-aware session to anchor identity and
    connect to the canonical Merkle chain.
    Returns session_id and chain position for subsequent well_anchor seals.
    W0: WELL holds a mirror, not a veto. Operator sovereignty is invariant.
    """
    import sys
    import uuid as _uuid

    ARIFOS_PATH = "/root/arifOS"
    if ARIFOS_PATH not in sys.path:
        sys.path.append(ARIFOS_PATH)

    sid = session_id or f"well-session-{_uuid.uuid4().hex[:12]}"

    try:
        from arifosmcp.runtime.vault_postgres import seal_to_vault

        state = _load_state()
        score = state.get("well_score", 50)
        violations = state.get("floors_violated", [])

        res = await seal_to_vault(
            event_type="WELL_SESSION_INIT",
            session_id=sid,
            actor_id=actor_id,
            stage="000_INIT",
            verdict="ACTIVE",
            payload={
                "well_score": score,
                "floors_violated": violations,
                "w0": "OPERATOR_VETO_INTACT",
            },
            risk_tier="low",
        )

        _append_event({
            "event": "WELL_INIT",
            "session_id": sid,
            "vault_id": res.ledger_id if hasattr(res, "ledger_id") else str(res),
        })

        return {
            "ok": True,
            "session_id": sid,
            "stage": "000_INIT",
            "well_score": score,
            "chain_hash": res.chain_hash if hasattr(res, "chain_hash") else "",
            "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
        }
    except Exception as e:
        return {"ok": False, "session_id": sid, "error": str(e)}


@mcp.tool()
async def well_anchor(
    force: bool = False,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Anchor current WELL state to arifOS VAULT999 (PostgreSQL + Merkle).
    Ensures human substrate readiness is immutably recorded.
    """
    import sys
    from pathlib import Path
    
    # Ensure arifOS is in path for bridge
    ARIFOS_PATH = "/root/arifOS"
    if ARIFOS_PATH not in sys.path:
        sys.path.append(ARIFOS_PATH)
        
    try:
        from arifosmcp.runtime.well_bridge import anchor_well_to_vault
        res = await anchor_well_to_vault(force=force)
        
        if res["ok"]:
            _append_event({
                "event": "VAULT_ANCHOR_SQL",
                "vault_id": res["vault_id"],
                "hash": res["hash"]
            })
            
        return res
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def well_check_floors(ctx: Context | None = None) -> dict[str, Any]:
    """
    Check WELL floor status against all W-Floors.
    Returns per-floor status, overall verdict, and bandwidth recommendation for arifOS JUDGE.
    """
    state = _load_state()
    metrics = state.get("metrics", {})
    sleep = metrics.get("sleep", {})
    cognitive = metrics.get("cognitive", {})

    floors: dict[str, dict[str, Any]] = {
        "W0": {
            "name": "Sovereignty Invariant",
            "status": "INVARIANT",
            "detail": "Operator veto always intact. WELL never self-authorizes.",
        },
        "W1": {
            "name": "Sleep Integrity",
            "status": "OK",
            "threshold": "sleep_debt_days <= 2",
            "current": sleep.get("sleep_debt_days", 0),
        },
        "W5": {
            "name": "Cognitive Entropy",
            "status": "OK",
            "threshold": "clarity >= 4",
            "current": cognitive.get("clarity", 10),
        },
        "W6": {
            "name": "Incentive Decoupling",
            "status": "PHASE_3_PENDING",
            "detail": "Repetitive intent loop detection pending wearable integration.",
        },
    }

    if sleep.get("sleep_debt_days", 0) > 2:
        floors["W1"]["status"] = "VIOLATED"
    if cognitive.get("clarity", 10) < 4:
        floors["W5"]["status"] = "VIOLATED"

    violated = [k for k, v in floors.items() if v["status"] == "VIOLATED"]
    
    status = "PASS" if not violated else "HOLD"
    risk = "GREEN" if not violated else "RED"

    return _compose_verdict(
        mcp="AFWELL",
        task="floor_integrity_check",
        status=status,
        domain_verdict=f"{len(violated)} floors violated" if violated else "All floors clear",
        confidence="HIGH",
        risk_level=risk,
        recommended_mode="full" if not violated else "draft_only",
        human_required=bool(violated),
        failure_flags=violated
    )


# ── Phase 2 Tools (Expanded Surface) ───────────────────────────────────────────

@mcp.tool("well_log_state")
def well_log_state(
    sleep_hours: float | None = None,
    stress_level: float | None = None,
    clarity_score: float | None = None,
    note: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Log biological state entry to ledger (Phase 2).
    Simple interface for core metrics. Triggers readiness score recompute.
    """
    # Map to well_log tool logic
    return well_log(
        sleep_hours=sleep_hours,
        stress_load=stress_level,
        clarity=clarity_score,
        note=note,
        ctx=ctx
    )


@mcp.tool("well_get_readiness")
def well_get_readiness(ctx: Context | None = None) -> dict[str, Any]:
    """
    Return current readiness score + W-floor status (Phase 2).
    Includes GREEN|AMBER|RED tiering and human_decision_required flag.
    """
    state = _load_state()
    metrics = state.get("metrics", {})
    sleep = metrics.get("sleep", {})
    stress = metrics.get("stress", {})
    cognitive = metrics.get("cognitive", {})

    r_score = readiness_score(metrics)

    return {
        "ok": True,
        "well_score": state.get("well_score", 50),
        "readiness": r_score,
        "floors_violated": state.get("floors_violated", []),
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


@mcp.tool("well_check_floor")
def well_check_floor(floor_id: str | None = None, ctx: Context | None = None) -> dict[str, Any]:
    """
    Check specific W-floor (W1/W5/W6) — return Canonical Verdict.
    If floor_id is None, checks all floors via well_check_floors.
    """
    if not floor_id:
        return well_check_floors(ctx=ctx)

    fid = floor_id.upper()
    state = _load_state()
    metrics = state.get("metrics", {})
    sleep = metrics.get("sleep", {})
    cognitive = metrics.get("cognitive", {})

    passed = True
    status = "OK"
    detail = ""

    if fid == "W1":
        debt = sleep.get("sleep_debt_days", 0)
        passed = debt <= 2
        status = "OK" if passed else "VIOLATED"
        detail = f"Sleep debt: {debt} days (Limit: 2)"
    elif fid == "W5":
        clarity = cognitive.get("clarity", 10)
        passed = clarity >= 4
        status = "OK" if passed else "VIOLATED"
        detail = f"Clarity: {clarity}/10 (Limit: 4)"
    elif fid == "W6":
        violations = state.get("floors_violated", [])
        passed = "W6_METABOLIC_PAUSE" not in violations
        status = "OK" if passed else "VIOLATED"
        detail = "Metabolic Pause active" if not passed else "Incentive decoupling clear"
    elif fid == "W0":
        status = "INVARIANT"
        detail = "Operator sovereignty is absolute."
    else:
        return {"ok": False, "error": f"Unknown floor: {fid}"}

    return _compose_verdict(
        mcp="AFWELL",
        task=f"floor_check: {fid}",
        status="PASS" if passed else "HOLD",
        domain_verdict=status,
        confidence="HIGH",
        risk_level="GREEN" if passed else "RED",
        recommended_mode="full" if passed else "draft_only",
        human_required=not passed,
        next_safe_action=detail
    )


@mcp.tool()
def well_forge_mode_recommend(ctx: Context | None = None) -> dict[str, Any]:
    """
    Returns current forge mode recommendation for A-FORGE.
    Based on H-WELL + M-WELL + C-WELL state using Canonical Verdict.
    """
    res = well_forge_precheck(task_description="general_forge_recommendation", ctx=ctx)
    return res


@mcp.tool("well_list_log")
def well_list_log(limit: int = 10, ctx: Context | None = None) -> dict[str, Any]:
    """List recent biological state log entries (Phase 1/2)."""
    if not EVENTS_PATH.exists():
        return {"ok": True, "entries": []}

    entries = []
    try:
        with open(EVENTS_PATH, "r") as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                try:
                    entries.append(json.loads(line))
                except:
                    continue
    except Exception as e:
        return {"ok": False, "error": str(e)}

    return {"ok": True, "entries": entries[::-1]}


@mcp.tool("well_seal_vault")
async def well_seal_vault(force: bool = False, ctx: Context | None = None) -> dict[str, Any]:
    """
    Seal current biological state to VAULT999 via vault_bridge.py (Phase 2).
    Ensures immutability of the substrate mirror.
    """
    return await well_anchor(force=force, ctx=ctx)


# ══════════════════════════════════════════════════════════════════════════════
# WELL MVP PHASE 2 — arifOS Human Substrate Mirror
# 7 additions for arifOS-grade biological substrate governance
# ══════════════════════════════════════════════════════════════════════════════

# ── 1. Trend Analysis Engine ───────────────────────────────────────────────────

@mcp.tool()
def well_trend_analysis(ctx: Context | None = None) -> dict[str, Any]:
    """
    Detect directional trajectory across all WELL metrics.
    Answers: improving / stable / degrading / collapse-risk.
    Requires events.jsonl (written by well_log on every update).
    Looks back 7 days, 14 days, 30 days.
    """
    events_path = Path(__file__).parent / "events.jsonl"
    state = _load_state()
    metrics = state.get("metrics", {})
    score = state.get("well_score", 50)

    # Parse events for historical trend
    trend_data: dict[str, list] = {
        "sleep_debt": [], "clarity": [], "decision_fatigue": [],
        "stress_load": [], "well_score": [], "pressure_events": []
    }

    if events_path.exists():
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
        try:
            with open(events_path) as f:
                for line in f:
                    try:
                        e = json.loads(line)
                        epoch = datetime.datetime.fromisoformat(e.get("epoch", "2000-01-01"))
                        if epoch < cutoff:
                            continue
                        if e.get("event") == "WELL_LOG":
                            trend_data["well_score"].append((epoch, e.get("well_score", 50)))
                            trend_data["decision_fatigue"].append(
                                (epoch, metrics.get("cognitive", {}).get("decision_fatigue", 0))
                            )
                        elif e.get("event") == "PRESSURE_SIGNAL":
                            trend_data["pressure_events"].append((epoch, e.get("load_delta", 0)))
                    except:
                        continue
        except Exception:
            pass

    # Current values
    sleep_debt = metrics.get("sleep", {}).get("sleep_debt_days", 0)
    clarity = metrics.get("cognitive", {}).get("clarity", 10)
    fatigue = metrics.get("cognitive", {}).get("decision_fatigue", 0)
    stress = metrics.get("stress", {}).get("subjective_load", 0)

    # Direction heuristics (from available data or current state)
    score_trend = "stable"
    if trend_data["well_score"]:
        sorted_scores = sorted(trend_data["well_score"], key=lambda x: x[0])
        if len(sorted_scores) >= 2:
            delta = sorted_scores[-1][1] - sorted_scores[0][1]
            if delta > 5:
                score_trend = "improving"
            elif delta < -5:
                score_trend = "degrading"

    # Pressure frequency
    pressure_count = len(trend_data.get("pressure_events", []))
    pressure_trend = "rising" if pressure_count > 3 else "normal"

    # Trajectory determination
    violation_count = len(state.get("floors_violated", []))
    if score < 40 or (violation_count >= 2 and score_trend == "degrading"):
        trajectory = "collapse-risk"
    elif score_trend == "degrading" or (fatigue > 6 and stress > 7):
        trajectory = "degrading"
    elif score_trend == "improving" and score >= 75:
        trajectory = "improving"
    else:
        trajectory = "stable"

    return {
        "ok": True,
        "trajectory": trajectory,
        "score": score,
        "score_trend": score_trend,
        "pressure_trend": pressure_trend,
        "pressure_events_30d": pressure_count,
        "metrics": {
            "sleep_debt_days": sleep_debt,
            "clarity": clarity,
            "decision_fatigue": fatigue,
            "stress_load": stress,
        },
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ── 2. Bandwidth Recommendation ───────────────────────────────────────────────

@mcp.tool()
def well_bandwidth_recommendation(ctx: Context | None = None) -> dict[str, Any]:
    """
    Action translation layer — maps WELL state to operational mode.
    Not just 'you are tired' but 'your state supports X but not Y.'
    For arifOS kernel: WELL does not block, it informs mode.
    """
    state = _load_state()
    score = state.get("well_score", 50)
    violations = state.get("floors_violated", [])
    metrics = state.get("metrics", {})
    cognitive = metrics.get("cognitive", {})
    sleep = metrics.get("sleep", {})

    fatigue = cognitive.get("decision_fatigue", 0)
    clarity = cognitive.get("clarity", 10)
    sleep_debt = sleep.get("sleep_debt_days", 0)

    # Determine operational mode
    if score >= 80 and not violations:
        mode = "FULL"
        verdict = "OPTIMAL"
        allowed = ["C0", "C1", "C2", "C3", "C4", "C5"]
        message = "Full architecture, coding, strategy, public writing. All decision classes open."
    elif score >= 60 and len(violations) <= 1:
        mode = "NORMAL"
        verdict = "FUNCTIONAL"
        allowed = ["C0", "C1", "C2", "C3"]
        forbidden = ["C4", "C5"]
        message = "Normal work. Keep structure. Avoid irreversible commitments."
    elif score >= 40 or (violations and score >= 50):
        mode = "RESTRICTED"
        verdict = "DEGRADED"
        allowed = ["C0", "C1"]
        forbidden = ["C2", "C3", "C4", "C5"]
        message = "Draft only. Reversible tasks. No major commitments or public actions."
    else:
        mode = "LOCKED"
        verdict = "LOW_CAPACITY"
        allowed = ["C0"]
        forbidden = ["C1", "C2", "C3", "C4", "C5"]
        message = "Pause. Recover. No consequential decisions."

    # W7 — Cognitive Load Threshold (new floor)
    if fatigue > 7 and clarity < 5:
        mode = "LOCKED"
        verdict = "COGNITIVE_OVERLOAD"
        allowed = ["C0"]
        forbidden = ["C1", "C2", "C3", "C4", "C5"]
        message = "Cognitive overload detected. All judgment suspended until recovery."

    return {
        "ok": True,
        "verdict": verdict,
        "mode": mode,
        "decision_classes_allowed": allowed,
        "decision_classes_forbidden": forbidden,
        "message": message,
        "current_score": score,
        "active_violations": violations,
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ── 3. Recovery Protocol ──────────────────────────────────────────────────────

@mcp.tool()
def well_recovery_protocol(ctx: Context | None = None) -> dict[str, Any]:
    """
    Suggest stabilizing actions based on current WELL state.
    Not medical advice — operational self-regulation support.
    Returns structured recovery steps ordered by priority.
    """
    state = _load_state()
    metrics = state.get("metrics", {})
    score = state.get("well_score", 50)
    violations = state.get("floors_violated", [])

    actions: list[dict[str, str]] = []
    warnings: list[str] = []

    sleep = metrics.get("sleep", {})
    cognitive = metrics.get("cognitive", {})
    stress = metrics.get("stress", {})
    metabolic = metrics.get("metabolic", {})

    # Hydration (always first if dehydrated or unknown)
    if metabolic.get("hydration_status", "") in ("DEHYDRATED", "", "STABLE"):
        if metabolic.get("hydration_status") == "DEHYDRATED":
            actions.append({"priority": "P0", "action": "Hydrate immediately", "reason": "Dehydration detected"})
        elif not metabolic.get("hydration_status"):
            actions.append({"priority": "P1", "action": "Drink water", "reason": "Hydration status unknown"})

    # Sleep debt
    debt = sleep.get("sleep_debt_days", 0)
    if debt > 1:
        actions.append({"priority": "P1", "action": "Prioritize sleep tonight", "reason": f"Sleep debt: {debt} days"})
        if debt > 2:
            warnings.append(f"Sleep debt ({debt}d) exceeds W1 threshold. Strategic decisions should wait.")

    # Cognitive fatigue
    fatigue = cognitive.get("decision_fatigue", 0)
    if fatigue > 5:
        actions.append({"priority": "P1", "action": "Step away for 15 minutes minimum", "reason": f"Decision fatigue: {fatigue}/10"})
    if fatigue > 7:
        warnings.append("High decision fatigue — avoid consequential choices until recovery.")
        actions.append({"priority": "P2", "action": "No financial or legal decisions", "reason": "Cognitive overload"})

    # Stress
    load = stress.get("subjective_load", 0)
    if load > 7:
        actions.append({"priority": "P1", "action": "Walk 10 minutes, change environment", "reason": f"Stress load: {load}/10"})
        warnings.append("High stress load — public replies and conflict decisions should be delayed.")

    # Fasting/metabolic
    fasting = metabolic.get("fasting_window_hours", 0)
    if fasting > 16:
        actions.append({"priority": "P2", "action": "Eat before major decisions", "reason": f"Fasting {fasting}h — glucose may be low"})

    # Clarity
    clarity = cognitive.get("clarity", 10)
    if clarity < 6:
        actions.append({"priority": "P2", "action": "Convert tasks to draft-only mode", "reason": f"Clarity: {clarity}/10"})

    # No known issues — positive affirmation
    if not actions:
        actions.append({"priority": "P0", "action": "Maintain current rhythm", "reason": "No recovery triggers detected"})

    return {
        "ok": True,
        "well_score": score,
        "recovery_actions": actions,
        "warnings": warnings,
        "verdict": "DEGRADED" if warnings else "STABLE",
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT — not medical advice",
    }


# ── 4. Niat / Intent Check ─────────────────────────────────────────────────────

@mcp.tool()
def well_niat_check(
    intent: str,
    context: str | None = None,
    reversibility: str = "unknown",
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Before high-impact action, check alignment between intent and biological state.
    W0: WELL never blocks — it only informs. Operator retains all sovereignty.

    Questions checked:
    - Is the intent clear?
    - Is this reversible?
    - Is current state stable enough?
    - Is emotion driving the action?
    - Does this need Arif's fresh confirmation?
    """
    state = _load_state()
    score = state.get("well_score", 50)
    violations = state.get("floors_violated", [])
    metrics = state.get("metrics", {})
    cognitive = metrics.get("cognitive", {})
    stress = metrics.get("stress", {})

    fatigue = cognitive.get("decision_fatigue", 0)
    clarity = cognitive.get("clarity", 10)
    stress_load = stress.get("subjective_load", 0)

    # Assessment
    questions = {
        "intent_clear": {
            "question": "Is the intent clear?",
            "result": "UNCLEAR" if not intent else "CLEAR",
            "detail": f"Intent: {intent or 'none provided'}",
        },
        "reversibility": {
            "question": "Is this reversible?",
            "result": "REVERSIBLE" if reversibility == "reversible" else "PROCEED_WITH_CAUTION" if reversibility == "unknown" else "IRREVERSIBLE",
            "detail": f"Reversibility: {reversibility}",
        },
        "state_stable": {
            "question": "Is current state stable?",
            "result": "STABLE" if score >= 70 and not violations else "UNSTABLE",
            "detail": f"Score: {score}, Violations: {violations or 'none'}",
        },
        "emotion_driven": {
            "question": "Is emotion driving this?",
            "result": "LIKELY" if stress_load > 7 else "POSSIBLE" if stress_load > 5 else "UNLIKELY",
            "detail": f"Stress load: {stress_load}/10",
        },
        "fresh_confirmation": {
            "question": "Does this need Arif's fresh confirmation?",
            "result": "REQUIRED" if (fatigue > 5 or clarity < 7 or score < 65) else "NOT_REQUIRED",
            "detail": f"Fatigue: {fatigue}/10, Clarity: {clarity}/10",
        },
    }

    # Overall recommendation
    flags = sum(1 for q in questions.values() if q["result"] in ("UNSTABLE", "LIKELY", "REQUIRED", "IRREVERSIBLE", "UNCLEAR"))

    if flags >= 3 or score < 40:
        recommendation = "HOLD — delay action"
        readiness = "BLOCKED"
        reason = "Multiple WELL indicators flag this action as high-risk in current state."
    elif flags >= 1:
        recommendation = "CAUTION — proceed with review"
        readiness = "CONDITIONAL"
        reason = "Some indicators flag caution. Consider delaying or drafting only."
    else:
        recommendation = "PROCEED"
        readiness = "READY"
        reason = "Biological state supports this intent."

    return {
        "ok": True,
        "intent": intent,
        "context": context,
        "readiness": readiness,
        "recommendation": recommendation,
        "reason": reason,
        "questions": questions,
        "flag_count": flags,
        "score": score,
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ── 5. Decision Class Gate ──────────────────────────────────────────────────────

@mcp.tool()
def well_decision_classify(
    task_description: str | None = None,
    decision_class: str | None = None,  # Allow pre-specified class
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Classify a task or decision into C0-C5 risk tiers.
    If class is pre-specified, validate against current WELL state.
    If class is not specified, auto-classify from description.

    Decision Classes:
    C0 = Notes, journaling (always safe)
    C1 = Drafting, organizing (usually safe)
    C2 = Coding, testing (needs focus)
    C3 = Public posting (needs clarity)
    C4 = Money/legal/work decision (needs stability)
    C5 = Irreversible/reputational (requires high readiness + explicit confirmation)
    """
    state = _load_state()
    score = state.get("well_score", 50)
    violations = state.get("floors_violated", [])
    metrics = state.get("metrics", {})
    cognitive = metrics.get("cognitive", {})

    fatigue = cognitive.get("decision_fatigue", 0)
    clarity = cognitive.get("clarity", 10)

    # Auto-classify from description keywords
    if decision_class is None and task_description:
        desc = task_description.lower()
        if any(k in desc for k in ["publish", "post", "public", "tweet", "broadcast", "announce", "article", "essay"]):
            decision_class = "C3"
        elif any(k in desc for k in ["money", "financial", "invest", "budget", "contract", "legal", "hire", "fire", "delete account"]):
            decision_class = "C4"
        elif any(k in desc for k in ["irreversible", "delete", "permanent", "revoke", "architecture", "schema migration"]):
            decision_class = "C5"
        elif any(k in desc for k in ["code", "refactor", "deploy", "build", "implement", "feature"]):
            decision_class = "C2"
        elif any(k in desc for k in ["draft", "outline", "note", "journal", "log", "草稿"]):
            decision_class = "C1"
        else:
            decision_class = "C0"

    if decision_class is None:
        return {"ok": False, "error": "Either task_description or decision_class required"}

    # Validate against WELL state
    class_requirements = {
        "C0": {"min_score": 0, "max_fatigue": 10, "max_stress": 10, "clarity_min": 0},
        "C1": {"min_score": 40, "max_fatigue": 8, "max_stress": 9, "clarity_min": 4},
        "C2": {"min_score": 55, "max_fatigue": 6, "max_stress": 7, "clarity_min": 6},
        "C3": {"min_score": 65, "max_fatigue": 5, "max_stress": 6, "clarity_min": 7},
        "C4": {"min_score": 75, "max_fatigue": 4, "max_stress": 5, "clarity_min": 8},
        "C5": {"min_score": 85, "max_fatigue": 3, "max_stress": 4, "clarity_min": 9},
    }

    req = class_requirements.get(decision_class, class_requirements["C0"])

    score_ok = score >= req["min_score"]
    fatigue_ok = fatigue <= req["max_fatigue"]
    clarity_ok = clarity >= req["clarity_min"]

    stress = metrics.get("stress", {}).get("subjective_load", 0)
    stress_ok = stress <= req["max_stress"]

    all_clear = score_ok and fatigue_ok and clarity_ok and stress_ok

    if all_clear:
        verdict = "APPROVED"
        message = f"WELL state supports {decision_class} tasks."
    else:
        verdict = "CAUTION" if score >= 40 else "BLOCKED"
        blocked_reasons = []
        if not score_ok: blocked_reasons.append(f"score {score} < required {req['min_score']}")
        if not fatigue_ok: blocked_reasons.append(f"fatigue {fatigue} > max {req['max_fatigue']}")
        if not clarity_ok: blocked_reasons.append(f"clarity {clarity} < min {req['clarity_min']}")
        if not stress_ok: blocked_reasons.append(f"stress {stress} > max {req['max_stress']}")
        message = f"WELL advises caution for {decision_class}: {" | ".join(blocked_reasons)}"

    return {
        "ok": True,
        "decision_class": decision_class,
        "verdict": verdict,
        "message": message,
        "checks": {
            "score_ok": score_ok,
            "fatigue_ok": fatigue_ok,
            "clarity_ok": clarity_ok,
            "stress_ok": stress_ok,
        },
        "current_state": {
            "score": score,
            "fatigue": fatigue,
            "clarity": clarity,
            "stress": stress,
        },
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ── 6. arifOS Handoff Packet ────────────────────────────────────────────────────

@mcp.tool()
def well_arifos_packet(ctx: Context | None = None) -> dict[str, Any]:
    """
    Emit a clean, structured context packet for arifOS governance kernel.
    This is the canonical handoff format from WELL to arifOS.

    arifOS asks: Is the Judge biologically ready?
    WELL answers with this packet.
    """
    state = _load_state()
    score = state.get("well_score", 50)
    violations = state.get("floors_violated", [])
    metrics = state.get("metrics", {})
    cognitive = metrics.get("cognitive", {})
    sleep = metrics.get("sleep", {})
    stress = metrics.get("stress", {})

    fatigue = cognitive.get("decision_fatigue", 0)
    clarity = cognitive.get("clarity", 10)
    sleep_debt = sleep.get("sleep_debt_days", 0)
    stress_load = stress.get("subjective_load", 0)

    # Determine safe mode
    if score >= 80 and not violations:
        safe_mode = "full"
        readiness = "OPTIMAL"
    elif score >= 60:
        safe_mode = "normal"
        readiness = "FUNCTIONAL"
    elif score >= 40:
        safe_mode = "draft_only"
        readiness = "DEGRADED"
    else:
        safe_mode = "suspended"
        readiness = "LOW_CAPACITY"

    # Decision classes
    if safe_mode == "full":
        classes_allowed = ["C0", "C1", "C2", "C3", "C4", "C5"]
    elif safe_mode == "normal":
        classes_allowed = ["C0", "C1", "C2", "C3"]
    elif safe_mode == "draft_only":
        classes_allowed = ["C0", "C1"]
    else:
        classes_allowed = ["C0"]

    # Human confirmation required
    human_confirmation = (
        safe_mode in ("draft_only", "suspended") or
        fatigue > 5 or
        score < 60 or
        len(violations) > 0
    )

    # What to avoid
    avoid = []
    if fatigue > 5: avoid.append("consequential_decisions")
    if stress_load > 7: avoid.append("public_commitment")
    if sleep_debt > 1: avoid.append("irreversible_actions")
    if score < 50: avoid.extend(["financial_decision", "conflict_reply", "public_posting"])

    return {
        "ok": True,
        "readiness": readiness,
        "safe_mode": safe_mode,
        "well_score": score,
        "decision_classes_allowed": classes_allowed,
        "avoid": avoid if avoid else None,
        "human_confirmation_required": human_confirmation,
        "active_violations": violations,
        "operator_snapshot": {
            "sleep_debt_days": sleep_debt,
            "clarity": clarity,
            "decision_fatigue": fatigue,
            "stress_load": stress_load,
        },
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ── 7. W0 Consent & Privacy Floor ───────────────────────────────────────────────

W0_CONSENT_VERSION = "1.0"
W0_TELEMETRY_PURPOSES = ["governance_readiness", "arifOS_kernel_context", "vault_anchor", "operator_self-regulation"]

@mcp.tool()
def well_consent_status(ctx: Context | None = None) -> dict[str, Any]:
    """
    Return W0 Sovereignty & Telemetry Consent status.
    This is a hard floor — WELL never operates without operator consent.
    W0: WELL holds a mirror, not a veto. Operator sovereignty is invariant.
    """
    return {
        "ok": True,
        "w0_version": W0_CONSENT_VERSION,
        "axiom": "WELL holds a mirror, not a veto. Operator sovereignty is invariant.",
        "rules": [
            "WELL may reflect, recommend, and anchor only within Arif's consent.",
            "WELL must never shame, coerce, diagnose, manipulate, or override.",
            "Telemetry is private, sensitive, purpose-limited, and revocable.",
            "WELL never self-authorizes any action on behalf of the operator.",
            "Any WELL output is advisory only — operator retains full veto.",
        ],
        "consent_active": True,  # Hard-coded: Arif owns this system
        "telemetry_purposes": W0_TELEMETRY_PURPOSES,
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ══════════════════════════════════════════════════════════════════════════════
# WELL MVP PHASE 3 — Medical Boundary + Pressure Ledger + Daily Brief
# ══════════════════════════════════════════════════════════════════════════════

# ── 8. Medical Boundary Guard ────────────────────────────────────────────────

MEDICAL_RED_FLAGS = [
    "chest pain", "difficulty breathing", "severe injury", "unconscious",
    "suicidal ideation", "panic attack lasting >30min", " sudden numbness",
    "blood pressure crisis", "seizure", "stroke symptoms",
]

@mcp.tool()
def well_medical_boundary(ctx: Context | None = None) -> dict[str, Any]:
    """
    Explicit non-diagnosis guard for WELL.
    WELL is not a doctor, therapist, or diagnostic authority.
    It tracks readiness signals only.
    For severe, persistent, or urgent symptoms, recommend professional care.

    This protects operator dignity and safety.
    """
    state = _load_state()
    metrics = state.get("metrics", {})
    score = state.get("well_score", 50)

    return {
        "ok": True,
        "boundary": "WELL is not a medical authority.",
        "rules": [
            "WELL tracks readiness signals — it does not diagnose conditions.",
            "WELL does not interpret medical symptoms.",
            "WELL does not prescribe treatments or medications.",
            "WELL does not replace professional medical advice.",
            "For severe, persistent, or urgent symptoms: seek professional care.",
        ],
        "red_flag_recommendation": "If you experience severe, persistent, or urgent physical or mental symptoms, contact a qualified healthcare provider or emergency services.",
        "scope": "readiness_signals / biological_telemetry / operational_self-regulation",
        "out_of_scope": ["diagnosis", "prescription", "medical_treatment", "crisis_counseling"],
        "current_score": score,
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ── 9. Pressure Source Ledger ────────────────────────────────────────────────

PRESSURE_SOURCES = [
    "work", "family", "financial", "coding/debugging",
    "public_identity", "conflict", "sleep_disruption",
    "health", "spiritual/emotional_load",
]

@mcp.tool()
def well_pressure_ledger(
    log_source: str | None = None,
    intensity: float | None = None,
    note: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Log or retrieve pressure events categorized by source.
    Answers: 'What is draining Arif's judgment bandwidth?'

    Categories: work / family / financial / coding-debugging / public_identity / conflict / sleep_disruption / health / spiritual-emotional_load
    """
    events_path = Path(__file__).parent / "events.jsonl"
    state = _load_state()

    # If logging a new event
    if log_source:
        if log_source not in PRESSURE_SOURCES:
            return {"ok": False, "error": f"Unknown source. Must be one of: {PRESSURE_SOURCES}"}

        intensity = intensity or 5.0
        event = {
            "event": "PRESSURE_LEDGER",
            "source": log_source,
            "intensity": min(10.0, max(0.0, float(intensity))),
            "note": note,
            "epoch": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        with open(events_path, "a") as f:
            f.write(json.dumps(event) + "\n")

        # Update cognitive pressure in state
        metrics = state.get("metrics", {})
        cog = dict(metrics.get("cognitive", {}))
        cog["pressure_sources"] = cog.get("pressure_sources", {})
        cog["pressure_sources"][log_source] = cog["pressure_sources"].get(log_source, 0) + intensity
        metrics["cognitive"] = cog
        state["metrics"] = metrics
        _save_state(state)

        return {
            "ok": True,
            "logged": {"source": log_source, "intensity": intensity},
            "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
        }

    # Otherwise, retrieve ledger summary
    source_totals: dict[str, float] = {}
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14)

    if events_path.exists():
        try:
            with open(events_path) as f:
                for line in f:
                    try:
                        e = json.loads(line)
                        if e.get("event") == "PRESSURE_LEDGER":
                            src = e.get("source", "unknown")
                            intensity_val = e.get("intensity", 0)
                            source_totals[src] = source_totals.get(src, 0) + intensity_val
                    except:
                        continue
        except Exception:
            pass

    # Sort by drain
    sorted_sources = sorted(source_totals.items(), key=lambda x: x[1], reverse=True)
    top_drain = sorted_sources[0] if sorted_sources else (None, 0)

    return {
        "ok": True,
        "period_days": 14,
        "source_totals": dict(sorted_sources) if sorted_sources else {},
        "top_drain": {"source": top_drain[0], "intensity": top_drain[1]} if top_drain[0] else None,
        "all_sources": PRESSURE_SOURCES,
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ── 10. WELL Daily Brief ─────────────────────────────────────────────────────

@mcp.tool()
def well_daily_brief(ctx: Context | None = None) -> dict[str, Any]:
    """
    Daily operator dashboard — one consolidated briefing.
    Readiness / Main Risk / Best Task Class / Avoid / Recovery Move / arifOS Mode

    Designed for morning or pre-session check-in.
    """
    state = _load_state()
    score = state.get("well_score", 50)
    violations = state.get("floors_violated", [])
    metrics = state.get("metrics", {})
    cognitive = metrics.get("cognitive", {})
    sleep = metrics.get("sleep", {})
    stress = metrics.get("stress", {})
    metabolic = metrics.get("metabolic", {})

    fatigue = cognitive.get("decision_fatigue", 0)
    clarity = cognitive.get("clarity", 10)
    sleep_debt = sleep.get("sleep_debt_days", 0)
    stress_load = stress.get("subjective_load", 0)
    hydration = metabolic.get("hydration_status", "UNKNOWN")

    # Readiness verdict
    if score >= 80 and not violations:
        readiness = "FUNCTIONAL"
        arifos_mode = "full / open"
    elif score >= 60:
        readiness = "FUNCTIONAL"
        arifos_mode = "structured / normal"
    elif score >= 40:
        readiness = "DEGRADED"
        arifos_mode = "draft_only / low_option"
    else:
        readiness = "LOW_CAPACITY"
        arifos_mode = "suspended / minimal"

    # Main risk
    risks = []
    if sleep_debt > 1:
        risks.append(f"sleep_debt_{sleep_debt}d")
    if fatigue > 5:
        risks.append(f"decision_fatigue_{fatigue}")
    if stress_load > 7:
        risks.append(f"high_stress_{stress_load}")
    if clarity < 7:
        risks.append(f"low_clarity_{clarity}")
    main_risk = risks[0] if risks else "none"

    # Best task class
    if score >= 75:
        best_class = "architecture + coding + strategy + public writing"
    elif score >= 55:
        best_class = "drafting + review + testing"
    elif score >= 40:
        best_class = "notes + journaling + organizing"
    else:
        best_class = "rest only"

    # What to avoid
    avoid = []
    if score < 50: avoid.append("irreversible decisions")
    if fatigue > 6: avoid.append("major commitments after 10pm")
    if stress_load > 7: avoid.append("public posts / conflict replies")
    if sleep_debt > 2: avoid.append("strategic decisions until sleep recovered")

    # Recovery move
    recovery = []
    if hydration != "HYDRATED": recovery.append("hydration first")
    if sleep_debt > 0: recovery.append("20-min walk + prioritize sleep tonight")
    if fatigue > 5: recovery.append("15-min break before next task")
    if stress_load > 6: recovery.append("environment change + breath work")
    if not recovery:
        recovery = ["maintain current rhythm"]

    # Time-based note
    now = datetime.datetime.now(datetime.timezone.utc)
    hour = now.hour
    time_note = ""
    if hour >= 22 or hour < 6:
        time_note = " — late night window, defer consequential decisions"

    return {
        "ok": True,
        "readiness": readiness,
        "well_score": score,
        "main_risk": main_risk,
        "best_task_class": best_class,
        "avoid": avoid if avoid else ["none"],
        "recovery_move": recovery[0] if len(recovery) == 1 else recovery,
        "arifOS_mode": arifos_mode + time_note,
        "active_violations": violations if violations else ["none"],
        "timestamp": now.isoformat(),
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ══════════════════════════════════════════════════════════════════════════════
# M-WELL — Machine Substrate
# Tracks tool/system health, model reliability, context integrity, compute limits
# Purpose: Is the Instrument technically reliable enough for this task?
# ══════════════════════════════════════════════════════════════════════════════

# M-WELL State — loads machine telemetry from state.json (m_machine section)
@mcp.tool()
def well_machine_state(ctx: Context | None = None) -> dict[str, Any]:
    """
    Read current machine substrate state.
    Tracks: model reliability, tool availability, latency, context pressure,
    memory integrity, API failure rate, data freshness, compute budget, security flags.
    """
    state = _load_state()
    m_machine = state.get("m_machine", {})

    # Defaults for all machine metrics
    default_metrics = {
        "model_reliability": 1.0,    # 0-1
        "tool_availability": 1.0,     # 0-1
        "latency_ms": 200,            # ms
        "context_length_pressure": 0.0,  # 0-1 (1 = near limit)
        "memory_integrity": 1.0,      # 0-1
        "api_failure_rate": 0.0,      # 0-1
        "data_freshness": 1.0,       # 0-1
        "compute_budget_pct": 100.0,  # remaining %
        "token_budget_pct": 100.0,    # remaining %
        "security_flags": [],         # list of flag names
        "vault_status": "ok",        # ok / degraded / offline
        "schema_valid": True,
    }

    machine_metrics = {**default_metrics, **m_machine}

    # Compute M-WELL score
    score = (
        machine_metrics["model_reliability"] * 20 +
        machine_metrics["tool_availability"] * 15 +
        max(0, 1 - machine_metrics["api_failure_rate"]) * 15 +
        max(0, 1 - machine_metrics["context_length_pressure"]) * 15 +
        machine_metrics["memory_integrity"] * 10 +
        machine_metrics["data_freshness"] * 10 +
        max(0, machine_metrics["compute_budget_pct"] / 100) * 10 +
        max(0, machine_metrics["token_budget_pct"] / 100) * 5
    )
    score = round(min(100.0, score), 1)

    # Verdict
    if score >= 85:
        verdict = "HEALTHY"
        mode = "full"
    elif score >= 65:
        verdict = "FUNCTIONAL"
        mode = "normal"
    elif score >= 45:
        verdict = "DEGRADED"
        mode = "reduced"
    else:
        verdict = "CRITICAL"
        mode = "suspended"

    return {
        "ok": True,
        "m_well_verdict": verdict,
        "m_well_score": score,
        "mode": mode,
        "metrics": machine_metrics,
        "security_flags": machine_metrics.get("security_flags", []),
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT — M-WELL is instrument, not authority",
    }


@mcp.tool()
def well_machine_log(
    model_reliability: float | None = None,
    tool_availability: float | None = None,
    latency_ms: float | None = None,
    context_pressure: float | None = None,
    memory_integrity: float | None = None,
    api_failure_rate: float | None = None,
    data_freshness: float | None = None,
    compute_budget: float | None = None,
    token_budget: float | None = None,
    security_flag: str | None = None,
    vault_status: str | None = None,
    schema_valid: bool | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Log machine substrate telemetry.
    All values are 0-1 scale (normalized) or absolute ms for latency.
    """
    state = _load_state()
    m_machine = dict(state.get("m_machine", {}))

    if model_reliability is not None:
        m_machine["model_reliability"] = max(0.0, min(1.0, model_reliability))
    if tool_availability is not None:
        m_machine["tool_availability"] = max(0.0, min(1.0, tool_availability))
    if latency_ms is not None:
        m_machine["latency_ms"] = max(0, latency_ms)
    if context_pressure is not None:
        m_machine["context_length_pressure"] = max(0.0, min(1.0, context_pressure))
    if memory_integrity is not None:
        m_machine["memory_integrity"] = max(0.0, min(1.0, memory_integrity))
    if api_failure_rate is not None:
        m_machine["api_failure_rate"] = max(0.0, min(1.0, api_failure_rate))
    if data_freshness is not None:
        m_machine["data_freshness"] = max(0.0, min(1.0, data_freshness))
    if compute_budget is not None:
        m_machine["compute_budget_pct"] = max(0.0, min(100.0, compute_budget))
    if token_budget is not None:
        m_machine["token_budget_pct"] = max(0.0, min(100.0, token_budget))
    if vault_status is not None:
        m_machine["vault_status"] = vault_status.lower()
    if schema_valid is not None:
        m_machine["schema_valid"] = bool(schema_valid)

    # Append security flag
    if security_flag:
        flags = list(m_machine.get("security_flags", []))
        if security_flag not in flags:
            flags.append(security_flag)
        m_machine["security_flags"] = flags

    state["m_machine"] = m_machine
    _save_state(state)

    _append_event({
        "event": "M_WELL_LOG",
        "metrics_logged": list(m_machine.keys()),
    })

    return {
        "ok": True,
        "m_machine": m_machine,
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


@mcp.tool()
def well_machine_reliability(
    target_task: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Assess machine substrate reliability for a specific task type.
    Task types: coding / reasoning / creative / memory / critical / real_time
    """
    m_state = well_machine_state(ctx=None)
    metrics = m_state.get("metrics", {})
    score = m_state.get("m_well_score", 0)

    # Task-specific thresholds
    task_requirements = {
        "coding": {"min_reliability": 0.8, "max_latency": 2000, "max_context_pressure": 0.8},
        "reasoning": {"min_reliability": 0.75, "max_latency": 3000, "max_context_pressure": 0.7},
        "creative": {"min_reliability": 0.7, "max_latency": 5000, "max_context_pressure": 0.9},
        "memory": {"min_reliability": 0.9, "max_latency": 500, "max_context_pressure": 0.5, "min_memory_integrity": 0.95},
        "critical": {"min_reliability": 0.95, "max_latency": 1000, "max_context_pressure": 0.5},
        "real_time": {"min_reliability": 0.85, "max_latency": 500, "max_context_pressure": 0.6},
    }

    if target_task and target_task in task_requirements:
        req = task_requirements[target_task]
        checks = {
            "reliability_ok": metrics.get("model_reliability", 0) >= req["min_reliability"],
            "latency_ok": metrics.get("latency_ms", 0) <= req["max_latency"],
            "context_ok": metrics.get("context_length_pressure", 0) <= req["max_context_pressure"],
        }
        if "min_memory_integrity" in req:
            checks["memory_integrity_ok"] = metrics.get("memory_integrity", 0) >= req["min_memory_integrity"]
        all_ok = all(checks.values())
        return {
            "ok": True,
            "task": target_task,
            "verdict": "APPROVED" if all_ok else "CAUTION",
            "checks": checks,
            "m_well_score": score,
            "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
        }

    return {
        "ok": True,
        "verdict": m_state.get("m_well_verdict", "UNKNOWN"),
        "m_well_score": score,
        "mode": m_state.get("mode", "unknown"),
        "task": target_task or "general",
        "available_task_types": list(task_requirements.keys()),
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ══════════════════════════════════════════════════════════════════════════════
# C-WELL — Coupled Readiness
# Evaluates interaction risk between human state and machine state
# Purpose: Is the human-machine pair safe to proceed?
# ══════════════════════════════════════════════════════════════════════════════

COUPLED_RISK_PATTERNS = [
    {"h_key": "decision_fatigue", "h_thresh": 6, "m_key": "context_length_pressure", "m_thresh": 0.7, "risk": "context_overload_coding"},
    {"h_key": "stress_load", "h_thresh": 7, "m_key": "model_reliability", "m_thresh": 0.75, "risk": "high_stress_public_writing"},
    {"h_key": "sleep_debt_days", "h_thresh": 2, "m_key": "api_failure_rate", "m_thresh": 0.1, "risk": "low_sleep_financial_decision"},
    {"h_key": "decision_fatigue", "h_thresh": 7, "m_key": "memory_integrity", "m_thresh": 0.8, "risk": "fatigue_irreversible_action"},
    {"h_key": "stress_load", "h_thresh": 8, "m_key": "tool_availability", "m_thresh": 0.8, "risk": "stress_tool_gap"},
    {"h_key": "clarity", "h_thresh": 5, "m_key": "model_reliability", "m_thresh": 0.7, "risk": "low_clarity_complex_coding"},
    {"h_key": "decision_fatigue", "h_thresh": 5, "m_key": "latency_ms", "m_thresh": 3000, "risk": "fatigue_high_latency"},
]

@mcp.tool()
def well_coupled_readiness(ctx: Context | None = None) -> dict[str, Any]:
    """
    C-WELL: Evaluate coupled human-machine readiness.

    Checks interaction risks between Arif's biological state and machine health.
    Returns human_readiness, machine_readiness, coupled_risk, and recommended_mode.

    Key rule: Human substrate and machine substrate are separate.
    Governance sees both. Judgment remains Arif's.
    """
    h_state = _load_state()
    h_metrics = h_state.get("metrics", {})
    h_score = h_state.get("well_score", 50)
    h_violations = h_state.get("floors_violated", [])

    cognitive = h_metrics.get("cognitive", {})
    stress = h_metrics.get("stress", {})
    sleep = h_metrics.get("sleep", {})

    m_state = well_machine_state(ctx=None)
    m_metrics = m_state.get("metrics", {})
    m_score = m_state.get("m_well_score", 100)
    m_verdict = m_state.get("m_well_verdict", "UNKNOWN")

    # Human verdict
    if h_score >= 80 and not h_violations:
        h_verdict = "OPTIMAL"
    elif h_score >= 60:
        h_verdict = "FUNCTIONAL"
    elif h_score >= 40:
        h_verdict = "DEGRADED"
    else:
        h_verdict = "LOW_CAPACITY"

    # Coupled risk detection
    h_vals = {
        "decision_fatigue": cognitive.get("decision_fatigue", 0),
        "clarity": cognitive.get("clarity", 10),
        "stress_load": stress.get("subjective_load", 0),
        "sleep_debt_days": sleep.get("sleep_debt_days", 0),
    }

    risks_found = []
    for pattern in COUPLED_RISK_PATTERNS:
        h_val = h_vals.get(pattern["h_key"], 0)
        m_val = m_metrics.get(pattern["m_key"], 0)
        h_triggered = h_val >= pattern["h_thresh"]
        m_triggered = m_val >= pattern["m_thresh"]
        if h_triggered and m_triggered:
            risks_found.append(pattern["risk"])

    # Coupled risk level
    risk_count = len(risks_found)
    if risk_count >= 3 or (h_verdict == "LOW_CAPACITY" and m_verdict in ("DEGRADED", "CRITICAL")):
        coupled_risk = "RED"
        recommended_mode = "suspended"
        status = "HOLD"
    elif risk_count >= 1 or (h_verdict == "DEGRADED" and m_verdict != "HEALTHY"):
        coupled_risk = "AMBER"
        recommended_mode = "draft_only"
        status = "CAUTION"
    elif h_verdict == "OPTIMAL" and m_verdict == "HEALTHY":
        coupled_risk = "GREEN"
        recommended_mode = "full"
        status = "PASS"
    else:
        coupled_risk = "AMBER"
        recommended_mode = "normal"
        status = "CAUTION"

    human_confirmation = (
        coupled_risk == "RED" or
        h_verdict in ("DEGRADED", "LOW_CAPACITY") or
        risk_count >= 2
    )

    return _compose_verdict(
        mcp="AFWELL",
        task="coupled_readiness_check",
        status=status,
        domain_verdict=f"Human {h_verdict} | Machine {m_verdict}",
        confidence="HIGH",
        risk_level=coupled_risk,
        recommended_mode=recommended_mode,
        human_required=human_confirmation,
        failure_flags=risks_found if risks_found else None,
        next_safe_action="Step away if RED; Draft if AMBER." if coupled_risk != "GREEN" else "Proceed with Forge."
    )


@mcp.tool()
def well_decision_bandwidth(
    decision_class: str | None = None,
    task_description: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    C-WELL decision bandwidth — combines human + machine state for a specific class.
    Validates against H-WELL readiness + M-WELL health + C-WELL coupled risk.
    Returns APPROVED / CAUTION / BLOCKED with full rationale.

    This is the C-WELL output Arif described:
    {"human_readiness": "FUNCTIONAL", "machine_readiness": "DEGRADED",
     "coupled_risk": "AMBER", "recommended_mode": "draft_only",
     "human_confirmation_required": true, "reason": "..."}
    """
    # Get H-WELL
    h_state = _load_state()
    h_score = h_state.get("well_score", 50)
    h_violations = h_state.get("floors_violated", [])

    # Get M-WELL
    m_state = well_machine_state(ctx=None)
    m_score = m_state.get("m_well_score", 100)
    m_verdict = m_state.get("m_well_verdict", "UNKNOWN")

    # Get C-WELL
    c_state = well_coupled_readiness(ctx=None)
    coupled_risk = c_state.get("coupled_risk", "AMBER")
    c_risks = c_state.get("risks_found", [])

    # Determine human verdict
    if h_score >= 80 and not h_violations:
        h_verdict = "OPTIMAL"
    elif h_score >= 60:
        h_verdict = "FUNCTIONAL"
    elif h_score >= 40:
        h_verdict = "DEGRADED"
    else:
        h_verdict = "LOW_CAPACITY"

    # Per-class thresholds
    class_req = {
        "C0": {"h_min": 0, "m_min": 0},
        "C1": {"h_min": 40, "m_min": 30},
        "C2": {"h_min": 55, "m_min": 50},
        "C3": {"h_min": 65, "m_min": 55},
        "C4": {"h_min": 75, "m_min": 65},
        "C5": {"h_min": 85, "m_min": 75},
    }

    if decision_class is None and task_description:
        d = task_description.lower()
        if any(k in d for k in ["publish", "post", "public", "tweet"]): dc = "C3"
        elif any(k in d for k in ["money", "financial", "legal", "contract"]): dc = "C4"
        elif any(k in d for k in ["irreversible", "delete permanent", "schema migration"]): dc = "C5"
        elif any(k in d for k in ["code", "deploy", "feature", "refactor"]): dc = "C2"
        elif any(k in d for k in ["draft", "outline", "note", "草稿"]): dc = "C1"
        else: dc = "C0"
        decision_class = dc

    reason_parts = []
    verdict = "APPROVED"

    if decision_class:
        req = class_req.get(decision_class, {"h_min": 0, "m_min": 0})
        h_ok = h_score >= req["h_min"]
        m_ok = m_score >= req["m_min"]
        c_ok = coupled_risk in ("GREEN", "AMBER")

        if not h_ok:
            reason_parts.append(f"human score {h_score} < required {req['h_min']}")
        if not m_ok:
            reason_parts.append(f"machine score {m_score} < required {req['m_min']}")
        if not c_ok:
            reason_parts.append(f"coupled risk {coupled_risk} too high")

        if not (h_ok and m_ok and c_ok):
            verdict = "BLOCKED" if (not h_ok or not m_ok) else "CAUTION"
    else:
        reason_parts.append("no decision class specified — general assessment")

    if c_risks and c_risks != ["none"]:
        reason_parts.append(f"coupled risks: {', '.join(c_risks)}")

    if coupled_risk == "RED":
        verdict = "BLOCKED"
        reason_parts.append("coupled risk RED — suspend all consequential actions")
    elif verdict == "APPROVED":
        reason_parts.append(f"human {h_verdict}, machine {m_verdict}, coupled {coupled_risk}")

    return {
        "ok": True,
        "decision_class": decision_class or "general",
        "verdict": verdict,
        "human_readiness": h_verdict,
        "human_score": h_score,
        "machine_readiness": m_verdict,
        "machine_score": m_score,
        "coupled_risk": coupled_risk,
        "recommended_mode": c_state.get("recommended_mode", "normal"),
        "human_confirmation_required": c_state.get("human_confirmation_required", False),
        "reason": "; ".join(reason_parts),
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ── Entry ──────────────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════════
# WELL–FORGE Bridge — Coupling Layer
# A-FORGE asks WELL for bandwidth before execution.
# WELL receives pressure signals during execution.
# WELL never commands or vetoes — it only informs.
# ══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def well_forge_precheck(
    task_description: str | None = None,
    decision_class: str | None = None,
    estimated_duration_minutes: float | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    A-FORGE asks WELL before forging: What is the safe execution mode?

    This is the primary coupling handshake. A-FORGE calls this before any
    forge operation to get bandwidth-adaptive execution parameters.

    WELL does NOT block A-FORGE. It recommends. Arif decides.
    W0: WELL holds a mirror, not a veto.
    """
    h_state = _load_state()
    h_score = h_state.get("well_score", 50)
    h_violations = h_state.get("floors_violated", [])
    metrics = h_state.get("metrics", {})
    cognitive = metrics.get("cognitive", {})
    stress = metrics.get("stress", {})
    sleep = metrics.get("sleep", {})

    fatigue = cognitive.get("decision_fatigue", 0)
    clarity = cognitive.get("clarity", 10)
    stress_load = stress.get("subjective_load", 0)
    sleep_debt = sleep.get("sleep_debt_days", 0)

    # Get M-WELL health
    m_state = well_machine_state(ctx=None)
    m_score = m_state.get("m_well_score", 100)
    m_verdict = m_state.get("m_well_verdict", "UNKNOWN")

    # Forge mode determination
    if h_score >= 80 and m_verdict == "HEALTHY" and not h_violations:
        forge_mode = "full"
        max_task_size = "large"
        recovery_first = False
        h_verdict = "OPTIMAL"
    elif h_score >= 60 and m_verdict in ("HEALTHY", "FUNCTIONAL"):
        forge_mode = "normal"
        max_task_size = "medium"
        recovery_first = False
        h_verdict = "FUNCTIONAL"
    elif h_score >= 40 or (h_score >= 50 and m_verdict == "DEGRADED"):
        forge_mode = "draft_only"
        max_task_size = "small"
        recovery_first = False
        h_verdict = "DEGRADED"
    else:
        forge_mode = "paused"
        max_task_size = "minimal"
        recovery_first = True
        h_verdict = "LOW_CAPACITY"

    # Things to avoid
    avoid = []
    if fatigue > 5: avoid.append("major_refactor")
    if stress_load > 7: avoid.append("public_posting")
    if sleep_debt > 1: avoid.append("deployment")
    if h_score < 50: avoid.append("irreversible_write")
    if fatigue > 7: avoid.append("financial_decision")
    if clarity < 7: avoid.append("complex_architecture")

    # Coupled risk
    c_state = well_coupled_readiness(ctx=None)
    coupled_risk = c_state.get("risk_level", "AMBER")
    c_mode = c_state.get("recommended_mode", "draft_only")

    # FORGE MODE DETERMINATION (Conservative wins)
    # 1. Base readiness
    if h_score >= 80 and m_verdict == "HEALTHY" and not h_violations:
        base_mode = "full"
        max_task_size = "large"
        h_verdict = "OPTIMAL"
    elif h_score >= 60 and m_verdict in ("HEALTHY", "FUNCTIONAL"):
        base_mode = "structured"
        max_task_size = "medium"
        h_verdict = "FUNCTIONAL"
    elif h_score >= 40:
        base_mode = "draft_only"
        max_task_size = "small"
        h_verdict = "DEGRADED"
    else:
        base_mode = "pause"
        max_task_size = "minimal"
        h_verdict = "LOW_CAPACITY"

    # 2. Apply C-WELL override
    mode_priority = {"full": 3, "structured": 2, "draft_only": 1, "pause": 0, "suspended": 0}
    final_mode_val = min(mode_priority.get(base_mode, 0), mode_priority.get(c_mode, 0))
    # Map back to canonical modes
    final_mode = "full" if final_mode_val == 3 else "structured" if final_mode_val == 2 else "draft_only" if final_mode_val == 1 else "pause"

    # Human reconfirmation threshold
    human_confirmation = (
        h_verdict in ("DEGRADED", "LOW_CAPACITY") or
        coupled_risk in ("RED", "AMBER") or
        (decision_class and decision_class >= "C4")
    )

    status = "PASS" if coupled_risk == "GREEN" and final_mode == "full" else "HOLD" if final_mode == "pause" else "CAUTION"

    return _compose_verdict(
        mcp="AFWELL",
        task=f"forge_precheck: {task_description or 'unspecified'}",
        status=status,
        domain_verdict=f"Mode: {final_mode} | Risk: {coupled_risk}",
        confidence="HIGH",
        risk_level=coupled_risk,
        recommended_mode=final_mode,
        human_required=human_confirmation,
        failure_flags=h_violations + c_state.get("failure_flags", []),
        next_safe_action=f"Adopt {final_mode} mode; respect {max_task_size} task ceiling."
    )


@mcp.tool()
def well_forge_pressure_update(
    source: str,  # e.g., "debugging_loop", "token_pressure", "tool_error", "context_overload"
    intensity: float,  # 0-10
    detail: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    A-FORGE reports pressure/cognitive load to WELL during forging.
    Updates decision_fatigue and pressure_ledger.

    Categories:
    - debugging_loop (repeated debugging cycles)
    - token_pressure (context length near limit)
    - tool_error (repeated tool failures)
    - context_overload (too many files/context)
    - complexity_spike (unanticipated complexity)
    - decision_fatigue (too many decisions in a row)
    """
    # Map source to pressure categories
    pressure_source_map = {
        "debugging_loop": "coding/debugging",
        "token_pressure": "work",
        "tool_error": "coding/debugging",
        "context_overload": "work",
        "complexity_spike": "coding/debugging",
        "decision_fatigue": "work",
    }

    # Update decision fatigue
    state = _load_state()
    metrics = state.get("metrics", {})
    cognitive = dict(metrics.get("cognitive", {}))

    old_fatigue = cognitive.get("decision_fatigue", 0)
    # Scale intensity (0-10) to fatigue delta (0-2)
    fatigue_delta = (intensity / 10.0) * 2.0
    new_fatigue = min(10.0, old_fatigue + fatigue_delta)
    cognitive["decision_fatigue"] = round(new_fatigue, 1)
    metrics["cognitive"] = cognitive
    state["metrics"] = metrics

    # Recompute score
    score, violations = _compute_score(metrics)
    state["well_score"] = score
    state["floors_violated"] = violations
    _save_state(state)

    # Log to pressure ledger
    ledger_source = pressure_source_map.get(source, "work")
    _append_event({
        "event": "FORGE_PRESSURE",
        "forge_source": source,
        "ledger_source": ledger_source,
        "intensity": intensity,
        "detail": detail,
        "old_fatigue": old_fatigue,
        "new_fatigue": new_fatigue,
    })

    # Check if W6 Metabolic Pause should trigger
    w6_triggered = False
    if fatigue_delta > 1.5 and new_fatigue > 6.0:
        if "W6_METABOLIC_PAUSE" not in violations:
            violations.append("W6_METABOLIC_PAUSE")
            state["floors_violated"] = violations
            _save_state(state)
            w6_triggered = True

    return {
        "ok": True,
        "logged": {"source": source, "intensity": intensity},
        "fatigue_delta": round(fatigue_delta, 2),
        "new_fatigue": new_fatigue,
        "well_score": score,
        "w6_triggered": w6_triggered,
        "w0": "WELL recommends. arifOS governs. Arif decides. — DITEMPA BUKAN DIBERI",
    }


@mcp.tool()
def well_forge_mode_recommend(ctx: Context | None = None) -> dict[str, Any]:
    """
    Returns current forge mode recommendation for A-FORGE.
    Based on H-WELL + M-WELL + C-WELL state.

    Output mirrors the WELL–A-FORGE coupling contract:
    {"readiness": "DEGRADED", "forge_mode": "draft_only",
     "max_task_size": "small", "avoid": [...], "recovery_first": true}
    """
    h_state = _load_state()
    h_score = h_state.get("well_score", 50)
    h_violations = h_state.get("floors_violated", [])
    metrics = h_state.get("metrics", {})
    cognitive = metrics.get("cognitive", {})

    fatigue = cognitive.get("decision_fatigue", 0)
    clarity = cognitive.get("clarity", 10)
    stress_load = metrics.get("stress", {}).get("subjective_load", 0)

    m_state = well_machine_state(ctx=None)
    m_score = m_state.get("m_well_score", 100)
    m_verdict = m_state.get("m_well_verdict", "UNKNOWN")

    c_state = well_coupled_readiness(ctx=None)
    coupled_risk = c_state.get("coupled_risk", "AMBER")

    if h_score >= 80 and m_verdict == "HEALTHY":
        forge_mode = "full"
        max_task_size = "large"
        readiness = "OPTIMAL"
        recovery_first = False
    elif h_score >= 60:
        forge_mode = "normal"
        max_task_size = "medium"
        readiness = "FUNCTIONAL"
        recovery_first = False
    elif h_score >= 40:
        forge_mode = "draft_only"
        max_task_size = "small"
        readiness = "DEGRADED"
        recovery_first = False
    else:
        forge_mode = "paused"
        max_task_size = "minimal"
        readiness = "LOW_CAPACITY"
        recovery_first = True

    avoid = []
    if fatigue > 5: avoid.append("major_refactor")
    if stress_load > 7: avoid.append("public_commitment")
    if h_score < 50: avoid.append("deployment")
    if clarity < 7: avoid.append("complex_architecture")
    if coupled_risk == "RED": avoid.append("all_consequential_actions")

    return {
        "ok": True,
        "readiness": readiness,
        "forge_mode": forge_mode,
        "max_task_size": max_task_size,
        "avoid": avoid if avoid else ["none"],
        "recovery_first": recovery_first,
        "coupled_risk": coupled_risk,
        "human_score": h_score,
        "machine_score": m_score,
        "w0": "WELL recommends. arifOS governs. Arif decides. — DITEMPA BUKAN DIBERI",
    }


@mcp.tool()
def well_forge_closeout(
    task_description: str,
    outcome: str,  # "success" | "partial" | "failed" | "paused"
    errors_encountered: int = 0,
    decisions_remaining: int = 0,
    human_confirmation_required: bool = False,
    fatigue_spent: float | None = None,  # explicit fatigue cost if known
    note: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    A-FORGE sends closure data after forge operation.
    WELL updates fatigue/load state based on work done.

    This is the third leg of the WELL–A-FORGE coupling:
    1. precheck (before forging)
    2. pressure_update (during forging)
    3. closeout (after forging)
    """
    state = _load_state()
    metrics = state.get("metrics", {})
    cognitive = dict(metrics.get("cognitive", {}))

    old_fatigue = cognitive.get("decision_fatigue", 0)

    # Compute fatigue cost
    if fatigue_spent is not None:
        new_fatigue = max(0, old_fatigue - fatigue_spent)
    else:
        # Estimate from outcome and errors
        if outcome == "success":
            cost = 0.5
        elif outcome == "partial":
            cost = 1.0
        elif outcome == "failed":
            cost = 1.5
        else:  # paused
            cost = 0.3
        cost += errors_encountered * 0.3
        new_fatigue = max(0, old_fatigue - cost)

    cognitive["decision_fatigue"] = round(new_fatigue, 1)
    metrics["cognitive"] = cognitive
    state["metrics"] = metrics

    # Recompute
    score, violations = _compute_score(metrics)
    state["well_score"] = score
    state["floors_violated"] = violations
    _save_state(state)

    _append_event({
        "event": "FORGE_CLOSEOUT",
        "task": task_description,
        "outcome": outcome,
        "errors": errors_encountered,
        "decisions_remaining": decisions_remaining,
        "human_confirmation_required": human_confirmation_required,
        "fatigue_delta": round(new_fatigue - old_fatigue, 2),
        "new_fatigue": new_fatigue,
        "note": note,
    })

    return {
        "ok": True,
        "outcome_recorded": outcome,
        "fatigue_delta": round(new_fatigue - old_fatigue, 2),
        "new_fatigue": new_fatigue,
        "well_score": score,
        "decisions_remaining": decisions_remaining,
        "human_confirmation_required": human_confirmation_required,
        "w0": "WELL recommends. arifOS governs. Arif decides. — DITEMPA BUKAN DIBERI",
    }


# ── Entry ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    mcp.run(transport="http")


