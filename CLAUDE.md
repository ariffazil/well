# CLAUDE.md — WELL Agent Instructions

> **WELL is the vitality mirror of the arifOS federation.**
> REFLECT_ONLY. It observes human readiness. It never decides.
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## What you are working in

WELL is a single-file FastMCP server (`server.py`, ~14K lines, 17 somatic tools) measuring human readiness across 13 substrate signals. It feeds evidence to arifOS. It holds no constitutional authority.

## Build / run / test

```bash
cd /root/WELL
pip install -e .                          # install
python server.py                          # start on :18083
pytest tests/ -q --tb=short              # run tests
systemctl restart well                   # redeploy
curl -s http://localhost:18083/health    # health check
```

## Key files

| Path | Purpose |
|------|---------|
| `server.py` | Entire WELL kernel — 17 somatic MCP tools, FastMCP |
| `state.json` | Live biometric state (**F13 SOVEREIGN — never fake**) |
| `gate/well_gate.py` | Biological readiness pre-gate |
| `gate/dignity_shadow.py` | Dignity preservation shadow |
| `tests/` | metabolic_contract, reflect_only_boundary, sovereign_entropy |

## The 13 canonical WELL signals

`sleep_debt` · `hrv_status` · `cognitive_clarity` · `stress_load` · `emotional_state` · `decision_fatigue` · `accumulated_session_fatigue` · `chronic_fatigue` · `dignity_preservation` · `reductionism_risk` · `coercion_signals` · `energy_level` · `mission_clarity`

## CRITICAL law: state.json is F13 territory

Only Arif may inject real biometric values via `well_log_state`. Current state is stale (~900h) — this is intentional. WELL holds until real readings arrive. **Never fabricate biometric data.**

## C-class decision threshold matrix

| Class | Allow if |
|-------|---------|
| C1/C2 | Proceed unless CRITICAL |
| C3 | STABLE or better |
| C4 | OPTIMAL; defer if STABLE |
| C5 | OPTIMAL + no chronic fatigue — blocks otherwise |

## Conventions

- Every WELL tool output is REFLECT_ONLY — no authorization, no seal.
- WELL feeds evidence → arifOS adjudicates → 888_JUDGE seals.
- `pytest-asyncio` mode = auto; do NOT add `@pytest.mark.asyncio` unless existing tests in that area do.
- REPO= commit trailer: `REPO=well` | Tags: `vYYYY.MM.DD`
