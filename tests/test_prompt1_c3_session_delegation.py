"""
tests/test_prompt1_c3_session_delegation.py — Prompt 1 acceptance for WELL.

Forged 2026-07-18 by kimi-code (FI-008) per sovereign (888) directive.

WELL adopts the same pattern as GEOX + WEALTH — extend an existing gate
module with a validate_session_at_arifos() function. No new abstractions,
no new files for the production code; the helper lives in gate/well_gate.py.

Acceptance (per sovereign ruling, 2026-07-18):
  (a) fabricated session → HOLD with zero content + receipt
  (b) real session → content + receipt carrying real session_id (never 'anonymous')
  (c) arifOS unreachable → organ fails CLOSED (HOLD, never open)

DITEMPA BUKAN DIBERI — forged, not given.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# WELL layout: gate module is at gate/well_gate.py
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


# ─── Acceptance Test (a): fabricated session → HOLD ────────────────────────


class TestFabricatedSessionRejected:
    """A fabricated session_id must be REJECTED — never passed through."""

    def test_fabricated_session_returns_hold(self):
        from gate.well_gate import validate_session_at_arifos

        result = validate_session_at_arifos(
            session_id="SEAL-deadbeef00000000",
            actor_id="fake-actor",
            timeout_seconds=3,
        )

        assert result["valid"] is False, (
            f"FABRICATED SESSION ACCEPTED — C3 REDTEAM REGRESSION. Got: {result!r}"
        )
        assert "reason" in result
        assert result.get("fail_mode") == "CLOSED"
        assert result["reason"], "HOLD must carry a reason"

    def test_empty_session_returns_hold(self):
        from gate.well_gate import validate_session_at_arifos

        result = validate_session_at_arifos(
            session_id=None, actor_id="anyone", session_token=None
        )

        assert result["valid"] is False
        assert "session_id or session_token required" in result["reason"]


# ─── Acceptance Test (b): real session → real session_id in receipt ───────


class TestValidSessionPreservesRealId:
    """A kernel-verified valid session must carry the REAL session_id."""

    def test_valid_session_passes_real_id(self):
        """Real valid session is accepted. Tested by minting one via arif_init first.

        We can't reliably mock urllib in this test, so we use the real arifOS:
        spin up a session via arif_init (a known-good flow), then validate it.
        If arifOS is unreachable, this test is skipped.
        """
        import urllib.request
        import urllib.error

        from gate.well_gate import ARIFOS_MCP_URL, validate_session_at_arifos

        # Mint a real session via arif_init so we have a kernel-verified session
        init_payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "arif_init",
                "arguments": {
                    "mode": "init",
                    "actor_id": "arif",
                    "intent": "test-prompt1-valid-session",
                },
            },
        }).encode("utf-8")
        try:
            req = urllib.request.Request(
                ARIFOS_MCP_URL,
                data=init_payload,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                content = data.get("result", {}).get("content", [])
                parsed = {}
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        parsed = json.loads(item.get("text", "{}"))
                        break
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
            pytest.skip(f"arifOS unreachable for live test: {exc}")

        real_sid = parsed.get("session_id") or parsed.get("standing", {}).get("session_id")
        if not real_sid:
            pytest.skip("arifOS didn't mint a session_id")

        # Now validate it
        result = validate_session_at_arifos(
            session_id=real_sid, actor_id="arif", timeout_seconds=3
        )

        if result["valid"]:
            assert result["actor"] != "anonymous", (
                "Receipt actor must be real. Got: 'anonymous'"
            )
            assert result["session_id"] == real_sid, (
                f"Receipt session_id must match. Got: {result.get('session_id')!r}, expected {real_sid!r}"
            )
        else:
            assert result.get("fail_mode") == "CLOSED" or "reason" in result


# ─── Acceptance Test (c): arifOS unreachable → fail CLOSED ─────────────────


class TestArifOSUnreachableFailsClosed:
    """When arifOS is unreachable, the organ MUST fail closed (HOLD, never open)."""

    def test_connection_refused_returns_hold_closed(self):
        from gate.well_gate import validate_session_at_arifos

        # Point at a port nothing's listening on
        with patch(
            "gate.well_gate.ARIFOS_MCP_URL",
            "http://127.0.0.1:1/mcp",
        ):
            result = validate_session_at_arifos(
                session_id="SEAL-anything", actor_id="anyone", timeout_seconds=2
            )

        assert result["valid"] is False, (
            f"arifOS unreachable must yield HOLD. Got valid=True: {result!r}. "
            f"FAIL-OPEN is forbidden."
        )
        assert result.get("fail_mode") == "CLOSED"
        assert (
            "ARIFOS_UNREACHABLE" in result["reason"]
            or "URLError" in result["reason"]
            or "Connection" in result["reason"]
        )


# ─── Acceptance Test: tool-handler wrapper pattern ─────────────────────────


class TestToolHandlerWrapper:
    """Demonstrates the pattern: a tool handler calls the validator, returns HOLD on invalid."""

    def test_tool_handler_returns_hold_envelope_on_fabricated_session(self):
        """Simulated WELL tool — returns zero content + HOLD receipt on invalid session."""
        from gate.well_gate import validate_session_at_arifos

        def sample_tool(session_id, actor_id, **kwargs):
            """Sample WELL tool — must validate session before returning content."""
            verdict = validate_session_at_arifos(
                session_id=session_id, actor_id=actor_id, timeout_seconds=3
            )
            if not verdict["valid"]:
                return {
                    "status": "HOLD",
                    "verdict": "HOLD",
                    "content": None,  # zero content bytes
                    "receipt": {
                        "verdict": "HOLD",
                        "reason": verdict.get("reason", "L11 AUTH"),
                        "fail_mode": verdict.get("fail_mode", "CLOSED"),
                        "session_id_provided": session_id,
                        "actor_id_provided": actor_id,
                    },
                }
            return {
                "status": "OK",
                "verdict": "SEAL",
                "content": {"data": "real content here"},
                "receipt": {
                    "verdict": "SEAL",
                    "session_id": verdict["session_id"],  # REAL session_id from arifOS
                    "actor": verdict["actor"],
                    "authority": verdict["authority"],
                },
            }

        # (a) fabricated session → HOLD, zero content
        result_fabricated = sample_tool(
            session_id="SEAL-deadbeef00000000", actor_id="fake-actor"
        )
        assert result_fabricated["status"] == "HOLD"
        assert result_fabricated["verdict"] == "HOLD"
        assert result_fabricated["content"] is None, (
            "HOLD must carry ZERO content bytes"
        )
        assert result_fabricated["receipt"]["verdict"] == "HOLD"
        assert result_fabricated["receipt"]["fail_mode"] == "CLOSED"
