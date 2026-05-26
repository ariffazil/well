# WELL Status — 2026-05-26
> **DITEMPA BUKAN DIBERI** — Human Readiness Intelligence.

## Current Status: OPERATIONAL

WELL is **live on bare-metal systemd** at `https://well.arif-fazil.com`.

## Live Endpoints

| Endpoint | Port | Status |
|----------|------|--------|
| MCP | `http://127.0.0.1:18083/mcp` | ✅ LIVE — `well.service` active |
| Health (public) | `https://well.arif-fazil.com/health` | ✅ LIVE |
| Health (local) | `http://127.0.0.1:18083/health` | ✅ LIVE |

## Service Management

```bash
# Restart after code changes
systemctl restart well

# Check status
systemctl status well

# View logs
journalctl -u well -f
```

## MCP Surface

- **Live public tools:** 13
- **Invariant:** `/health tool_count = SOMATIC_TOOLS = ChatGPT MCP registration = 13`
- **Enforced by:** `_enforce_somatic_boundary()` at startup — strips all `@mcp.tool` not in `SOMATIC_TOOLS`

## Deployment Verification

```bash
# 1. Health check (local)
curl http://localhost:18083/health | python3 -m json.tool

# 2. MCP tool count
curl http://localhost:18083/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(f\"tool_count: {d['tool_count']}\")"

# 3. MCP tool list
curl http://localhost:18083/tools

# 4. Public endpoint
curl https://well.arif-fazil.com/health
```

## Governance

- **Authority:** arifOS (F1-F13 floors, 888_JUDGE)
- **Boundary:** `SOMATIC_TOOLS` enforced at startup — no unlisted tools reach MCP clients
- **Source of truth for federation status:** `ariffazil/arifOS/FEDERATION_STATUS.md`

---

*Last Verified: 2026-05-26 | PHOENIX-73F | DITEMPA BUKAN DIBERI*
