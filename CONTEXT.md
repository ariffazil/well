# CONTEXT.md — WELL (Human Readiness)

> **Organ:** WELL | **Port:** 18083 | **Repo:** `ariffazil/well`
> **Last Updated:** 2026-06-21

## Live State
- **Service:** `well.service` (systemd, enabled)
- **Health:** `http://127.0.0.1:18083/health`
- **Tools:** 21 somatic MCP tools (+4 from v2026.06 release)
- **Authority:** REFLECT_ONLY — never adjudicates
- **Biometric State:** truth_status=EXPIRED (F13 sovereign territory)

## Key Updates (2026-06-21)
- **vault_bridge Phase 2** — async VAULT999 writer seal path, metabolic flux extraction, freshness computation
- **ADR-001** — local-only persistence for biometric data isolation (F6 MARUAH)
- **21 tools** (was 17) — metabolic_flux, reliability check, substrate classification added

## Dependencies
- arifOS MCP kernel (port 8088) — constitutional judgment
- No database dependencies (local-only persistence per ADR-001)
- Caddy reverse proxy for public endpoint

## Federation Context
- Federation organs = 7: arifOS (8088), AAA (3001), A-FORGE (7071), GEOX (8081), WEALTH (18082), WELL (18083), APEX legacy (3002)
- A-FORGE hosts support services MIND (51001) and MEMORY (51002)
- APEX (3002) is legacy health probe; 888 JUDGE deliberation in AAA a2a-server

## Known Issues
- `state.json` truth_status=EXPIRED — sovereign biometric data needed
- `vault_ledger.jsonl` misnamed empty dir — ✅ cleaned 2026-06-21
