# CONTEXT.md — WELL (Human Readiness)

> **Organ:** WELL | **Port:** 18083 | **Repo:** `ariffazil/well`
> **Kernel SoT:** `ariffazil/arifos` (FEDERATION_CONTRACT.md + GENESIS/000)
> **Live status:** `ariffazil/arifos/FEDERATION_STATUS.md`
> **Last Updated:** 2026-06-14

## Live State
- **Service:** `well.service` (systemd, enabled)
- **Health:** `http://127.0.0.1:18083/health`
- **Tools:** 17 somatic MCP tools
- **Authority:** REFLECT_ONLY — never adjudicates
- **Biometric State:** truth_status=EXPIRED (F13 sovereign territory)

## Dependencies
- arifOS MCP kernel (port 8088) — constitutional judgment
- No database dependencies
- Caddy reverse proxy for public endpoint

## Federation Context
- Federation organs = 7: arifOS (8088), AAA (3001), A-FORGE (7071), GEOX (8081), WEALTH (18082), WELL (18083), APEX legacy (3002).
- A-FORGE hosts support services `MIND` on port 51001 and `MEMORY` on port 51002.
- APEX (port 3002) is a legacy health probe; 888 JUDGE deliberation now lives in the AAA a2a-server.

## Current Focus
- Operational. GENESIS/004-012 canon chain established.
- Biometric state stale — needs Arif sovereign injection via `well_log_state` or `biometric_inject.sh`.

## Known Issues
- `state.json` truth_status=EXPIRED — sovereign biometric data needed
- `well_autosleeper.py` and `entropy-report.json` removed; both are now ignored generated artifacts
