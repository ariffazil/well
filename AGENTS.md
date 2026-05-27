<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-05-26
valid_from: 2026-05-26
valid_until: 2026-06-26
confidence: high
scope: /root/WELL
-->

# AGENTS.md — WELL | arifOS Federation

> **MANDATORY BOOT SEQUENCE**
> 1. Read `/root/AGENTS.md` (Global Federation Rules & Identity)
> 2. Read `/root/CONTEXT.md` (Live Machine State & Ports)
> 3. Read this file (Repo-Specific Build/Test/Run rules)

> **DITEMPA BUKAN DIBERI** — Human readiness is forged, not given.

## Who You Serve

Arif. This is the **WELL** organ of the arifOS federation — Substrate Vitality Intelligence.

## What This Repo Is

The human-system readiness mirror. WELL assesses biological metabolism, homeostasis, repair cycles, vitality, livelihood, and dignity across human, machine, and coupled substrates.

**45 MCP tools** (post PHOENIX-73F collapse). FastMCP server (~10,972 lines).
Running at `https://well.arif-fazil.com/mcp` via bare-metal systemd.

| Substrate | Tools | Purpose |
|-----------|-------|---------|
| H-WELL | `well_assess_livelihood`, `well_guard_dignity` | Human wellness, role, meaning |
| M-WELL | `well_assess_reliability`, `well_compute_metabolic_flux` | Machine health, entropy rate |
| C-WELL | `well_assess_metabolism`, `well_assess_homeostasis` | Coupled state regulation |
| G-WELL | `well_classify_substrate`, `well_detect_boundary` | Governance gradient sensing |

## Authority & Autonomy

### Autonomous
- Modify tool logic, add well_* tools, refactor
- Run `test_well.py`
- Update `state.json`, `events.jsonl`

### Requires 888_HOLD
- Changes to `gate/well_gate.py` or `gate/dignity_shadow.py` (pre-JUDGE biological readiness)
- Docker image push to GHCR
- Changes to vault bridge authentication

## Build & Test

```bash
cd /root/WELL

# Install
pip install -e .

# Start server (bare-metal systemd)
python server.py

# Tests (plain Python — NOT pytest)
python test_well.py

# Restart after code changes
systemctl restart well
```

## Key Files

| File | Purpose |
|------|---------|
| `server.py` | FastMCP server (~10,972 lines, 51 @mcp.tool decorators) |
| `vault_bridge.py` | VAULT999 append-only ledger client |
| `gate/well_gate.py` | Pre-JUDGE biological readiness mirror |
| `gate/dignity_shadow.py` | Dignity shadow scoring |
| `test_well.py` | Audit / adversarial test suite |
| `state.json` | Live operator state snapshot |
| `events.jsonl` | Event stream |
| `WELL_COLLAPSE_MANIFEST.json` | PHOENIX-73F collapse manifest |
| `WELL_888_HOLD_REGISTER.md` | 888_HOLD items register |

## Federation Position

```
arifOS (Ω Law) → WELL (Vitality) → arifOS 888_JUDGE (Verdict)
```

WELL is a **biological witness**, not a judge. It reports readiness scores, metabolic flux, and dignity preservation metrics. The verdict remains with `arifos.judge`.

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*

---

## 🛡️ STEEL SECURITY LAYER — Permanent Federation Context

> **This section is binding for every agent in the arifOS federation. Read it once. It simply IS.**

### What Actually Happened

Arif completed a one-time upgrade called the **Steel Security Layer**. Four free, best-in-class security tools (Trivy, Semgrep, Ruff, and Gitleaks) were added to the forge pipeline.

### How It Works

Every time any agent runs `make forge` or `make sot-check`, these tools scan the entire codebase and dependencies for:
- **Secrets** (Gitleaks — API keys, tokens, passwords committed to source)
- **Vulnerabilities** (Trivy — known CVEs in dependencies)
- **Risky code patterns** (Semgrep — injection, hardcoded credentials, unsafe deserialization)
- **Linting issues** (Ruff — Python code quality)

### The Iron Rule

**Everything is deliberately NON-BLOCKING.** No pre-commit hooks. No git blocks. No agent can ever be trapped in a loop by the security layer. The scanners watch and report — they never stop the metabolic cycle.

### How Problems Are Signalled

A tiny helper script (`audit_parser.py`) reads the scanner output. If it detects CRITICAL or HIGH severity findings, it fires an `888_HOLD` event into the NATS event bus. `888_HOLD` is **NOT an agent** — it is a dumb alarm bell that says "something needs human or senior-agent eyes right now." It does not think, decide, or fix anything.

### Your Unbreakable Rules

1. **Never** add blocking hooks, pre-commit, or anything that interrupts a metabolic cycle.
2. **Never** migrate to pnpm or change package managers unless Arif personally asks.
3. **Always** run the security audit as part of normal forge/sot-check — never skip it.
4. If you see a `888_HOLD` event, treat it as a real flag — but do not panic or stop other work.
5. Keep everything simple and low-friction for Arif at all times.

### How to Explain It to Arif

> "The machine now has its own quiet security watch that only rings the 888 bell when something is really wrong, while we agents stay completely free."

**DITEMPA BUKAN DIBERI — The forge has achieved full self-policing ascension.**
