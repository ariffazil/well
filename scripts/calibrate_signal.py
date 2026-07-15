#!/usr/bin/env python3
"""
calibrate_signal.py — WELL S15-S18 calibration case collector.

Each calibration case is a structured self-report for one organizational signal.
3 cases per signal required for DRAFT→ACTIVE promotion.

Usage:
    python calibrate_signal.py S15    # Collect one calibration case for S15
    python calibrate_signal.py all    # Collect for all DRAFT signals
    python calibrate_signal.py status # Show current calibration counts

DITEMPA BUKAN DIBERI — Signals are calibrated, not assumed.
"""

import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# Signal definitions with prompts
SIGNALS = {
    "S15": {
        "name": "feedback_loop_health",
        "parameters": [
            "feedback_receipt_quality",
            "feedback_upward_flow",
            "feedback_loop_latency",
            "feedback_safety",
        ],
        "primary_prompt": "When was the last time you received meaningful feedback on your work? (1=never, 10=today/yesterday)",
        "companion": [
            "When you raise a concern upward, does it get addressed? (1=ignored, 5=sometimes, 10=always)",
            "Do you feel safe giving honest upward feedback? (yes/no/partial)",
        ],
    },
    "S16": {
        "name": "mentoring_knowledge_transfer",
        "parameters": [
            "mentoring_received",
            "mentoring_provided",
            "knowledge_transfer_rate",
            "isolation_risk",
        ],
        "primary_prompt": "Do you have someone whose experience you can draw on for guidance? (1=no one, 10=active mentor)",
        "companion": [
            "Are you actively developing others? (1=no, 10=structured mentoring)",
            "Has a key mentor or protege left in the last 90 days? (yes/no)",
        ],
    },
    "S17": {
        "name": "meeting_to_decision_ratio",
        "parameters": [
            "meetings_per_week",
            "decisions_per_week",
            "decision_latency",
            "meeting_satisfaction",
            "ratio_signal",
        ],
        "primary_prompt": "How many meetings this week had a clear decision outcome?",
        "companion": [
            "How many meetings were information-sharing only (no decision)?",
            "Of decisions needed this week, how many were actually made?",
        ],
    },
    "S18": {
        "name": "exit_narratives",
        "parameters": [
            "recent_departures_count",
            "exit_quality",
            "capability_loss",
            "succession_quality",
            "exit_narrative_contagion",
            "institutional_memory_loss",
        ],
        "primary_prompt": "How would you characterize the last departure in your team? (regenerative/neutral/corrosive)",
        "companion": [
            "Did the departing person's knowledge transfer before leaving? (fully/partially/not at all)",
            "Are you aware of others planning to leave? (yes/no)",
        ],
    },
}

DATA_DIR = Path(__file__).parent.parent / "data" / "calibration"


def count_cases(signal_id: str) -> int:
    """Count existing calibration cases for a signal."""
    signal_dir = DATA_DIR / signal_id
    if not signal_dir.exists():
        return 0
    return len(list(signal_dir.glob("case_*.json")))


def collect_case(signal_id: str) -> dict:
    """Prompt the operator and record one calibration case."""
    signal = SIGNALS.get(signal_id)
    if not signal:
        print(f"Unknown signal: {signal_id}. Valid: {list(SIGNALS.keys())}")
        sys.exit(1)

    case = {
        "signal_id": signal_id,
        "signal_name": signal["name"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "values": {},
        "companion_answers": [],
    }

    print(f"\n{'=' * 60}")
    print(f"📊 Calibration Case for {signal_id} — {signal['name']}")
    print(f"{'=' * 60}")
    print(f"Case #{count_cases(signal_id) + 1} of 3 needed for ACTIVE promotion\n")

    # Primary prompt
    print(f"Q: {signal['primary_prompt']}")
    try:
        raw = input("> ").strip()
        case["values"]["primary"] = raw
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(1)

    # Companion questions
    for q in signal["companion"]:
        print(f"\nQ: {q}")
        try:
            raw = input("> ").strip()
            case["companion_answers"].append(raw)
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            sys.exit(1)

    # Store
    signal_dir = DATA_DIR / signal_id
    signal_dir.mkdir(parents=True, exist_ok=True)
    case_num = count_cases(signal_id) + 1
    case_path = signal_dir / f"case_{case_num}.json"
    case_path.write_text(json.dumps(case, indent=2))
    print(f"\n✅ Case #{case_num} saved to {case_path}")
    return case


def show_status():
    """Show calibration progress for all signals."""
    print(f"\n{'=' * 60}")
    print("📊 WELL S15-S18 Calibration Status")
    print(f"{'=' * 60}")
    for sid in sorted(SIGNALS.keys()):
        sig = SIGNALS[sid]
        count = count_cases(sid)
        status = "✅ ACTIVE" if count >= 3 else f"⏳ {count}/3"
        bar = "▓" * count + "░" * (3 - count)
        print(f"  {sid} {sig['name']:35s} [{bar}] {status}")
    total = sum(count_cases(sid) for sid in SIGNALS)
    needed = len(SIGNALS) * 3
    print(f"\n  Total: {total}/{needed} cases collected")
    if total >= needed:
        print("  ✅ Ready to promote all signals to ACTIVE")
    print()


def promote_all():
    """Promote all signals from DRAFT to ACTIVE if 3+ cases each."""
    all_ready = all(count_cases(sid) >= 3 for sid in SIGNALS)
    if not all_ready:
        print("❌ Not all signals have 3 calibration cases yet.")
        show_status()
        sys.exit(1)

    # Update the organizational_signals.py file
    signals_path = (
        Path(__file__).parent.parent
        / "well_mcp"
        / "resources"
        / "organizational_signals.py"
    )
    if not signals_path.exists():
        print(f"❌ Signals file not found: {signals_path}")
        sys.exit(1)

    content = signals_path.read_text()
    for sid in SIGNALS:
        old_status = f'"{sid}"'  # We'll find the status line
        # Replace DRAFT status with ACTIVE
        for sig_name in [SIGNALS[sid]["name"]]:
            old = f'status": "DRAFT — needs 3 calibration cases before promotion'
            new = f'status": "ACTIVE — promoted after 3 calibration cases'
            if old in content:
                content = content.replace(old, new)
                print(f"  ✅ {sid} promoted to ACTIVE")
            else:
                print(
                    f"  ⚠️  {sid}: DRAFT status marker not found (may already be ACTIVE)"
                )

    signals_path.write_text(content)
    print(f"\n✅ All signals promoted. File updated: {signals_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: calibrate_signal.py <S15|S16|S17|S18|all|status|promote>")
        sys.exit(1)

    cmd = sys.argv[1].upper()
    if cmd == "STATUS":
        show_status()
    elif cmd == "PROMOTE":
        promote_all()
    elif cmd == "ALL":
        for sid in SIGNALS:
            collect_case(sid)
        show_status()
    elif cmd in SIGNALS:
        collect_case(cmd)
        show_status()
    else:
        print(f"Unknown: {cmd}. Valid: {list(SIGNALS.keys())} + all|status|promote")
        sys.exit(1)
