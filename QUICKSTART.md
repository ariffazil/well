# WELL Quickstart — 15 Minutes to Running Locally

> **WELL** is the vitality organ of the arifOS federation. It observes and reports human readiness — sleep, fatigue, stress, cognitive clarity, dignity — so that irreversible decisions are never made by or about a depleted human. It reflects. It warns. It never decides.

---

## What You'll Have

A running FastMCP server on `http://localhost:18083` exposing 45 readiness-assessment tools.

## Prerequisites

- Python 3.12+
- pip or uv

## Quickstart

```bash
# 1. Clone
git clone https://github.com/ariffazil/well.git
cd well

# 2. Install (minimal — only one dependency)
pip install fastmcp>=3.3.1

# 3. Start the server
python server.py
```

**That's it.** The server starts on `http://localhost:18083`.

## Verify

```bash
# Health check
curl http://localhost:18083/health | python3 -m json.tool

# Expected: {"verdict": "WELL_HOLD", "service": "well-mcp", ...}

# List all tools
curl -s http://localhost:18083/tools | python3 -m json.tool | head -20
```

For a more realistic test, create a `state.json` file with your readiness data. Without it, WELL operates in mock mode — tools work but biometric scores are synthetic.

## Key Tools

| Tool | What It Does |
|------|-------------|
| `well_assess_homeostasis` | Check sleep, fatigue, stress, emotional balance |
| `well_guard_dignity` | Detect coercion, reductionism risk, consent violations |
| `well_assess_livelihood` | Assess role clarity, purpose, mission alignment |
| `well_compute_metabolic_flux` | Compute cognitive+system entropy rate |
| `well_assess_reliability` | Machine and tool reliability check |

## Common Issues

- **"state.json not found"** → Normal. WELL runs in mock mode. Create a `state.json` with your real data for production use.
- **Port 18083 in use** → Set `WELL_PORT=18084` environment variable before starting.

## Next Steps

- Read the [arifOS Constitution](https://github.com/ariffazil/arifOS/blob/main/docs/CONSTITUTION.md) to understand the governance framework
- Set up [GEOX](https://github.com/ariffazil/geox) for Earth intelligence
- Set up [WEALTH](https://github.com/ariffazil/wealth) for capital intelligence
- Read the [Glossary](https://github.com/ariffazil/arifOS/blob/main/docs/GLOSSARY.md) to understand every term

---

**DITEMPA BUKAN DIBERI — Forged, Not Given.**
