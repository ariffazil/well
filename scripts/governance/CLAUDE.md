# CLAUDE.md — WELL Agent Instructions

> **Canonical agent instruction file:** `/root/AAA/CLAUDE.md`
> **WELL** — vitality mirror of the arifOS federation.
> **Port:** 18083 | **Runtime:** Python 3.12+, FastMCP
> REFLECT_ONLY. It observes human readiness. It never decides.

**DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## What you are working in

WELL is a pure-Python organ with a single-file FastMCP server (`server.py`, ~15,755 lines, **22 somatic tools**). It measures human readiness across 13 substrate signals, feeds evidence to arifOS, and holds no constitutional authority.

**New (Phase 2 — 2026-06-21):** vault_bridge Phase 2 — async VAULT999 writer seal path, metabolic flux extraction, freshness computation, ADR-001 local fallback.

## Build / run / test

```bash
cd /root/WELL
uv sync --frozen                    # install
python server.py                    # start on :18083
pytest tests/ -q --tb=short        # run tests
python test_well.py                 # audit suite
systemctl restart well              # redeploy
curl -s http://localhost:18083/health
```

## Key files

| Path | Purpose |
|------|---------|
| `server.py` | FastMCP server (~15,755 lines, 22 somatic tools) |
| `vault_bridge.py` | VAULT999 async writer + freshness computation (Phase 2) |
| `state.json` | Live biometric state (**F13 SOVEREIGN — never fake**) |
| `gate/well_gate.py` | Pre-JUDGE biological readiness mirror |
| `gate/dignity_shadow.py` | Dignity preservation shadow |
| `telemetry/budget_violations.jsonl` | Compute budget tracking |

## The 13 canonical WELL signals

`sleep_debt` · `hrv_status` · `cognitive_clarity` · `stress_load` · `emotional_state` · `decision_fatigue` · `accumulated_session_fatigue` · `chronic_fatigue` · `dignity_preservation` · `reductionism_risk` · `coercion_signals` · `energy_level` · `mission_clarity`

## CRITICAL: state.json is F13 territory

Only Arif may inject real biometric values via `well_log_state`. Current state is from the last real reading — this is intentional. WELL holds until real readings arrive. **Never fabricate biometric data.**

## C-class decision threshold matrix

| Class | Allow if |
|-------|---------|
| C1/C2 | Proceed unless CRITICAL |
| C3 | STABLE or better |
| C4 | OPTIMAL; defer if STABLE |
| C5 | OPTIMAL + no chronic fatigue — blocks otherwise |

## Conventions

- Every WELL tool output is REFLECT_ONLY — no authorization, no seal
- WELL feeds evidence → arifOS adjudicates → 888_JUDGE seals
- `pytest-asyncio` mode = auto
- REPO=well commit trailer | Tags: `vYYYY.MM.DD`
- **Stale SOT files:** CLAUDE.md ✅ Updated 2026-07-01
