"""
A2A Card Consolidation — WELL Scope Regression Tests
═══════════════════════════════════════════════════════

Proves the local A2A agent-card implementations have been removed from
WELL as part of the federation-wide A2A card consolidation.

Canonical A2A card surfaces are owned by AAA at
  `/.well-known/agent.json` and `/.well-known/agent-card.json`
(see /root/AAA/docs/AGENT_IDENTITY.md and /root/AAA/UNIFIED_AGENT.md).

WELL keeps only:
  - MCP server card manifests (.well-known/mcp/server.json)
  - health / ready / tools / build-info surfaces
  - Caddy-fronted public ingress (no local card duplication)

These tests are self-contained: they read the source from the filesystem
and assert structural invariants, then dynamically import server.py and
assert that no card handler symbols leak into the module namespace.
No HTTP server is started.

Run: cd /root/WELL && python3 -m pytest tests/test_a2a_card_consolidation.py -v
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER_PY = ROOT / "server.py"
WELL_KNOWN = ROOT / ".well-known"

# Forbidden symbols — local A2A card handler names that must NOT exist
# anywhere in the WELL scope after the consolidation.
FORBIDDEN_SYMBOLS = (
    "_WELL_AGENT_CARD",
    "_well_agent_card_handler",
    "_WELL_A2A_CARD",
    "_well_a2a_card",
)

# Forbidden URL paths — local A2A card routes that must NOT be registered
# by server.py at module scope.
FORBIDDEN_ROUTES = (
    "/.well-known/agent.json",
    "/.well-known/agent-card.json",
)

# Forbidden local card file (per task spec).
FORBIDDEN_LOCAL_FILES = (
    WELL_KNOWN / "agent-card.json",
)


# ── 1. Source-level: server.py does not contain local card symbols ─────────


def test_server_py_has_no_local_agent_card_dict():
    """`_WELL_AGENT_CARD = { ... }` and `_WELL_A2A_CARD = { ... }`
    must be gone from the source."""
    src = SERVER_PY.read_text(encoding="utf-8")
    for sym in ("_WELL_AGENT_CARD", "_WELL_A2A_CARD"):
        # Match `sym = {` (with optional whitespace) — that is a dict assignment.
        assert not re.search(
            rf"^\s*{re.escape(sym)}\s*=\s*\{{",
            src,
            flags=re.MULTILINE,
        ), f"server.py still contains a `{sym} = {{ ... }}` dict assignment"


def test_server_py_has_no_local_card_handlers():
    """`_well_agent_card_handler` and `_well_a2a_card` async defs
    must be gone from the source."""
    src = SERVER_PY.read_text(encoding="utf-8")
    for fn in ("_well_agent_card_handler", "_well_a2a_card"):
        assert not re.search(
            rf"^\s*(async\s+)?def\s+{re.escape(fn)}\s*\(",
            src,
            flags=re.MULTILINE,
        ), f"server.py still defines `{fn}`"


def test_server_py_has_no_local_card_routes():
    """`app.add_route("/.well-known/agent[-card].json", ...)` lines
    must be gone from the source. The forbidden path strings may appear
    in the NOTE comments, so we match actual `add_route` call sites only."""
    src = SERVER_PY.read_text(encoding="utf-8")
    for path in FORBIDDEN_ROUTES:
        # Match `add_route("<path>"` (the path is always a string literal
        # in this codebase). Strip comment lines first to avoid false
        # positives from the consolidation NOTE.
        non_comment = "\n".join(
            line for line in src.splitlines() if not line.lstrip().startswith("#")
        )
        pattern = rf'add_route\(\s*["\']{re.escape(path)}["\']'
        assert not re.search(pattern, non_comment), (
            f"server.py still registers route {path!r} via add_route"
        )


# ── 2. Filesystem-level: local card file is absent ──────────────────────────


def test_local_agent_card_file_is_absent():
    """The local .well-known/agent-card.json must be removed (per task spec).
    The file was the A2A-v2 arifOS wrapper view; canonical is AAA-owned."""
    assert not (WELL_KNOWN / "agent-card.json").exists(), (
        "Local .well-known/agent-card.json still exists; "
        "remove it (canonical A2A card is owned by AAA)."
    )


def test_mcp_manifest_still_present():
    """Sanity: the MCP server.json manifest is NOT removed.
    Consolidation only targets the A2A agent-card, not the MCP surface."""
    assert (WELL_KNOWN / "mcp" / "server.json").exists(), (
        "MCP manifest .well-known/mcp/server.json must remain"
    )


def test_agent_json_still_present():
    """Sanity: the A2A agent.json (different from agent-card.json) is
    a different file and is preserved. Only agent-card.json is removed."""
    assert (WELL_KNOWN / "agent.json").exists(), (
        ".well-known/agent.json must remain (different schema, not in scope)"
    )


# ── 3. Module-level: dynamically loaded server has no card symbols ──────────


def test_module_scope_has_no_local_card_symbols():
    """Importing server.py must NOT surface any local A2A card handler
    symbol into the module namespace."""
    spec = importlib.util.spec_from_file_location(
        "_well_server_under_test", SERVER_PY
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    leaked = [s for s in FORBIDDEN_SYMBOLS if hasattr(mod, s)]
    assert not leaked, (
        f"Local A2A card symbols leaked into server module scope: {leaked}"
    )


# ── 4. Source-level: the consolidation comment is present ───────────────────


def test_consolidation_note_present():
    """The consolidation note must be present so future readers know
    why the local card route is gone and where the canonical surface lives."""
    src = SERVER_PY.read_text(encoding="utf-8")
    assert "A2A consolidation 2026-07-15" in src, (
        "Missing consolidation note that explains the local card route removal"
    )
    assert "AAA" in src and "AGENT_IDENTITY" in src, (
        "Consolidation note should reference the canonical AAA location"
    )


# ── 5. Source-level: unrelated health/tools/OAuth routes are preserved ─────


def test_unrelated_routes_still_present():
    """Sanity: removing the local A2A card route must NOT remove the
    canonical health, ready, tools, build-info, OAuth, or MCP routes.
    These are the public surfaces WELL is responsible for."""
    src = SERVER_PY.read_text(encoding="utf-8")
    for needle in (
        '"/health"',
        '"/ready"',
        '"/tools"',
        '"/api/build-info"',
        '"/.well-known/mcp.json"',
        '"/.well-known/mcp/server.json"',
        "/.well-known/oauth-protected-resource",
        "/.well-known/oauth-authorization-server",
    ):
        assert needle in src, (
            f"Unrelated route {needle!r} was removed; consolidation "
            f"must NOT touch non-card surfaces."
        )


# ── 6. Source-level: well_registry_status is untouched ──────────────────────


def test_well_registry_status_untouched():
    """Sanity: the P0.5 registry classification that the parent task
    already shipped is still present. This test ensures the A2A
    consolidation did not accidentally regress the prior work."""
    src = SERVER_PY.read_text(encoding="utf-8")
    assert "well_system_registry_status" in src, (
        "P0.5 hidden-internal-alias logic for well_system_registry_status "
        "should still be present (was a separate prior fix)."
    )
    assert "P0.5 fix" in src or "P0.5" in src, (
        "P0.5 marker comment should still be present"
    )


# ── 7. No JSONResponse import dangling from removed handlers ───────────────


def test_jsonresponse_still_imported():
    """Sanity: starlette.responses.JSONResponse is still used elsewhere
    in server.py (health, tools, build-info handlers), so the import
    must NOT have been removed. If this test fails, either JSONResponse
    is no longer used, or the consolidation accidentally removed it."""
    src = SERVER_PY.read_text(encoding="utf-8")
    assert "from starlette.responses import JSONResponse" in src, (
        "JSONResponse import was removed; consolidation must not "
        "remove shared imports."
    )
    # The import is referenced in multiple places — count at least 3.
    refs = len(re.findall(r"JSONResponse", src))
    assert refs >= 3, (
        f"JSONResponse appears only {refs}x in server.py; "
        f"consolidation may have removed too much"
    )


# ── 8. Module imports cleanly (regression) ──────────────────────────────────


def test_server_module_imports_cleanly():
    """Re-importing server.py must succeed without syntax errors.
    This catches accidental truncation from the edit."""
    spec = importlib.util.spec_from_file_location(
        "_well_server_under_test_v2", SERVER_PY
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # mcp is the canonical entry point; if it's gone, the module is broken.
    assert hasattr(mod, "mcp"), "server.mcp not defined after consolidation"


# ── Runner ─────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    import traceback

    tests = [
        v for k, v in globals().items() if k.startswith("test_") and callable(v)
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  PASS  {t.__name__}")
        except Exception:
            failed += 1
            print(f"  FAIL  {t.__name__}")
            traceback.print_exc()
    print()
    print(f"  Total: {passed + failed} | Passed: {passed} | Failed: {failed}")
    sys.exit(0 if failed == 0 else 1)
