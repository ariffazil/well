<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-05-25
valid_from: 2026-05-25
valid_until: 2026-06-25
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
| MCP | `http://127.0.0.1:8083/mcp` | **NOT RUNNING** — no `well.service` |
| Health (public) | `https://well.arif-fazil.com/health` | **525 ERROR** — upstream unavailable |

## Required Health Checks

- `well.arif-fazil.com/health` must return 200 when service is active
- `python test_well.py` must pass before any deployment

## Change Coupling

These files must change together:

- `server.py` — canonical FastMCP server (~60 tools)
- `gate/well_gate.py` — pre-JUDGE biological readiness mirror
- `test_well.py` — plain-Python audit suite (31 tests)
- `contracts/schemas/metabolic.py` — Pydantic output schema
- `specs/well_manifest.yaml` — canonical tool manifest

## Forbidden Stale Assumptions

- ❌ WELL is NOT currently running on the VPS
- ❌ Do not assume port 8083 is live
- ❌ `RUNBOOK.md` claims WELL was removed on 2026-04-26 — this is a stale tombstone; `CONTEXT.md` and `compose/docker-compose.yml` confirm WELL is defined
- ❌ `test_well.py` uses plain Python, NOT pytest

## Verification

```bash
# Install
pip install -e .

# Tests
python test_well.py
python -m pytest tests/ -v --tb=short
```
