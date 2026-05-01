# WELL — Human Substrate Governance Layer

> **Biological readiness mirror for the arifOS Constitutional Federation.**
> **DITEMPA BUKAN DIBERI — Intelligence is forged, not given.**

[![WELL](https://img.shields.io/badge/WELL-v1.1.0-00D4AA?style=flat-square)](https://github.com/ariffazil/well)
[![MCP](https://img.shields.io/badge/MCP-FastMCP-7C3AED?style=flat-square)](https://github.com/ariffazil/well)
[![arifOS](https://img.shields.io/badge/arifOS-F1%E2%80%93F13_Governed-FF6B00?style=flat-square)](https://github.com/ariffazil/arifOS)
[![License](https://img.shields.io/badge/License-AGPL_V3-4EAF0C?style=flat-square)](./LICENSE)

---

## What WELL Is

WELL is the **Human–Machine Substrate Governance Layer** for arifOS. It provides high-signal biological and technical readiness telemetry to ensure that intent is verified before it is forged into action.

WELL is the **mirror** — it reflects the state of the human and machine substrate so arifOS can judge whether the current configuration is safe for the decision class at hand. It does not veto. It informs.

> **W0 Sovereignty Invariant:** WELL holds a mirror, not a veto. It informs the arifOS JUDGE, but the Operator (Arif) retains final authority. Hierarchy is invariant.

---

## Position in the arifOS Trinity

```
Operator (Arif) → WELL (Mirror) → arifOS (Judge) → A-FORGE (Execute)
                    ↑
              YOU ARE HERE
```

WELL sits between the human and the constitutional kernel. It answers the question: *"Is the human substrate in a state capable of giving reliable consent for the class of decision being proposed?"*

**Authority flow:**
```
WELL informs  →  arifOS judges  →  A-FORGE executes  →  VAULT999 remembers
     ↑                ↑                  ↑                    ↑
  H/M substrate   F1–F13 floors    Constitutional gate   Immutable ledger
```

---

## Canonical 13-Tool Surface

WELL speaks `well_verb_noun`. Domain lives in schema, not tool sprawl.

| # | Tool | Verb | Purpose |
|---|------|------|---------|
| 1 | `well_get_health` | get | Three-layer health seal (service / instrument / domain-truth) |
| 2 | `well_get_state` | get | Retrieve current state with evidence status |
| 3 | `well_check_invariant` | check | Verify WELL identity, W-floors, and constitutional bounds |
| 4 | `well_log_signal` | log | Plastic evidence logger — human, machine, forge, or session |
| 5 | `well_list_events` | list | List recent events with optional redaction |
| 6 | `well_reflect_trend` | reflect | Reflect trajectory over time — no authority claimed |
| 7 | `well_reflect_readiness` | reflect | Reflect readiness — human, machine, or coupled |
| 8 | `well_suggest_mode` | suggest | Suggest operating mode — never decides |
| 9 | `well_suggest_recovery` | suggest | Suggest stabilizing actions — not medical advice |
| 10 | `well_reflect_niat` | reflect | Reflect intent clarity, reversibility, and alignment |
| 11 | `well_classify_task` | classify | Classify task into C0–C5 risk tiers |
| 12 | `well_get_packet` | get | Emit context packet for arifOS, A-FORGE, or dashboard |
| 13 | `well_request_anchor` | request | Request vault anchor — subject to auth and invariant pass |

**Grammar rule:** WELL uses only calm, non-authority verbs: `get`, `check`, `log`, `list`, `reflect`, `suggest`, `classify`, `request`. It never uses `approve`, `block`, `judge`, `execute`, `command`, `diagnose`, or `certify`.

**Legacy compatibility:** 31 legacy tools remain as backward-compatible wrappers. New integrations should prefer the canonical 13.

---

## Identity Invariant

WELL must prove it is WELL before its readings are trusted.

```python
def is_well(state):
    return (
        state.get("identity") == "WELL"
        and state.get("role") in ["Body", "Body / Human Intelligence", "Biological Substrate Governance"]
        and state.get("delta_s", -1) >= 0
        and state.get("peace2", 0) >= 1.0
        and state.get("kappa_r", 0) >= 0.95
        and state.get("rasa") is True
        and state.get("amanah") in ["LOCK", "🔐", True]
        and state.get("authority") == "REFLECT_ONLY"
    )
```

If any field is corrupted or missing, WELL returns `NOT_WELL` and refuses to make biological claims.

---

## Three-Layer Health Model

`well_get_health` returns a governed instrument health check — not just a process ping.

### Layer 1 — Service
```json
{ "alive": true, "transport": "SSE_VALID" }
```

### Layer 2 — Instrument
```json
{
  "identity_valid": true,
  "schema_valid": true,
  "dependencies_ok": true,
  "tool_surface_valid": true,
  "registered_tools": 13,
  "canonical_tools": 13,
  "authority_boundary": "intact",
  "mutation_guard": "locked"
}
```

### Layer 3 — Domain Truth
```json
{
  "has_telemetry": true,
  "truth_status": "VERIFIED",
  "freshness": "fresh",
  "state_age_hours": 0.0
}
```

### Verdict
| Verdict | Meaning |
|---------|---------|
| **PASS** | Identity intact, instrument healthy, domain evidence fresh |
| **WARN** | Dependency broken, surface compromised, telemetry stale/unknown |
| **FAIL** | Identity invariant failed — organ may be corrupted or impersonated |

---

## Truth Policy

WELL does not fake biological knowledge.

| Condition | WELL Response |
|-----------|---------------|
| Metrics present + `truth_status: VERIFIED` | Normal computed readiness (GREEN/AMBER/RED) |
| Metrics empty or `truth_status: UNVERIFIED` | `readiness: UNKNOWN`, `recommended_mode: draft_only` |
| Metrics expired (>24h) | `freshness: expired`, `verdict: WARN` |
| Identity invariant failed | `verdict: NOT_WELL`, all biological claims withheld |

**The rule:** *No telemetry, no biological claim.*

---

## Readiness Tiers

| Tier | Score | Bandwidth | Protocol |
|:-----|:-----:|:---------:|---------|
| 🟢 **GREEN** | ≥ 0.7 | **FULL** | Optimal capacity. All decision classes (C0–C5) open. |
| 🟡 **AMBER** | 0.4–0.69 | **RESTRICTED** | Soft warning. Recommend drafting and reversible tasks. |
| 🔴 **RED** | < 0.4 | **PAUSED** | Hard veto recommendation. Strategic actions suspended. |
| ⚪ **UNKNOWN** | N/A | **DRAFT_ONLY** | No verified telemetry. WELL cannot infer biological readiness. |

---

## Governance Floors (W-Floors)

| Floor | Name | Trigger |
|-------|------|---------|
| **W0** | Sovereignty Invariant | WELL identity must be intact; authority must be REFLECT_ONLY |
| **W1** | Sleep Integrity | RED if sleep debt > 2 days |
| **W5** | Cognitive Entropy | RED if clarity < 4/10 |
| **W6** | Metabolic Pause | Enforce 15-min pause if high-frequency intent loops detected |
| **W7** | Cognitive Overload | PAUSED if fatigue > 7 and clarity < 5 |

---

## Decision Classes (C-Axis)

| Class | Type | Risk | Req. Score | Human Reconfirmation |
| :--- | :--- | :--- | :--- | :--- |
| **C0** | Reflection / Notes | Zero | 0.0 | No |
| **C1** | Drafting / Organizing | Low | 0.4 | No |
| **C2** | Coding / Testing | Med | 0.55 | Yes (if Amber) |
| **C3** | Public Posting / Replies | Med-High | 0.65 | Yes |
| **C4** | Financial / Legal / Architecture | High | 0.75 | Yes (Absolute) |
| **C5** | Irreversible / Schema Migration | Critical | 0.85 | Yes (Dual-Witness) |

---

## Source of Truth

| Field | Value |
|-------|-------|
| Canonical repository | `https://github.com/ariffazil/well` |
| Package version | `1.1.0` |
| Framework | FastMCP >= 3.0 |
| Entry point | `server.py` |
| State | `/root/well/state.json` |
| Events | `/root/well/events.jsonl` |
| Vault ledger | `/root/well/vault_ledger.jsonl` |
| Health endpoint | `GET /health` |

---

## Sibling Organs

| Organ | Role |
|-------|------|
| [`arifOS`](https://github.com/ariffazil/arifOS) | Constitutional kernel — F1–F13 floors, 13 canonical tools, VAULT999 |
| [`A-FORGE`](https://github.com/ariffazil/A-FORGE) | Execution shell — orchestration, metabolic execution, operator observability |
| [`GEOX`](https://github.com/ariffazil/geox) | Earth intelligence — seismic, petrophysics, basin analysis |
| [`WEALTH`](https://github.com/ariffazil/wealth) | Capital intelligence — NPV, IRR, EMV, crisis triage |
| [`AAA`](https://github.com/ariffazil/AAA) | Identity, A2A federation gateway, and operator control plane |

---

## Live Sites

| Surface | URL |
|---------|-----|
| arifOS | https://arifosmcp.arif-fazil.com/ |
| Human | https://arif-fazil.com/ |

---

*The mirror does not decide. It reflects. Reflection is the prerequisite to judgment.*

*DITEMPA BUKAN DIBERI — Readiness is forged through discipline, not granted by default.*
