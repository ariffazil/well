"""
APEX Envelope for WELL — Vitality organ

Maps biological/cognitive signals to 10 APEX gates:
  Amanah: honesty about operator state (no false "I'm fine")
  Presence: real-time vs historical biometrics
  Humility: uncertainty in sensor readings
  Signal: HRV, sleep, movement signal quality
  Understanding: behavioral coherence (patterns vs anomalies)
  Energy: metabolic load
  Authority: actor verification (operator_id)
  Reversibility: READ (WELL is reflect-only)
  Proof: ZKPC_OBSERVATION
  Sovereign: passthrough

DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

from typing import Any

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, '/root/arifOS')
from arifosmcp.schemas.arifos_response import ArifOSResponse, ActionClass, ensure_arifos_response

try:
    from server import _load_state, _state_score
except ImportError:
    _load_state = lambda: {}
    _state_score = lambda s: 50


def well_apex_envelope(
    *,
    tool_name: str = "unknown",
    state: dict[str, Any] | None = None,
    actor_id: str | None = None,
) -> dict[str, Any]:
    """Build APEX envelope from WELL-specific signals."""
    st = state or _load_state()
    score = _state_score(st)

    # Amanah: honesty about operator state
    truth_status = st.get("truth_status", "UNVERIFIED")
    amanah = 1.0 if truth_status == "VERIFIED" else (0.7 if truth_status == "CACHED" else 0.4)

    # Presence: real-time vs historical
    boundary = "LIVE" if truth_status == "VERIFIED" else "CACHED"

    # Humility: uncertainty in sensor readings
    humility = 0.8  # Sensors are inherently uncertain

    # Signal: HRV, sleep quality
    metrics = st.get("metrics", {})
    has_hrv = "hrv" in metrics or "hrv_proxy" in metrics
    has_sleep = "sleep_hours" in metrics
    signal_score = 0.3
    if has_hrv: signal_score += 0.3
    if has_sleep: signal_score += 0.2
    if score > 0: signal_score += 0.2
    signal_score = min(1.0, signal_score)

    # Understanding: behavioral coherence
    floors_violated = st.get("floors_violated", [])
    coherent = len(floors_violated) == 0

    # Energy: metabolic load (inverted — lower load = higher score)
    safe_mode = st.get("safe_mode", False)
    energy = 0.5 if safe_mode else 0.8

    # Compute G
    import math
    A = (amanah * humility * (0.9 if coherent else 0.4)) ** (1/3)
    P = 1.0 if boundary == "LIVE" else 0.7
    H = 1.0  # authority passthrough
    S = signal_score
    U = (1.0 * (0.9 if coherent else 0.4)) ** 0.5
    E = energy
    G = round(A * P * H * math.sqrt(S * U) * E ** 2, 4)

    if G >= 0.80:
        verdict = "SEAL"
    elif G >= 0.50:
        verdict = "SABAR"
    else:
        verdict = "HOLD"

    return {
        "equation": "g(t)=A(t)\u00b7P(t)\u00b7H(t)\u00b7\u221a(S(t)\u00b7U(t))\u00b7E(t)\u00b2",
        "gates": {
            "amanah": {"pass": True, "score": round(amanah, 4), "detail": f"truth_status={truth_status}"},
            "presence": {"pass": True, "score": round(P, 4), "detail": boundary, "boundary": boundary},
            "humility": {"pass": True, "score": round(humility, 4), "detail": "sensor uncertainty declared"},
            "signal": {"pass": signal_score >= 0.3, "score": round(signal_score, 4), "detail": f"hrv={has_hrv}, sleep={has_sleep}"},
            "understanding": {"pass": coherent, "score": round(0.9 if coherent else 0.4, 4), "detail": "coherent" if coherent else f"floors_violated={floors_violated}"},
            "energy": {"pass": True, "score": round(energy, 4), "detail": f"safe_mode={safe_mode}"},
            "authority": {"pass": bool(actor_id), "score": 1.0 if actor_id else 0.0, "detail": f"actor={actor_id}", "actor_id": actor_id},
            "reversibility": {"pass": True, "score": 1.0, "detail": "READ action_class", "action_class": ActionClass.OBSERVE},
            "proof": {"pass": True, "score": 0.85, "detail": "ZKPC_OBSERVATION", "proof_level": "ZKPC_OBSERVATION"},
            "sovereign": {"pass": True, "score": 1.0, "detail": "no F13 halt"},
        },
        "dials": {"A": round(A, 4), "P": round(P, 4), "H": round(H, 4), "S": round(S, 4), "U": round(U, 4), "E": round(E, 4)},
        "G": G,
        "verdict": verdict,
        "weakest_gate": min(
            ["amanah", "presence", "humility", "signal", "understanding", "energy", "authority", "reversibility", "proof", "sovereign"],
            key=lambda k: {"amanah": amanah, "presence": P, "humility": humility, "signal": signal_score,
                          "understanding": 0.9 if coherent else 0.4, "energy": energy, "authority": 1.0 if actor_id else 0.0,
                          "reversibility": 1.0, "proof": 0.85, "sovereign": 1.0}[k]
        ),
        "spec": "APEX-MCP-001",
        "version": "v2026.06.20",
    }
