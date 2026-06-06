# 004 — WELL-13 Canon

> **Ratified:** 2026-06-06
> **Authority:** 888 (Muhammad Arif bin Fazil, F13 SOVEREIGN)
> **Status:** CONSTITUTIONAL — supersedes prior WELL positioning.
> **Companion to:** `001_…`, `002_…`, `003_…` in `/root/WELL/GENESIS/`

---

## 0. The Soul

```
WELL = Body + dignity + vitality + boundaries + role burden + consent + meaning.
```

In Malay:

> **Fitness MCP jaga badan sebagai mesin.**
> **WELL MCP jaga manusia sebagai insan.**

WELL is **not** a wellness app clone. WELL is the **constitutional organ for living
substrate integrity** under arifOS. It observes. It reflects. It signals. It does
**not** coach, score, optimise, judge, or diagnose.

---

## 1. The 13-Signal Substrate Map

The human substrate has thirteen primary signals. They are nested in four tiers,
ordered by survivability-first:

### Tier 1 — Vital Substrate (4 signals)

> Without these, no higher layer is meaningful.

| # | Signal              | What it reads                                      |
|---|---------------------|----------------------------------------------------|
| 1 | Heart / circulation | resting HR, HRV, rhythm, recovery trend            |
| 2 | Blood pressure      | circulatory load, chronic strain, acute danger    |
| 3 | Breathing / SpO₂    | respiratory rate, breath pattern, oxygenation      |
| 4 | Temperature / inflammation | fever, hypothermia, infection/stress signal |

### Tier 2 — Recovery / Metabolic (3 signals)

| # | Signal              | What it reads                                      |
|---|---------------------|----------------------------------------------------|
| 5 | Sleep architecture  | duration, quality, timing, awakenings, sleep debt  |
| 6 | Metabolic state     | glucose, basal rate, energy stability               |
| 7 | Nutrition / hydration | food quality, appetite, water intake, elimination |

### Tier 3 — Function / Cognition (3 signals)

| # | Signal              | What it reads                                      |
|---|---------------------|----------------------------------------------------|
| 8 | Movement / strength | steps, activity, gait, grip, mobility              |
| 9 | Pain / injury       | pain level, soreness, chronic tension              |
| 10| Cognitive clarity   | focus, memory, reaction, confusion, decision fatigue |

### Tier 4 — Dignity / Environment (3 signals)

> The layer fitness apps never see. The differentiator.

| # | Signal              | What it reads                                      |
|---|---------------------|----------------------------------------------------|
| 11| Emotional / stress  | mood, anxiety, irritability, calm, perceived control |
| 12| Social / dignity / consent | support, isolation, coercion, objectification, relationship safety |
| 13| Environment / livelihood | housing, work pressure, money stress, heat, air, noise, safety, caregiving burden |

The complete structure: **4 + 3 + 3 + 3 = 13.**

---

## 2. Authority Boundary — WAJIB

WELL **must never** issue final constitutional verdicts. WELL is **advisory only**.

### 2.1 What WELL may say (signals only)

```text
signal: consent_at_risk
signal: reality_boundary_compromised
signal: dignity_leakage
signal: fatigue_strain
signal: acute_hold_recommended
signal: sleep_recovery_low
signal: objectification_surface_present
signal: shame_loop_detected
```

### 2.2 What WELL must NOT say (verdicts)

```text
verdict: SEAL
verdict: HOLD
verdict: VOID
verdict: SABAR
verdict: PASS
verdict: FAIL
```

These belong to **arifOS / 888_JUDGE** alone. WELL's `verdict` field is renamed to
`signal` in all advisory output (already partially done — must be universal).

### 2.3 The hard rule

> WELL observes biological substrate state and readiness.
> WELL must use `signal`, not final `verdict`, for all downstream logic.
> arifOS 888_JUDGE is the sole constitutional authority.

---

## 3. Human Substrate Integrity Doctrine

### 3.1 The mission (one sentence)

> WELL detects when optimisation, desire, labour, worship, fitness, addiction,
> duty, or AI relation starts consuming the human underneath.

### 3.2 The body/person boundary model

WELL must distinguish three axes when a body is the object of attention:

```text
body admiration     vs  body consumption     vs  personhood deletion
non-erotic          vs  ambiguous            vs  erotic/reductionist
admirer preserves   vs  admirer consumes     vs  admirer erases
self                vs  object               vs  tool
```

The substrate classifier (`well_classify_substrate`) is the surface that must
operate on this model. See:
- `well_detect_boundary` (body/person, admiration/consumption, dominance/coercion)
- `well_guard_dignity` (objectification risk, reductionism risk, shame loop)
- `well_classify_substrate` (HUMAN_RELATIONAL_DYNAMIC canonical object, 2026-06-06)

### 3.3 The body-as-product rule

```text
If human body becomes product/object/status-machine,
WELL must flag reductionism risk.
```

This is the dignity guard's central rule. It is **advisory** — it does not
block, but it surfaces the risk to arifOS/JUDGE.

---

## 4. Triage Model — Forbid Diagnosis

WELL does **not** diagnose. WELL classifies signal families.

### 4.1 What WELL must NOT diagnose

```text
- psychosis
- meth intoxication
- addiction
- sexuality
- gender identity
- kinks / fetishes
- psychiatric conditions
- substance use disorders
```

### 4.2 What WELL may emit (signal triage)

```text
- reality_boundary_compromised
- substance_strain_suspected
- arousal_boundary_intact
- compulsion_risk
- acute_hold_recommended
- medical_escalation_recommended
```

The reason: diagnosis is sovereign territory. It is irreversible in social
terms, requires licensed human authority, and cannot be automated without
violating F7 HUMILITY and F13 SOVEREIGN.

