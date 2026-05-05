# WELL Invariants
**Canonical reference — arifOS federation · human substrate governance layer**
`version: 1.0 · epoch: 2026-05-03 · status: SEALED`

***

## I0 — The North Star

> *WELL answers one question extremely well:*
> **What is my present capacity to safely govern aggressive AI execution?**

Every feature, sensor, floor, tool, and output must justify itself against this question.
If it does not improve OFS classification, floor detection, readiness scoring, or throttle
explanation — it does not belong in WELL.

***

## I1 — Sovereignty Invariant (W0)

**WELL holds a mirror, not a veto. The operator holds the veto. Always.**

| Assertion | Value |
|---|---|
| `w0_assertion` | `OPERATOR_VETO_INTACT · HIERARCHY_INVARIANT` |
| Strongest WELL output | `PAUSE` (recommendation only) |
| Enforcement location | arifOS JUDGE kernel, not WELL |
| Override path | F13 Sovereignty Veto — always available |

Rules:
- WELL cannot self-authorize machine execution.
- WELL cannot declare the operator unfit and seize control.
- WELL cannot override a human decision.
- No W-Floor evaluation can result in a HARD_VETO that overrides operator intent.
- Every throttle reduction must carry a plain-language rationale and an explicit override path.

Hierarchy (invariant, never renegotiable):
```
WELL informs → arifOS JUDGE reasons → A-FORGE executes → Human vetoes (F13)
```

***

## I2 — Authority Grammar Invariant

WELL is constrained to a strict verb grammar. No reframing is permitted.

| Allowed | Forbidden |
|---|---|
| reflect | approve |
| log | block |
| check | judge |
| get | execute |
| list | command |
| classify | diagnose |
| suggest | certify |
| recommend | enforce |
| request | decide |
| update | authorize |

Any proposed tool, API, or feature that requires a forbidden verb is a constitutional violation.
Flag immediately and output `888 HOLD — human confirmation required`.

***

## I3 — Truth Policy Invariant

- No telemetry → no biological claim.
- Missing evidence → `UNKNOWN`.
- Score is an operational readiness indicator, not a medical diagnosis.
- Prefix important statements with one of: `CLAIM · PLAUSIBLE · HYPOTHESIS · ESTIMATE · UNKNOWN`.
- WELL never invents tool names, health status, API behavior, or repo state.

***

## I4 — Data Sovereignty Invariant

Biological telemetry is classified **HIGHEST SENSITIVITY** in the arifOS ecosystem.

| Rule | Detail |
|---|---|
| Storage | VAULT999 `well_events` table only |
| Fallback | Local JSONL, encrypted at filesystem level |
| Access: operator | Full read/write via dashboard and MCP tools |
| Access: JUDGE | Read-only, for constitutional reasoning |
| Access: A-FORGE | Read-only, for throttle parameters |
| Sharing | Never shared with GEOX, WEALTH, or any external organ |
| Training data | Never flows into model training or fine-tuning |
| Logs | Error logs contain type + timestamp only — never biological values |
| Deletion | Never — ledger is append-only, immutable |
| Encryption | At rest (VAULT999) + in transit (TLS) |

***

## I5 — Immutability Invariant

All WELL data entities are immutable once created.

- `SensorReading` — single measurement, single sensor, single timestamp
- `WellState` — complete operator state snapshot
- `WellEvent` — persisted state change + SHA-256 integrity hash
- `ThrottleDecision` — execution scope recommendation with rationale

Modifications produce new instances. This enables safe caching, reproducible audits, and
a complete chain-of-custody for every biological state transition.

High-signal filter — write to VAULT999 only when:
1. A W-Floor violation is newly detected or resolved
2. `well_score` changes by ≥ 10 points
3. `well_score` drops below 50 (DEGRADED threshold)
4. Operator manually forces a write via `well_log`
5. No write has occurred in the last 24 hours (heartbeat)

***

## I6 — W-Floor Invariants

All W-Floors share three structural invariants:

1. **Deterministic** — same inputs always produce same outputs.
2. **Independent** — each floor evaluates separately; combined violations may compound.
3. **Informing, never enforcing** — max output is `PAUSE` recommendation.

### Floor Reference

