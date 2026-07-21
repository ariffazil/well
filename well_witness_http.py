#!/usr/bin/env python3
"""
well_witness_http.py — HTTP health endpoint for WITNESS observer.

Exposes :18084/health for arifOS federation probing.
Wraps well_witness.observe() with a lightweight HTTP server.

Design: Starlette is too heavy for a witness. Use bare http.server.

v1.1.0 — surfaces source_integrity, service_probes, telemetry_freshness,
self_check, advanced_severity, and signal audit. Severity 888_HOLD returns 503
so monitors do not silently believe a sandbagged witness.
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Add parent to path for witness import
sys.path.insert(0, str(Path(__file__).parent))

from well_witness import observe, verify_chain


class WitnessHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health" or self.path == "/":
            # Run observation
            obs = observe()
            chain = verify_chain()

            severity = obs["consensus"]["severity"]
            verdict = obs["consensus"]["verdict"]

            # Severity → HTTP status. 888_HOLD must NOT silently return 200 — that
            # would let monitors think the witness is healthy when the substrate is
            # being sandbagged. 503 means "service unavailable but a witness is
            # alive enough to tell you why". WARN is non-fatal → keep 200 so
            # orchestration does not restart-loop on a real divergence signal.
            status_code = 200
            if severity == "888_HOLD":
                status = "divergent"
                status_code = 503
            elif severity == "WARN":
                status = "warn"
            elif severity == "DEGRADED":
                status = "degraded"
            elif verdict == "CONSENSUS":
                status = "ok"
            elif verdict == "INSUFFICIENT_DATA":
                status = "degraded"
            else:
                status = "degraded"

            adv = obs.get("advanced", {})
            adv_sev = obs.get("advanced_severity", {})
            signal = obs.get("signal", {})

            body = {
                "organ": "WITNESS",
                "status": status,
                "version": "1.2.0",
                "commit": _get_commit(),
                "consensus": {
                    "verdict": verdict,
                    "checks_consensus": obs["consensus"]["checks_consensus"],
                    "checks_total": obs["consensus"]["checks_total"],
                    "severity": severity,
                },
                "sources": obs["sources"],
                "well_self_reported": obs["well_self_reported"],
                "advanced": {
                    "source_integrity": {
                        "verdict": adv.get("source_integrity", {}).get("verdict"),
                        "head_commit": adv.get("source_integrity", {}).get("head_commit"),
                        "files_intact": adv.get("source_integrity", {}).get("files_intact"),
                        "files_total": adv.get("source_integrity", {}).get("files_total"),
                        "any_violation": adv.get("source_integrity", {}).get("any_violation"),
                    },
                    "service_probes": {
                        "verdict": adv.get("service_probes", {}).get("verdict"),
                        "active": adv.get("service_probes", {}).get("active"),
                        "total": adv.get("service_probes", {}).get("total"),
                        "inactive_critical": adv.get("service_probes", {}).get("inactive_critical"),
                    },
                    "telemetry_freshness": {
                        "verdict": adv.get("telemetry_freshness", {}).get("verdict"),
                        "age_seconds": adv.get("telemetry_freshness", {}).get("age_seconds"),
                        "max_age_seconds": adv.get("telemetry_freshness", {}).get("max_age_seconds"),
                    },
                    "self_check": {
                        "verdict": adv.get("self_check", {}).get("verdict"),
                        "can_observe": adv.get("self_check", {}).get("can_observe"),
                        "critical_blind": adv.get("self_check", {}).get("critical_blind"),
                        "channels": adv.get("self_check", {}).get("channels"),
                    },
                    "runtime_attestation": {
                        "verdict": adv.get("runtime_attestation", {}).get("verdict"),
                        "identity_match": adv.get("runtime_attestation", {}).get("identity_match"),
                        "git_head": adv.get("runtime_attestation", {}).get("git_head"),
                        "well_self_reported": adv.get("runtime_attestation", {}).get("well_self_reported"),
                        "mismatch_detail": adv.get("runtime_attestation", {}).get("mismatch_detail"),
                    },
                },
                "advanced_severity": adv_sev,
                "signal": signal,
                "chain": {
                    "entries": chain["entries"],
                    "valid": chain["valid"],
                },
                "w0": "OPERATOR_VETO_INTACT",
                "boundary": "WITNESS observes. arifOS judges. A-FORGE executes.",
            }

            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(body, default=str).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error":"not found"}')

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def _get_commit() -> str:
    try:
        import subprocess

        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=Path(__file__).parent,
            text=True,
        ).strip()
    except Exception:
        return "unknown"


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18084
    server = HTTPServer(("127.0.0.1", port), WitnessHandler)
    print(f"WITNESS HTTP on :{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWITNESS stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