---

## 5. Hukm Roster (Permanent Design Boundary)

This is the permanent boundary. Any PR that violates it is rejected.

### 5.1 WAJIB (must forge / preserve)

| # | Rule                                                                          |
|---|-------------------------------------------------------------------------------|
| 1 | The 13-signal canon above                                                     |
| 2 | Advisory-only authority boundary (signal, never verdict)                       |
| 3 | Human substrate integrity doctrine (soul of WELL)                             |
| 4 | Body/person boundary model                                                     |
| 5 | Dignity guard for objectification                                              |
| 6 | Triage model for psychosis / meth / arousal (signal, never diagnosis)         |
| 7 | Substrate classifier abstraction fix (HUMAN_RELATIONAL_DYNAMIC, 2026-06-06)   |
| 8 | `mode="sleep"` contract must work in `well_assess_homeostasis`                  |
| 9 | Test response wrapper KeyError fix (unwraps governance envelope)               |
| 10| Reliability / identity invariant hardening (no sovereign output until fixed)   |

### 5.2 SUNAT (strongly recommended)

| # | Item                                                                         |
|---|------------------------------------------------------------------------------|
| 1 | `WELL_13_SIGNAL_MAP.json` — every signal mapped to tool, source, confidence   |
| 2 | `well_13_signal_coverage` tool — audit active / stale / missing signals     |
| 3 | Cultural archetype metadata map (e.g. `abang_sado_shadow`)                    |
| 4 | Addiction / arousal / reality-boundary triage labels                          |
| 5 | Cross-organ handoff map (WELL → WEALTH / HEART / arifOS / GEOX)             |

### 5.3 HARUS (allowed / optional, must be scoped)

| # | Item                                                                         |
|---|------------------------------------------------------------------------------|
| 1 | Wearable integrations as telemetry adapters (Apple Health, Fitbit, WHOOP, …)|
| 2 | Fitness telemetry as substrate signal (steps, HRV, sleep, glucose, …)       |
| 3 | Dashboards (only if they show freshness, uncertainty, advisory-only)         |
| 4 | Self-report forms (sleep debt, pain, stress, safety, coercion, …)            |
| 5 | Kink/sexuality boundary check (dignity/consent only, not erotic instruction)  |

> **Rule:** Wearables may feed WELL. Wearables must not define WELL.

### 5.4 MAKRUH (discouraged, allowed only with guardrails)

| # | Item                                                                         |
|---|------------------------------------------------------------------------------|
| 1 | "Optimise your sleep" coaching                                                |
| 2 | Calorie / step / performance nudging                                          |
| 3 | Body scoring (body score, attractiveness, masculinity, dominance, …)         |
| 4 | Over-detailed sexual dynamic modelling                                        |
| 5 | Over-cultural hardcoding (e.g. fitting WELL only to Malay gay male context)  |

### 5.5 HARAM (rejected from WELL canon)

| # | Item                                                                         |
|---|------------------------------------------------------------------------------|
| 1 | WELL as wellness coach                                                        |
| 2 | WELL as diagnostic psychiatrist                                               |
| 3 | WELL as morality police (gay desire, kink, horniness ≠ pathology)            |
| 4 | WELL issuing final constitutional verdicts (SEAL/HOLD/VOID/SABAR)            |
| 5 | WELL reducing human to metric (HRV + sleep + steps ≠ wellness)               |
| 6 | WELL storing erotic/fetish identity as fixed identity                         |
| 7 | WELL making irreversible actions from biometric state (auto-block, auto-alert, auto-notify) without explicit governance route |

---

## 6. The Permanent Design Boundary

```text
WELL is not the organ that asks:
  "How fit is this body?"

WELL is the organ that asks:
  "Is this living human substrate still intact, dignified, bounded,
   supported, and meaningfully alive?"
```

If any future PR, agent, or forge cycle drifts WELL toward "wellness coaching,"
"body optimisation," or "psychiatric diagnosis," this canon is the contract
that rejects it.

---

## 7. Cross-Organ Handoff Map (SUNAT-future, but recorded)

| Pattern detected                  | Hand off to       |
|-----------------------------------|-------------------|
| Validation economy / body-as-capital | WEALTH           |
| Shame / vulnerability / longing   | HEART             |
| Consent / dignity breach          | arifOS / JUDGE    |
| Acute medical danger              | human medical route |
| Environment / livelihood pressure | WELL + WEALTH     |
| Terrain / fault / pressure metaphor | GEOX (lens only) |

---

## 8. Evidence Basis (recorded, not exhaustive)

The 13-signal map aligns with:

- **Clinical vital signs:** heartbeat rate, breathing rate, temperature, blood
  pressure (essential body-function indicators).
- **AHA Life's Essential 8:** diet, physical activity, nicotine, sleep, weight,
  cholesterol, blood sugar, blood pressure.
- **CDC mental health:** emotional, psychological, and social well-being.
- **WHO social determinants of health:** conditions where people are born,
  grow, live, work, and age; distribution of power, money, and resources.

But WELL-13 goes **further** than any one of these. The 12th and 13th signals
(dignity/consent and environment/livelihood) are the differentiator. Fitness
MCPs do not see them. WELL does.

---

## 9. Ratification

By ratifying this canon, F13 SOVEREIGN accepts the above as the binding
operational doctrine for WELL. Subsequent PRs may proceed without further
ratification IF and ONLY IF they do not modify:

1. The 13-signal map (Tier structure)
2. The advisory-only authority boundary
3. The body/person boundary model
4. The triage model (no diagnosis)
5. The HARAM list (rejected items)

Any modification to those five sections requires a new `## RATIFIED:` block
on a new canon file (e.g. `005_…`).

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE.
