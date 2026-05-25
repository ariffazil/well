# WELL Status — 2026-05-25
> **DITEMPA BUKAN DIBERI** — Human Readiness Intelligence.

## Current Status: NOT DEPLOYED

WELL is **not currently deployed** on the VPS. The service does not exist.
Attempting to access `well.arif-fazil.com` will return **404 Not Found**.

This is **intentional** — WELL is reserved for future deployment when the service is ready.

## What WELL Is

WELL is the **Human Readiness Intelligence** organ of the arifOS federation.
It models metabolic health, cognitive readiness, and human vitality as thermodynamic invariants.

- **Port when deployed:** `18083` (organ-standard; aligns with GEOX 18081, WEALTH 18082)
- **Planned health endpoint:** `https://well.arif-fazil.com/health`
- **Planned MCP endpoint:** `https://well.arif-fazil.com/mcp`
- **Governance:** F1-F13 floor enforcement via `organ_governance.py`

## Deployment Prerequisites

Before deploying WELL:
1. Verify `python3 /root/WELL/server.py` boots cleanly on port 18083
2. Confirm governance wrapper loads (log shows: `[GOVERNANCE] WELL governance wrapper active`)
3. Confirm `/health` returns `{"status":"healthy",...}`
4. Uncomment the `well.arif-fazil.com` block in `/root/arifOS/Caddyfile`
5. Reload Caddy: `sudo systemctl reload caddy`
6. Verify public endpoint: `curl https://well.arif-fazil.com/health`

## What NOT To Do

- Do NOT create fake routes pointing to dead ports
- Do NOT mark WELL as "live" in federation manifests if no service exists
- Do NOT deploy WELL without governance wrapper loading cleanly
- Do NOT expose WELL publicly until health endpoint is verified

## Current Live Services (for reference)

| Domain | Port | Status |
|--------|------|--------|
| arifos.arif-fazil.com | 8088 | ✅ LIVE |
| geox.arif-fazil.com | 18081 | ✅ LIVE |
| wealth.arif-fazil.com | 18082 | ✅ LIVE |
| well.arif-fazil.com | 18083 | ⛔ NOT DEPLOYED |
