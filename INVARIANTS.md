<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-05-26
valid_from: 2026-05-26
valid_until: 2026-06-26
confidence: high
scope: /root/WELL
-->

# INVARIANTS.md — WELL

> Human Substrate & Metabolic State

## Canonical Branch

`main`

## Live Endpoints

| Endpoint | Port | Status |
|----------|------|--------|
| MCP | `http://127.0.0.1:18083/mcp` | ✅ LIVE — `well.service` active |
| Health (public) | `https://well.arif-fazil.com/health` | ✅ LIVE |
| Health (local) | `http://127.0.0.1:18083/health` | ✅ LIVE |

## Required Health Checks

- `curl http://localhost:18083/health` must return `200` with `tool_count: 13`
- `python test_well.py` must pass before any deployment
- `/health tool_count` must equal `SOMATIC_TOOLS` size (13)

## Change Coupling

These files must change together:

- `server.py` — canonical FastMCP server (~11,243 lines, 53 `@mcp.tool` decorators)
- `gate/well_gate.py` — pre-JUDGE biological readiness mirror
- `test_well.py` — plain-Python audit suite
- `TOOL_SURFACE.md` — public MCP surface documentation

## Server Line Count

```
~11,243 lines (server.py)
~10,972 was a stale estimate from pre-PHOENIX-73F refactor
```

## Forbidden Stale Assumptions

- ❌ WELL is NOT "not deployed" — it is live on bare-metal systemd (port 18083)
- ❌ Do not assume port 8083 is in use — port is 18083
- ❌ `test_well.py` uses plain Python, NOT pytest

## Verification

```bash
# Health check
curl http://localhost:18083/health | python3 -m json.tool

# MCP tool count
curl http://localhost:18083/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(f\"tool_count: {d['tool_count']}\")"

# Restart after changes
systemctl restart well

# Tests
python test_well.py
```
