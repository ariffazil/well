"""Closed loop: Sense → Interpret → Propose → Judge(A_eff) → Act≤1 → Verify → Learn.

Mutations only on catalogue allowlist. Dry-run default unless mutate=True.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WELL_DIR = Path(__file__).resolve().parent.parent
if str(WELL_DIR) not in sys.path:
    sys.path.insert(0, str(WELL_DIR))

from loop.a_effective import compute_a_effective  # noqa: E402
from loop.recommend import recommend  # noqa: E402
from loop.state_envelope import build_state_envelope  # noqa: E402
RECEIPT_DIR = WELL_DIR / "loop" / "receipts"
CATALOGUE = Path(__file__).resolve().parent / "catalogues" / "autonomic_recovery_v1.yaml"

# Hard allowlist — never trust YAML alone for mutation targets
HARD_ALLOWLIST = frozenset({"well-heartbeat.service"})


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(cmd: list[str], timeout: int = 15) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or r.stderr or "").strip()
    except Exception as e:
        return 1, str(e)


def probe_service(unit: str) -> dict[str, Any]:
    code, out = _run(["systemctl", "is-active", unit])
    active = code == 0 and out.strip() == "active"
    code2, state = _run(
        ["systemctl", "show", unit, "-p", "ActiveState", "-p", "SubState", "--value"]
    )
    lines = state.splitlines() if state else []
    return {
        "unit": unit,
        "active": active,
        "is_active": out.strip() if out else "unknown",
        "active_state": lines[0] if lines else "unknown",
        "sub_state": lines[1] if len(lines) > 1 else "unknown",
        "failed": (lines[0] if lines else "") == "failed",
        "probed_at": _now(),
    }


def _load_catalogue() -> dict[str, Any]:
    # Minimal YAML subset without PyYAML dependency
    text = CATALOGUE.read_text() if CATALOGUE.exists() else ""
    services = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("- ") and s.endswith(".service"):
            services.append(s[2:].strip())
    return {
        "agent": "autonomic_recovery_v1",
        "services": services or list(HARD_ALLOWLIST),
        "max_mutations": 1,
        "lease_minutes": 10,
    }


def _write_receipt(receipt: dict[str, Any]) -> Path:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RECEIPT_DIR / f"recovery_{ts}.json"
    path.write_text(json.dumps(receipt, indent=2, default=str))
    # Append JSONL ledger
    ledger = RECEIPT_DIR / "recovery_ledger.jsonl"
    with ledger.open("a") as f:
        f.write(json.dumps(receipt, default=str) + "\n")
    return path


def run_recovery_loop(
    service: str = "well-heartbeat.service",
    mutate: bool = False,
    force_failed_probe: bool = False,
    a_granted: str = "EXECUTE_REVERSIBLE",
) -> dict[str, Any]:
    """
    Full closed loop for one allowlisted service.

    mutate=False → observe/recommend only (Gate 0–1).
    mutate=True  → at most one restart if A_effective allows (Gate 3).
    force_failed_probe → fault-injection: treat service as failed for diagnosis path.
    """
    cat = _load_catalogue()
    if service not in HARD_ALLOWLIST or service not in set(cat["services"]) | HARD_ALLOWLIST:
        return {
            "verdict": "VOID",
            "reason": f"service_not_allowlisted:{service}",
            "authority": "BLACK",
        }

    # ── SENSE ──────────────────────────────────────────────────────────────
    probe = probe_service(service)
    if force_failed_probe:
        probe = {**probe, "active": False, "failed": True, "is_active": "inactive", "fault_injected": True}

    envelope = build_state_envelope(
        task="restore_allowlisted_service",
        service=service,
        service_probe=probe,
        execution={
            "rollback_available": True,
            "blast_radius": "LOW",
            "max_mutations": 1,
            "mutate_requested": mutate,
        },
    )

    # ── INTERPRET + OPTIONS ────────────────────────────────────────────────
    # service_local: one allowlisted worker recovery ≠ require global peace
    proposal = recommend(
        envelope,
        a_granted=a_granted,
        human_required=False,
        scope="service_local",
    )
    aeff = proposal["a_effective"]

    stages: list[dict[str, Any]] = [
        {"stage": "SENSE", "envelope_hash": envelope["envelope_hash"], "probe": probe},
        {
            "stage": "INTERPRET",
            "top_hypothesis": proposal["top_hypothesis"],
            "selected": proposal["selected_option_id"],
            "reason": proposal["reason"],
        },
        {"stage": "JUDGE", "a_effective": aeff},
    ]

    action_taken = "none"
    mutation_count = 0
    verify: dict[str, Any] = {"skipped": True}
    final_verdict = "OBSERVE"

    # ── ACT (bounded) ──────────────────────────────────────────────────────
    want_mutate = proposal["selected_option_id"] == "C" and mutate
    if want_mutate and not aeff.get("mutation_allowed"):
        stages.append(
            {
                "stage": "ACT",
                "action": "denied",
                "reason": f"A_effective={aeff['effective_band']} mutation_allowed=false",
            }
        )
        final_verdict = "HOLD"
        action_taken = "denied_by_a_effective"
    elif want_mutate and aeff.get("mutation_allowed"):
        # Precondition: only restart if actually failed (or fault inject)
        if not probe.get("active") or probe.get("fault_injected"):
            code, out = _run(["systemctl", "restart", service])
            mutation_count = 1
            action_taken = "restart_allowlisted_worker"
            stages.append(
                {
                    "stage": "ACT",
                    "action": action_taken,
                    "returncode": code,
                    "output": out[:500],
                    "mutation_count": 1,
                }
            )
            # ── VERIFY ─────────────────────────────────────────────────────
            time.sleep(2)
            post = probe_service(service)
            ok = post.get("active") is True
            verify = {
                "skipped": False,
                "post_probe": post,
                "success": ok,
                "success_test": "active_state_running",
                "observation_window_s": 2,
            }
            stages.append({"stage": "VERIFY", **verify})
            final_verdict = "SEAL" if ok else "HOLD"
            if not ok:
                stages.append(
                    {
                        "stage": "ESCALATE",
                        "action": "stop_retries_enter_HOLD",
                        "notify": True,
                    }
                )
        else:
            action_taken = "noop_already_active"
            stages.append({"stage": "ACT", "action": action_taken})
            final_verdict = "SEAL"
            verify = {"skipped": False, "success": True, "reason": "already_active"}
    elif proposal["selected_option_id"] == "D":
        final_verdict = "HOLD"
        action_taken = "HOLD_and_notify"
        stages.append({"stage": "ACT", "action": action_taken})
    elif proposal["selected_option_id"] == "B":
        final_verdict = "RECOMMEND"
        action_taken = "gather_evidence"
        # Read-only evidence
        _code, logs = _run(
            ["journalctl", "-u", service, "-n", "20", "--no-pager", "-q"], timeout=10
        )
        stages.append(
            {
                "stage": "ACT",
                "action": action_taken,
                "log_tail_lines": len(logs.splitlines()) if logs else 0,
            }
        )
    else:
        final_verdict = "OBSERVE"
        action_taken = "do_nothing"
        stages.append({"stage": "ACT", "action": action_taken})

    # ── LEARN (advisory receipt only — never rewrites constitution) ─────────
    receipt = {
        "schema": "autonomic_recovery_receipt.v1",
        "agent": "autonomic_recovery_v1",
        "timestamp": _now(),
        "service": service,
        "mutate_mode": mutate,
        "observed_condition": proposal["top_hypothesis"],
        "selected_action": action_taken,
        "mutation_count": mutation_count,
        "max_mutations": 1,
        "a_effective": aeff,
        "envelope_hash": envelope["envelope_hash"],
        "stages": stages,
        "verify": verify,
        "final_verdict": final_verdict,
        "proposal": {
            "selected_option_id": proposal["selected_option_id"],
            "reason": proposal["reason"],
        },
        "reusable_rule_candidate": final_verdict == "SEAL" and mutation_count <= 1,
        "constitutional": {
            "may_not_modify": ["F1-F13", "bands", "allowlist", "human_sovereignty"],
            "learning_layer": "advisory_only",
        },
        "w0": "OPERATOR_VETO_INTACT",
        "authority": "BOUNDED_GREEN" if mutate else "OBSERVE_OR_PROPOSE",
    }
    path = _write_receipt(receipt)
    receipt["receipt_path"] = str(path)

    stages.append({"stage": "LEARN", "receipt_path": str(path)})
    receipt["stages"] = stages
    # rewrite with learn stage
    path.write_text(json.dumps(receipt, indent=2, default=str))
    return receipt


def main() -> None:
    import argparse

    p = argparse.ArgumentParser(description="autonomic_recovery_v1 closed loop")
    p.add_argument("--service", default="well-heartbeat.service")
    p.add_argument("--mutate", action="store_true", help="Allow at most one restart")
    p.add_argument(
        "--fault-inject",
        action="store_true",
        help="Simulate failed probe (diagnosis path; mutate still required for restart)",
    )
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    result = run_recovery_loop(
        service=args.service,
        mutate=args.mutate,
        force_failed_probe=args.fault_inject,
    )
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"verdict={result.get('final_verdict')} action={result.get('selected_action')}")
        print(f"band={result.get('a_effective', {}).get('effective_band')} mutations={result.get('mutation_count')}")
        print(f"receipt={result.get('receipt_path')}")


if __name__ == "__main__":
    main()
