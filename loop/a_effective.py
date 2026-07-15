"""A_effective = A_granted × E × R × G × S — authority collapses with weak evidence."""

from __future__ import annotations

from typing import Any

# Rank map for granted action class → numeric authority (0–1)
CLASS_A = {
    "OBSERVE": 0.2,
    "SUGGEST": 0.35,
    "SIMULATE": 0.45,
    "DRAFT": 0.5,
    "QUEUE": 0.55,
    "EXECUTE_REVERSIBLE": 0.75,
    "EXECUTE_HIGH_IMPACT": 0.9,
    "IRREVERSIBLE": 1.0,
    "GREEN": 0.75,
    "YELLOW": 0.55,
    "ORANGE": 0.45,
    "RED": 0.2,
    "BLACK": 0.0,
}

# Output bands from effective score (calibrated for A≈0.75 healthy path)
BAND_THRESHOLDS = (
    (0.55, "GREEN"),
    (0.40, "YELLOW"),
    (0.28, "ORANGE"),
    (0.12, "RED"),
    (0.0, "BLACK"),
)


def compute_a_effective(
    envelope: dict[str, Any],
    a_granted: str = "EXECUTE_REVERSIBLE",
    human_required: bool = False,
    scope: str = "global",
) -> dict[str, Any]:
    """
    Shrink delegated authority by evidence quality, reversibility,
    governance integrity, and substrate fitness.

    scope:
      global — full substrate fitness (default)
      service_local — allowlisted single-service recovery; one dead worker
        must not require global peace, but COMPROMISED gov still blocks.
    """
    A = CLASS_A.get(str(a_granted).upper(), 0.2)

    E = float(envelope.get("evidence_quality") or 0.0)
    # Freshness penalty if machine unknown
    if (envelope.get("machine") or {}).get("state") == "UNKNOWN":
        E = min(E, 0.2)

    exec_meta = envelope.get("execution") or {}
    R = 1.0 if exec_meta.get("rollback_available", True) else 0.15
    if str(exec_meta.get("blast_radius", "LOW")).upper() in ("HIGH", "CRITICAL"):
        R *= 0.4

    gov = envelope.get("governance") or {}
    g_state = str(gov.get("state", "UNKNOWN")).upper()
    if g_state in ("COMPROMISED", "HOLD"):
        G = 0.1
    elif g_state == "DRIFTING":
        # Drift is governance debt, not a hard block for one allowlisted bounce
        G = 0.88 if scope == "service_local" else 0.55
    elif g_state == "UNCERTAIN":
        G = 0.7
    elif g_state == "COHERENT":
        G = 0.95
    else:
        G = 0.4

    # Substrate fitness S from gate / coupling / ranks
    gate = envelope.get("gate") or {}
    verdict = str(gate.get("verdict", "INSUFFICIENT_DATA")).upper()
    s_map = {
        "PROCEED": 1.0,
        "REDUCE_LOAD": 0.7,
        "RECOVER": 0.45,
        "HOLD": 0.15,
        "INSUFFICIENT_DATA": 0.35,
    }
    S = s_map.get(verdict, 0.35)

    human = envelope.get("human") or {}
    if human_required and human.get("source") == "UNKNOWN":
        S = min(S, 0.2)
        E = min(E, 0.3)

    # Coupling high risk collapses S (global only)
    coup = str((envelope.get("coupling") or {}).get("state", "")).upper()
    if coup == "HIGH_RISK" and scope != "service_local":
        S = min(S, 0.3)

    # Service-local: one allowlisted unit recovery — fitness from service probe + R
    if scope == "service_local":
        svc = (envelope.get("machine") or {}).get("service") or {}
        if svc:
            S = 0.95 if str(exec_meta.get("blast_radius", "LOW")).upper() == "LOW" else 0.5
            E = max(E, 0.9)
        if g_state in ("COMPROMISED", "HOLD"):
            S = min(S, 0.1)  # still hard-block

    score = A * E * R * G * S
    band = "BLACK"
    thr_table = BAND_THRESHOLDS
    if scope == "service_local":
        # Slightly lower GREEN entry for narrow allowlisted bounce
        thr_table = (
            (0.50, "GREEN"),
            (0.38, "YELLOW"),
            (0.28, "ORANGE"),
            (0.12, "RED"),
            (0.0, "BLACK"),
        )
    for thr, name in thr_table:
        if score >= thr:
            band = name
            break

    # Hard floors
    if score < 0.05:
        band = "BLACK"
    if verdict == "HOLD" and scope != "service_local":
        band = "RED" if band not in ("BLACK",) else band
    if g_state in ("COMPROMISED", "HOLD"):
        band = "RED" if band != "BLACK" else "BLACK"

    max_class = {
        "GREEN": "EXECUTE_REVERSIBLE",
        "YELLOW": "QUEUE",
        "ORANGE": "SIMULATE",
        "RED": "OBSERVE",
        "BLACK": "OBSERVE",
    }[band]

    mut_floor = 0.50 if scope == "service_local" else 0.55
    return {
        "a_granted": a_granted,
        "A": round(A, 3),
        "E": round(E, 3),
        "R": round(R, 3),
        "G": round(G, 3),
        "S": round(S, 3),
        "score": round(score, 4),
        "effective_band": band,
        "max_action_class": max_class,
        "scope": scope,
        "mutation_allowed": band == "GREEN"
        and max_class == "EXECUTE_REVERSIBLE"
        and score >= mut_floor,
        "formula": "A_effective = A × E × R × G × S",
        "note": "Capability alone never grants authority.",
    }
