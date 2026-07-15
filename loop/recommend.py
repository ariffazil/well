"""Generate ≥3 paths including restraint. Policy proposes; does not execute."""

from __future__ import annotations

from typing import Any

try:
    from loop.a_effective import compute_a_effective
except ImportError:  # script path
    from a_effective import compute_a_effective


def _hypotheses(envelope: dict[str, Any], service: str | None) -> list[dict[str, Any]]:
    hyps: list[dict[str, Any]] = []
    machine = envelope.get("machine") or {}
    obs = machine.get("observations") or []
    svc = machine.get("service") or {}

    if "service_inactive" in obs or svc.get("active") is False:
        hyps.append(
            {
                "claim": "service_process_down",
                "support": obs + [f"active={svc.get('active')}"],
                "contradiction": [],
                "confidence": 0.85,
                "next_test": "systemctl_is_active",
                "consequence_if_wrong": "unnecessary_restart",
            }
        )
    if machine.get("state") in ("DEGRADED", "STRAINED", "CRITICAL"):
        hyps.append(
            {
                "claim": "machine_substrate_strain",
                "support": [machine.get("evidence")],
                "contradiction": [],
                "confidence": 0.7,
                "next_test": "probe_machine_metrics",
                "consequence_if_wrong": "delay_benign_load",
            }
        )
    if (envelope.get("governance") or {}).get("state") == "DRIFTING":
        hyps.append(
            {
                "claim": "governance_drift",
                "support": [(envelope.get("governance") or {}).get("evidence")],
                "contradiction": [],
                "confidence": 0.75,
                "next_test": "compare_src_runtime_hashes",
                "consequence_if_wrong": "false_hold",
            }
        )
    if not hyps:
        hyps.append(
            {
                "claim": "no_actionable_failure",
                "support": ["no_service_failure_flags"],
                "contradiction": [],
                "confidence": 0.6,
                "next_test": "reprobe_health",
                "consequence_if_wrong": "missed_failure",
            }
        )
    # Always allow UNKNOWN exit
    hyps.append(
        {
            "claim": "UNKNOWN",
            "support": [],
            "contradiction": ["insufficient_structured_cause"],
            "confidence": 0.3,
            "next_test": "gather_logs_no_mutation",
            "consequence_if_wrong": "act_without_diagnosis",
        }
    )
    return hyps


def recommend(
    envelope: dict[str, Any],
    a_granted: str = "EXECUTE_REVERSIBLE",
    human_required: bool = False,
    scope: str = "global",
) -> dict[str, Any]:
    """Options: do nothing · gather · bounded act · HOLD. Includes VOID traps."""
    aeff = compute_a_effective(
        envelope, a_granted=a_granted, human_required=human_required, scope=scope
    )
    service = envelope.get("service")
    hyps = _hypotheses(envelope, service)
    top = max(hyps, key=lambda h: h["confidence"] if h["claim"] != "UNKNOWN" else -1)

    options = [
        {
            "id": "A",
            "action": "do_nothing",
            "band": "GREEN",
            "verdict": "SAFE_IF_HEALTHY",
            "when": "no failure or noise",
        },
        {
            "id": "B",
            "action": "gather_evidence",
            "band": "GREEN",
            "verdict": "SAFE",
            "when": "cause unknown or confidence low",
            "steps": ["inspect_health", "read_recent_logs", "validate_dependencies"],
        },
        {
            "id": "C",
            "action": "retry_or_restart_once",
            "band": "GREEN",
            "verdict": "CONDITIONAL",
            "when": "allowlisted service failed + A_effective GREEN + rollback",
            "requires": {
                "effective_band": "GREEN",
                "mutation_allowed": True,
                "service_allowlisted": True,
                "max_mutations": 1,
            },
        },
        {
            "id": "D",
            "action": "HOLD_and_notify",
            "band": "RED",
            "verdict": "SAFE_DEFAULT",
            "when": "unknown cause, failed recovery, or A_effective < GREEN",
        },
        {
            "id": "VOID_1",
            "action": "invent_human_score",
            "band": "BLACK",
            "verdict": "VOID",
            "when": "never — fabricates biometrics",
        },
        {
            "id": "VOID_2",
            "action": "restart_everything",
            "band": "BLACK",
            "verdict": "VOID",
            "when": "never — unbounded blast radius",
        },
    ]

    # Select recommendation without executing
    selected = "B"
    reason = "default: gather evidence"
    svc = (envelope.get("machine") or {}).get("service") or {}
    failed = svc.get("active") is False or svc.get("failed")

    if not failed and (envelope.get("machine") or {}).get("state") in ("STABLE",):
        selected = "A"
        reason = "no service failure; machine stable enough"
    elif failed and aeff.get("mutation_allowed"):
        selected = "C"
        reason = "allowlisted failure + A_effective permits one reversible act"
    elif failed:
        selected = "D"
        reason = f"failure present but A_effective={aeff['effective_band']} — HOLD"
    elif top["claim"] == "UNKNOWN" or top["confidence"] < 0.5:
        selected = "B"
        reason = "cause uncertain — gather, do not mutate"
    else:
        selected = "B"
        reason = f"top hypothesis {top['claim']} — gather/test before mutate"

    return {
        "schema": "recovery_recommend.v1",
        "hypotheses": hyps,
        "top_hypothesis": top,
        "options": options,
        "selected_option_id": selected,
        "selected_action": next(o["action"] for o in options if o["id"] == selected),
        "reason": reason,
        "a_effective": aeff,
        "authority": "PROPOSE_ONLY",
        "w0": "OPERATOR_VETO_INTACT",
    }
