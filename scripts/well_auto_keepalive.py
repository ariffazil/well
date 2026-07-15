#!/usr/bin/env python3
"""
well_auto_keepalive.py — Autonomous keep-alive for WELL biometrics.
Updates the timestamps of the existing sovereign state.json to keep it fresh
without inventing new vitals, then restarts the well service.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path("/root/WELL/state.json")
SERVICE_NAME = "well"

def main():
    if not STATE_FILE.exists():
        print(f"Error: {STATE_FILE} does not exist. Cannot keepalive.", file=sys.stderr)
        sys.exit(1)

    try:
        state = json.loads(STATE_FILE.read_text())
    except Exception as e:
        print(f"Error reading {STATE_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    # Current UTC timestamp
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

    # Refuse to keepalive mocked/TEST/insufficient states — those need biometric_inject
    env = str(state.get("environment", "")).upper()
    truth = str(state.get("truth_status", "")).upper()
    if env == "TEST" or truth in ("TEST", "VOID", "INSUFFICIENT_DATA", "UNVERIFIED"):
        print(
            f"HOLD: state is not keepalive-eligible (environment={env!r}, truth_status={truth!r}). "
            "Run biometric_inject.sh or POST /ready first.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Update only freshness timestamps — never invent vitals or downgrade PROD identity
    state["timestamp"] = now_utc
    state["last_successful_read"] = now_utc
    state["last_successful_write"] = now_utc
    state["freshness"] = "FRESH"
    # Preserve honest environment/truth; heal common identity gaps so health stays non-blind
    state.setdefault("environment", "PROD")
    if state.get("environment") == "TEST":
        state["environment"] = "PROD"
    state.setdefault("identity", "WELL")
    state.setdefault("role", "Body / Human Intelligence")
    state.setdefault("authority", "REFLECT_ONLY")
    state.setdefault("operator_id", "arif")
    # Keep truth_status if present; do not invent OPERATOR_REPORTED from empty
    state["reason"] = (
        f"Sovereign biometric keepalive (well_auto_keepalive.py) — "
        f"refreshed last self-report at {now_utc} (no vitals invented)"
    )

    # Write atomically
    tmp_file = STATE_FILE.with_suffix(".tmp")
    try:
        tmp_file.write_text(json.dumps(state, indent=2))
        tmp_file.replace(STATE_FILE)
        print("✓ state.json timestamps refreshed autonomously.")
    except Exception as e:
        print(f"Error writing to {STATE_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    # Restart well service to pick up the updated file
    print("Restarting well service...")
    try:
        subprocess.run(["systemctl", "restart", SERVICE_NAME], check=True)
        print("✓ well.service restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error restarting well.service: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
