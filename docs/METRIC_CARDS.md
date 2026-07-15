# WELL Metric Cards — Evidence vs Metaphor

**Rule:** Scientific-sounding names need auditable definitions.  
Validation status: `METAPHOR` | `OPERATIONAL` | `VALIDATED`.

---

### readiness / well_score (0–100)

| Field | Value |
|-------|--------|
| **inputs** | state.json well_score, TTL, optional gate ranks |
| **units** | dimensionless 0–100 or null |
| **baseline** | operator self-report or sensor inject |
| **confidence** | 0.4 self-report · 0.8+ sensor (when present) |
| **freshness** | TTL bands 12h/24h/48h |
| **threshold** | ≥75 GREEN · 50–74 YELLOW · <50 RED · stale→STALE |
| **limitations** | Not clinical; not mood diagnosis |
| **validation_status** | OPERATIONAL |

---

### metabolic_flux (0–1)

| Field | Value |
|-------|--------|
| **inputs** | cognitive load indicators + machine entropy proxies |
| **meaning** | Combined *strain indicator*, not physical thermodynamics |
| **threshold** | ≥0.65 reallocation signal · ≥0.85 system_hold *advisory* |
| **validation_status** | METAPHOR → OPERATIONAL (heuristic) |

**Do not claim:** “Landauer / thermodynamic proof Arif is unwell.”

---

### sovereignty_entropy / sovereign-entropy

| Field | Value |
|-------|--------|
| **intent** | Protect against behavioural fingerprinting & compliance optimisation |
| **measurable proxies** | model-dependence, profiling exposure, prediction confidence, data concentration, manipulation risk, choice diversity |
| **validation_status** | METAPHOR (governance construct) |

Rename in prose: **profiling / compliance-optimisation risk**.

---

### H/M/G/C substrate ranks

| Field | Value |
|-------|--------|
| **inputs** | vitality_gate assessors + machine sensor + VPS probe |
| **units** | ordinal ranks 0–4 + state enums |
| **validation_status** | OPERATIONAL |

---

### A_effective = A×E×R×G×S

| Field | Value |
|-------|--------|
| **inputs** | granted class, evidence_quality, rollback, gov state, fitness |
| **validation_status** | OPERATIONAL (policy formula) |

---

*Update this file when any formula changes.*
