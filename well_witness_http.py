#!/usr/bin/env python3
"""
well_witness_http.py — HTTP health endpoint for WITNESS observer.

Exposes :18084/health for arifOS federation probing.
Wraps well_witness.observe() with a lightweight HTTP server.

Design: Starlette is too heavy for a witness. Use bare http.server.
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

            status_code = 200
            if obs["consensus"]["severity"] == "888_HOLD":
                status = "divergent"
            elif obs["consensus"]["verdict"] == "CONSENSUS":
                status = "ok"
            elif obs["consensus"]["verdict"] == "INSUFFICIENT_DATA":
                status = "degraded"
            else:
                status = "degraded"

            body = {
                "organ": "WITNESS",
                "status": status,
                "version": "1.0.0",
                "commit": _get_commit(),
                "consensus": {
                    "verdict": obs["consensus"]["verdict"],
                    "checks_consensus": obs["consensus"]["checks_consensus"],
                    "checks_total": obs["consensus"]["checks_total"],
                    "severity": obs["consensus"]["severity"],
                },
                "sources": obs["sources"],
                "well_self_reported": obs["well_self_reported"],
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