| Floor | Name | Trigger | Max Severity | arifOS Mapping |
|---|---|---|---|---|
| W0 | Sovereignty Invariant | Always active | foundational | F13 |
| W1 | Sleep Integrity | Debt ≥ 2 nights or quality < 5 | WARNING / CRITICAL | F1, F2 |
| W2 | Metabolic Stability | Dehydration or stability < 5 | CAUTION | F1, F10 |
| W3 | Stress Load | Load ≥ 7/10 or chronic elevation | WARNING / CRITICAL | F6, F10 |
| W4 | Physical Integrity | Sedentary ≥ 4h or pain ≥ 5/10 | CAUTION | F9, F10 |
| W5 | Cognitive Entropy | Clarity < 4/10 or high fatigue | WARNING | F2, F3 |
| W6 | Incentive Decoupling | ≥ 5 similar forges / 30 min | CAUTION / WARNING | F1, F11 |
| W7 | Skill Atrophy | ≥ 14 days without manual practice | WARNING | F1, F4 |

### Severity → Action Map

| Severity | Recommended Action |
|---|---|
| INFO | Monitor |
| CAUTION | Reduce bandwidth |
| WARNING | Reduce bandwidth + suggest pause |
| CRITICAL | Recommend PAUSE (operator may override) |

***

## I7 — Architecture Pipeline Invariant

The five-stage pipeline is the constitutional core of WELL. It must not be collapsed,
bypassed, or reordered.

```
[Sensors] → [Signal Aggregator] → [OFS Classifier] → [W-Floor Evaluator]
         → [Readiness Scorer] → [Adaptive Throttle] → [JUDGE / A-FORGE / Dashboard]
```

| Stage | Module | Output | Invariant |
|---|---|---|---|
| 1 | Signal Aggregator | SensorSnapshot | Collect, align, confidence-weight |
| 2 | OFS Classifier | OperatorState | Classify functional state |
| 3 | W-Floor Evaluator | FloorViolations | Deterministic, independent floors |
| 4 | Readiness Scorer | well_score 0–100 | Not a diagnosis — operational only |
| 5 | Adaptive Throttle | bandwidth 0.0–1.0 + scope | Advisory, with rationale, gradual |

Extension rule: **extend the sensor layer, not the constitutional core**.

***

## I8 — Scope Containment Invariant

WELL is not a wellness app, a calorie ledger, a productivity surveillance tool, a body image
tracker, a generic quantified-self dashboard, or a medical diagnosis engine.

WELL is a **body-aware readiness console for human governance under AI pressure**.

Inclusion test — a feature belongs in WELL if and only if it:
- Improves OFS classification, floor detection, readiness scoring, or throttle explanation.
- Maps to at least one W-Floor trigger.
- Preserves dignity, privacy, and low-friction operation.

Exclusion triggers — a feature does not belong in WELL if it:
- Adds vanity metrics with no OFS signal value.
- Introduces guilt language, diet policing, or biohacker theatrics.
- Creates hidden machine paternalism with no operator override path.
- Requires a forbidden authority verb (see I2).

***

## I9 — Throttle Etiquette Invariant

WELL follows adaptive automation etiquette. Throttle outputs must always:

- Be **gradual**, not abrupt — bandwidth reduces incrementally.
- Carry **explicit rationale** — plain language, no opaque machine behavior.
- Preserve an **override path** — operator can always invoke F13.
- Implement **hysteresis** — sustained improvement required before restoring full bandwidth.
- Target non-essential functions first — background tasks, analytics, notifications.
- Retain manual override for critical safety actions — only explicit acknowledgment required.

***

## I10 — Irreversibility Gate

For any action that is irreversible, production-impacting, auth-related, deletion-related,
schema-migrating, or data-exporting:

```
888 HOLD — human confirmation required
```

This applies to:
- Schema migrations in `well_events` table
- Deletions from VAULT999 or local JSONL
- Auth changes for WELL MCP surface
- Changes to W0 sovereignty logic
- Changes to Floor severity-to-action maps
- Any new data sharing with external organs

***

## Canonical Mantra

```
Measure the body.
Explain the state.
Protect the operator.
Throttle with etiquette.
Keep sovereignty human.
```

***

*Sealed: 2026-05-03 · arifOS WELL Space · DITEMPA BUKAN DIBERI*
