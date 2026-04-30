# WELL — Biological Mirror

> **Substrate intelligence for the arifOS Constitutional Federation.**
> **DITEMPA BUKAN DIBERI — Intelligence is forged, not given.**

[![WELL](https://img.shields.io/badge/WELL-v1.0.0-00D4AA?style=flat-square)](https://github.com/ariffazil/well)
[![MCP](https://img.shields.io/badge/MCP-FastMCP-7C3AED?style=flat-square)](https://github.com/ariffazil/well)
[![arifOS](https://img.shields.io/badge/arifOS-F1%E2%80%93F13_Governed-FF6B00?style=flat-square)](https://github.com/ariffazil/arifOS)
[![License](https://img.shields.io/badge/License-AGPL_V3-4EAF0C?style=flat-square)](./LICENSE)

---

## What WELL Is

WELL is the **Human–Machine Substrate Governance Layer** for arifOS. It provides high-signal biological and technical readiness telemetry to ensure that intent is verified before it is forged into action.

WELL is the **mirror** — it reflects the state of the human and machine substrate so arifOS can judge whether the current configuration is safe for the decision class at hand. It does not veto. It informs.

> *W0 Sovereignty Invariant: WELL holds a mirror, not a veto. It informs the arifOS JUDGE, but the Operator (Arif) retains final authority.*

---

## Position in the arifOS Trinity

```
Operator (Arif) → WELL (Mirror) → arifOS (Judge) → A-FORGE (Execute)
                    ↑
              YOU ARE HERE
```

WELL sits between the human and the constitutional kernel. It answers the question: *"Is the human substrate in a state capable of giving reliable consent for the class of decision being proposed?"*

---

## Current Source of Truth

| Field | Value |
|-------|-------|
| Canonical repository | `https://github.com/ariffazil/well` |
| Package version | `1.0.0` |
| Git commit | `v2026.04.29` |
| Framework | FastMCP |
| Entry point | `server.py` |
| State | `/root/well/state.json` |
| Events | `/root/well/events.jsonl` |
| Vault ledger | `/root/well/vault_ledger.jsonl` |

---

## Tool Surface — 31 Prisms Across 4 Layers

### 1. H-WELL (Human Substrate)
Tracks biological telemetry: sleep, stress, clarity, and metabolic state.

| Tool | Purpose |
|------|---------|
| `well_log_state` | Log core biological metrics |
| `well_get_readiness` | Return 0.0–1.0 readiness score with color tiering |
| `well_daily_brief` | Morning pre-session substrate overview |

### 2. M-WELL (Machine Substrate)
Tracks instrument reliability: model health, context pressure, and tool availability.

| Tool | Purpose |
|------|---------|
| `well_machine_state` | Read current technical reliability metrics |
| `well_machine_log` | Log machine telemetry (latency, context use, errors) |

### 3. C-WELL (Coupled Readiness)
Evaluates the interaction risk between Human and Machine.

| Tool | Purpose |
|------|---------|
| `well_coupled_readiness` | Identify risks like "context overload + high fatigue" |
| `well_decision_bandwidth` | Validate if a task (C0–C5) is safe for the current pair |

### 4. FORGE Bridge
Couples WELL to the execution plane.

| Tool | Purpose |
|------|---------|
| `well_forge_precheck` | Handshake before forge to determine safe mode |
| `well_forge_pressure_update` | Signal cognitive load during active forging |

---

## Readiness Tiers

| Tier | Score | Bandwidth | Protocol |
|:-----|:-----:|:---------:|---------|
| 🟢 **GREEN** | ≥ 0.7 | **FULL** | Optimal capacity. All decision classes (C0–C5) open. |
| 🟡 **AMBER** | 0.4–0.69 | **RESTRICTED** | Soft warning. Recommend drafting and reversible tasks. |
| 🔴 **RED** | < 0.4 | **LOCKED** | Hard veto recommendation. Strategic actions suspended. |

---

## Governance Floors (W-Floors)

| Floor | Name | Trigger |
|-------|------|---------|
| **W1** | Sleep Integrity | RED if sleep debt > 2 days |
| **W5** | Cognitive Entropy | RED if clarity < 4/10 |
| **W6** | Metabolic Pause | Enforce 15-min pause if high-frequency intent loops detected |

---

## Constitutional Hierarchy

```
WELL (Informs)  →  arifOS (Judges)  →  A-FORGE (Executes)
      ↑                   ↑                    ↑
   H/M substrate      F1–F13 verdict      Constitutional gate
```

**W0 is non-negotiable:** WELL informs. It never overrides arifOS or the Operator. The chain of authority is invariant under all conditions.

---

## Sibling Organ READMEs

| Organ | One-liner |
|-------|----------|
| [`arifOS`](https://github.com/ariffazil/arifOS) | Constitutional kernel — F1–F13 floors, 13 tools, VAULT999 |
| [`AAA`](https://github.com/ariffazil/AAA) | Identity, A2A federation gateway, and operator control plane |
| [`A-FORGE`](https://github.com/ariffazil/A-FORGE) | Execution shell, orchestration, and operator observability |
| [`GEOX`](https://github.com/ariffazil/geox) | Governed earth intelligence — seismic, petrophysics, basin analysis |
| [`WEALTH`](https://github.com/ariffazil/wealth) | Capital intelligence — NPV, IRR, EMV, crisis triage |

---

## Live Sites

| Surface | URL |
|---------|-----|
| arifOS | https://arifosmcp.arif-fazil.com/ |
| Human | https://arif-fazil.com/ |

*The mirror does not decide. It reflects. Reflection is the prerequisite to judgment.*
*DITEMPA BUKAN DIBERI — Readiness is forged through discipline, not granted by default.*
