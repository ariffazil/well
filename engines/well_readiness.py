#!/usr/bin/env python3
"""
well_readiness — single verdict, single tool.

Reads state.json. Returns:
  - color: GREEN | YELLOW | RED | STALE
  - score: 0-100
  - ttl_hours: hours since last data
  - reason: one line
  - action: PROCEED | SIMPLIFY | HOLD | INJECT_NEEDED

TTL rules:
  < 12h  = GREEN (if score OK)
  12-24h = YELLOW
  24-48h = RED
  > 48h  = STALE → INJECT_NEEDED

This is a sensor, not a judge. Sensors auto-sample.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"

TTL_FRESH = 12    # hours — GREEN
TTL_WARN = 24     # hours — YELLOW
TTL_STALE = 48    # hours — RED/STALE


def load_state() -> dict:
    """Load state.json, return empty dict on failure."""
    try:
        return json.loads(STATE_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def compute_ttl_hours(state: dict) -> float:
    """Hours since last_successful_read or injection_ts."""
    ts_str = state.get("last_successful_read") or state.get("signals_meta", {}).get("injection_ts")
    if not ts_str:
        return 999.0  # never fed
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return max(0, (now - ts).total_seconds() / 3600)
    except (ValueError, TypeError):
        return 999.0


def classify(score: float, ttl_hours: float) -> tuple[str, str]:
    """Return (color, action) from score and TTL."""
    if ttl_hours > TTL_STALE:
        return "STALE", "INJECT_NEEDED"
    if ttl_hours > TTL_WARN:
        return "RED", "HOLD"
    if ttl_hours > TTL_FRESH:
        return "YELLOW", "SIMPLIFY"

    # Fresh — use score
    if score >= 75:
        return "GREEN", "PROCEED"
    if score >= 50:
        return "YELLOW", "SIMPLIFY"
    return "RED", "HOLD"


def readiness() -> dict:
    """Single verdict from state.json."""
    state = load_state()
    if not state:
        return {
            "color": "STALE",
            "score": 0,
            "ttl_hours": 999,
            "reason": "No state.json found",
            "action": "INJECT_NEEDED",
        }

    score = state.get("well_score", 0)
    ttl_hours = compute_ttl_hours(state)
    color, action = classify(score, ttl_hours)

    reason_parts = []
    if color == "STALE":
        reason_parts.append(f"No data for {ttl_hours:.0f}h")
    elif color == "RED":
        reason_parts.append(f"Data is {ttl_hours:.0f}h old")
    elif color == "YELLOW":
        reason_parts.append(f"Data aging ({ttl_hours:.0f}h)")
    else:
        reason_parts.append(f"Fresh ({ttl_hours:.1f}h)")

    if score < 50:
        reason_parts.append(f"low score ({score:.0f})")
    elif score < 75:
        reason_parts.append(f"moderate score ({score:.0f})")

    # Extract key biometric signals
    bio = state.get("biometric", {})
    signals = state.get("signals", {})
    sleep = signals.get("s05_sleep_architecture", {})

    return {
        "color": color,
        "score": round(score, 1),
        "ttl_hours": round(ttl_hours, 1),
        "reason": " | ".join(reason_parts),
        "action": action,
        "biometric": {
            "peace2": bio.get("peace2"),
            "delta_s": bio.get("delta_s"),
            "kappa_r": bio.get("kappa_r"),
            "rasa": bio.get("rasa"),
            "clarity": state.get("metrics", {}).get("cognitive", {}).get("clarity"),
            "sleep_hours": sleep.get("hours"),
        },
        "freshness": state.get("freshness", "UNKNOWN"),
        "confidence": state.get("confidence", "UNKNOWN"),
    }


if __name__ == "__main__":
    result = readiness()
    print(json.dumps(result, indent=2))
    # Exit code: 0=GREEN, 1=YELLOW, 2=RED/STALE
    if result["color"] == "GREEN":
        sys.exit(0)
    elif result["color"] == "YELLOW":
        sys.exit(1)
    else:
        sys.exit(2)
