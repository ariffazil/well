# WELL — Human Substrate Governance Layer

> **Biological readiness mirror for the arifOS Constitutional Federation.**
> **DITEMPA BUKAN DIBERI — Intelligence is forged, not given.**

[![WELL](https://img.shields.io/badge/WELL-v2026.05.01--KANON-00D4AA?style=flat-square)](https://github.com/ariffazil/well)
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

## Live 32-Tool Surface

WELL exposes **32 MCP tools** in the running container. These are not grouped into families — each is a focused, single-responsibility endpoint. All tools follow the `well_<noun>` or `well_<noun>_<verb>` naming convention.

| Tool | Purpose |
|------|---------|
| `well_anchor` | Request vault anchor — subject to auth and identity invariant pass |
| `well_arifos_packet` | Emit clean, structured context packet for arifOS governance kernel |
| `well_bandwidth_recommendation` | Maps WELL state to operational mode (action translation layer) |
| `well_check_floor` | Check specific W-floor (W1/W5/W6) — return Canonical Verdict |
| `well_check_floors` | Verify W-floor compliance for all active floors |
| `well_consent_status` | Return W0 Sovereignty & Telemetry Consent status |
| `well_coupled_readiness` | C-WELL: Evaluate coupled human-machine readiness |
| `well_daily_brief` | Daily operator dashboard — one consolidated briefing |
| `well_decision_bandwidth` | Combines human + machine state for specific decision class |
| `well_decision_classify` | Classify a task or decision into C0–C5 risk tiers |
| `well_forge_closeout` | A-FORGE sends closure data after forge operation |
| `well_forge_mode_recommend` | Returns current forge mode recommendation for A-FORGE |
| `well_forge_precheck` | A-FORGE asks WELL before forging: safe execution mode? |
| `well_forge_pressure_update` | A-FORGE reports pressure/cognitive load during forging |
| `well_get_readiness` | Return readiness score + W-floor status |
| `well_init` | Initialize WELL session and register identity |
| `well_list_log` | List recent biological state log entries |
| `well_log` | Log a biological telemetry update for operator Arif |
| `well_log_state` | Combined: log telemetry + return updated state |
| `well_machine_log` | Log machine substrate telemetry |
| `well_machine_reliability` | Assess machine substrate reliability for a specific task |
| `well_machine_state` | Read current machine substrate state |
| `well_medical_boundary` | Explicit non-diagnosis guard — WELL does not diagnose |
| `well_niat_check` | Before high-impact action: check intent–biological alignment |
| `well_pressure` | Signal cognitive pressure/load from external source (e.g. A-FORGE) |
| `well_pressure_ledger` | Log or retrieve pressure events by source |
| `well_readiness` | Reflect current biological readiness for arifOS JUDGE context |
| `well_recovery_protocol` | Suggest stabilizing actions based on current WELL state |
| `well_seal_vault` | Seal a WELL event to VAULT999 |
| `well_state` | Get current WELL state — biological telemetry snapshot |
| `well_trend_analysis` | Detect directional trajectory across all WELL metrics |

**Authority grammar:** WELL uses only non-authority verbs: `get`, `check`, `log`, `list`, `reflect`, `suggest`, `classify`, `request`, `recommend`, `update`. It never uses `approve`, `block`, `judge`, `execute`, `command`, `certify`, or `diagnose`.

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
   "registered_tools": 45,
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

## Federation Integration

WELL participates in the arifOS constitutional loop as the **human substrate evidence supplier** (stage 222):

```
Arif (F13) → arif_session_init → arif_sense_observe → arif_evidence_fetch
                                                       ↓
              WELL → well_reflect_readiness  (human readiness tier)
              WEALTH → wealth_reason_npv/irr/emv  (capital intelligence)
              GEOX → geox_evidence_summarize_cross  (earth evidence)
                                                       ↓
                            arif_evidence_fetch → arif_mind_reason → arif_heart_critique → arif_judge_deliberate
                                                                                          ↓
                                                                             SEAL · HOLD · VOID · CAUTION
```

**WELL's role at 222:** `well_reflect_readiness` and `well_get_packet` feed `substrate_readiness` into `arif_evidence_fetch`. If Arif is RED on C4/C5 decisions, 888_JUDGE cannot issue SEAL regardless of capital or earth signal.

**F3 Tri-Witness:** WELL's human readiness tier is the `human` witness leg. WEALTH capital signal is the `ai` witness leg. GEOX earth evidence is the `earth` witness leg. All three required for SEAL.

**C-WELL (Coupled Readiness):** `well_coupled_readiness` evaluates human-machine substrate readiness together. If machine telemetry (`well_machine_state`) has not been logged this session, `coupled_risk` returns `UNKNOWN` — truthful F02 behavior, not a failure.

---

## Source of Truth

| Field | Value |
|-------|-------|
| Canonical repository | `https://github.com/ariffazil/well` |
| Package version | `v2026.05.01-KANON` |
| Framework | FastMCP >= 3.0 |
| Entry point | `server.py` |
| State | `/root/well/state.json` |
| Events | `/root/well/events.jsonl` |
| Vault ledger | `/root/well/vault_ledger.jsonl` |
| Health endpoint | `GET /health` |

---

## arifOS Federation

arifOS is part of a federated AI governance system. Each organ has a narrow responsibility so no single agent becomes uncontrolled, unaccountable, or self-authorizing.

| Organ | Human Meaning | System Role | Docs |
|---|---|---|---|
| **ARIF / APEX** | Final human authority | F13 sovereign veto, approval, override, terminal judgment | [arif-fazil.com](https://arif-fazil.com) |
| **AAA** | Operator cockpit | Identity, A2A federation gateway, session control, agent supervision | [README](https://github.com/ariffazil/AAA) |
| **A-FORGE** | Execution shell | Runs tools, performs dry-runs, executes approved actions, reports outcomes | [README](https://github.com/ariffazil/A-FORGE) |
| **arifOS** | Governance kernel | Checks evidence, risk, authority, verdicts, and auditability before action | [README](https://github.com/ariffazil/arifOS) |
| **GEOX** | Earth intelligence | Seismic, petrophysics, basin, subsurface, and physics-grounded evidence | [README](https://github.com/ariffazil/geox) |
| **WEALTH** | Capital intelligence | NPV, IRR, EMV, risk scoring, crisis triage, economic judgment | [README](https://github.com/ariffazil/wealth) |
| **WELL** | Human readiness mirror | Operator pressure, biological state, cognitive load, human-system safety | — |
| **Ω-Wiki** | Knowledge base | Persistent compiled knowledge, doctrine, references, and memory surfaces | [wiki.arif-fazil.com](https://wiki.arif-fazil.com) |

### How the organs work together

A governed action should not move directly from prompt to execution.

```
Human / Agent request
→ AAA identifies the session
→ arifOS judges the request
→ GEOX / WEALTH / WELL provide domain evidence when needed
→ A-FORGE executes only approved actions
→ VAULT999 records the receipt
→ APEX / Human can veto at any time
```

> **AAA controls the session. arifOS judges. Domain organs provide evidence. A-FORGE executes. VAULT999 records. The human remains sovereign.**

---

## Live Sites

| Surface | URL |
|---------|-----|
| arifOS | https://arifosmcp.arif-fazil.com/ |
| Human | https://arif-fazil.com/ |

---

*The mirror does not decide. It reflects. Reflection is the prerequisite to judgment.*

*DITEMPA BUKAN DIBERI — Readiness is forged through discipline, not granted by default.*
