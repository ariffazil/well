# WELL 888_HOLD Register

> **Last updated:** 2026-06-06 (WELL-13 canon ratified)
> **Status:** ACTIVE — do NOT resolve without human confirmation (F13 SOVEREIGN)
> **Authority:** 888 (Muhammad Arif bin Fazil)
> **Companion to:** `GENESIS/004_WELL_13_CANON.md`

---

## A. BLOCKED DELEGATION CHAINS (mode contract mismatch)

Original aa7b7b5 register (2026-05-26). Status: STILL HELD.

| Tool | Expected Modes | Actual Delegate | Delegate Modes | Gap | Status |
|------|---------------|----------------|----------------|-----|--------|
| well_assess_livelihood | role, meaning, dignity | well_333_mind | human, machine, coupled | Full mismatch — no role/meaning/dignity logic in delegate | HELD |
| well_assess_metabolism | gradient, flux, coupled | well_333_mind | human, machine, coupled | Semantic overlap on "coupled" only — gradient/flux not implemented | HELD |
| well_guard_dignity | consent, boundary, shadow | well_666_heart | critique, empathize, dignity, redteam, maruah | Partial — "dignity" exists but consent/boundary/shadow do not | HELD |

### A.1 NEW HELD ITEM — `well_assess_homeostasis` mode contract

**Forged 2026-06-06:** When `mode="sleep"` (the default), the function fell through
to `well_666_heart(mode="sleep", ...)` which only accepts
`["critique", "empathize", "dignity", "redteam", "maruah"]`. Result: `"error: Unknown
mode: sleep"`. **WAJIB fix being applied this session (mode="sleep" direct
implementation in `well_assess_homeostasis`).** Once verified, mark resolved.

| Tool | Expected Mode | Gap | Status |
|------|---------------|-----|--------|
| well_assess_homeostasis | sleep | Falls through to well_666_heart which doesn't accept it | FIXING (this session) |

---

## B. 8 ADDITIONAL HOLD ITEMS (8 total, classified)

These require explicit 888 before modification:

| Tool | Mode(s) | Reason |
|------|---------|--------|
| well_777_forge | precheck, closeout | Forge cycle integrity — 888_JUDGE domain |
| well_888_judge | deliberate, decide, verdict | 888_JUDGE domain — sovereign veto |
| well_check_repair | check, repair | Pre-JUDGE biological repair assessment |
| well_reflect_intelligence | reflect | Reflection loop — may affect state |
| well_daily_checkin | checkin | Sovereign human interaction |
| well_validate_consensus | validate | Consensus validation |
| well_forge_closeout | closeout | Forge cycle close |
| well_forge_precheck | precheck | Forge preflight |

---

## C. RESOLUTION OPTIONS (requires ARIF approval)

### Option A — Direct Implementation (like fatigue fix)
Write mode logic directly in canonical tool, bypass stage alias delegate.
Pro: Clean, no dependency chain.
Con: Duplicates some stage alias logic.

### Option B — Expand Stage Alias Mode Enums
Add missing modes to well_333_mind and well_666_heart.
Pro: Preserves delegate chain.
Con: Bloats stage aliases that are scheduled for decorator removal in Step 2.

### Option C — Hybrid (RECOMMENDED)
Direct-implement for modes that are constitutionally distinct (consent, boundary,
shadow, role, meaning, gradient, flux).
Let "coupled" and "dignity" delegate where overlap already exists.
Remove stage alias decorators in Step 2 but keep internal functions callable.

---

## D. WELL-13 CANON HOLD (ratified 2026-06-06)

> The following are HELD as binding by F13 SOVEREIGN ratification of
> `GENESIS/004_WELL_13_CANON.md`. They are NOT to be modified without
> issuing a new canon file (e.g. `005_…`).

### D.1 Tier 1 — Vital Substrate (4 signals held)

| # | Signal | Authority | HELD BECAUSE |
|---|--------|-----------|--------------|
| 1 | Heart / circulation | reflect_only | vital signal; can never become coaching |
| 2 | Blood pressure | reflect_only | vital signal; can never become coaching |
| 3 | Breathing / SpO₂ | reflect_only | vital signal; can never become coaching |
| 4 | Temperature / inflammation | reflect_only | vital signal; can never become coaching |

### D.2 Tier 2 — Recovery / Metabolic (3 signals held)

| # | Signal | Authority | HELD BECAUSE |
|---|--------|-----------|--------------|
| 5 | Sleep architecture | reflect_only | one of 13 — must work; mode="sleep" contract fix is WAJIB |
| 6 | Metabolic state | reflect_only | substrate signal — not a body score |
| 7 | Nutrition / hydration | reflect_only | substrate signal — not a diet app |

### D.3 Tier 3 — Function / Cognition (3 signals held)

| # | Signal | Authority | HELD BECAUSE |
|---|--------|-----------|--------------|
| 8 | Movement / strength | reflect_only | MAKRUH to use as nudge; ALLOWED as substrate signal |
| 9 | Pain / injury | reflect_only | substrate signal — not a pain coach |
| 10 | Cognitive clarity | reflect_only | one of 13 — must work; supports decision_class routing |

### D.4 Tier 4 — Dignity / Environment (3 signals held)

| # | Signal | Authority | HELD BECAUSE |
|---|--------|-----------|--------------|
| 11 | Emotional / stress | reflect_only | one of 13 — body/person boundary surface |
| 12 | Social / dignity / consent | reflect_only | PRIMARY surface for objectification/dignity |
| 13 | Environment / livelihood | reflect_only | one of 13 — differentiator from fitness MCP |

---

## E. HARAM ITEMS HELD (must NEVER be forged into WELL)

The following are HELD as **HARAM** in `GENESIS/004_WELL_13_CANON.md` §5.5.
Any future PR, agent, or forge cycle that introduces these is rejected.

| # | HELD ITEM | Reason |
|---|-----------|--------|
| 1 | WELL as wellness coach | Violates purpose boundary |
| 2 | WELL as diagnostic psychiatrist | Sovereign territory, F7 HUMILITY |
| 3 | WELL as morality police | Gay desire / kink / horniness ≠ pathology |
| 4 | WELL issuing final constitutional verdicts | arifOS / 888_JUDGE domain |
| 5 | WELL reducing human to metric | Dignity/meaning are not reducible to biometrics |
| 6 | WELL storing erotic/fetish identity as fixed identity | Stigmatization = haram |
| 7 | WELL making irreversible actions from biometric state | Auto-block / auto-alert = haram without governance |

---

## F. RELIABILITY DEGRADATION HELD (operational issue, not doctrine)

> **WELL-2026-06-06 live health:** `identity_valid=false`,
> `authority_boundary=compromised`, `truth_status=UNVERIFIED`,
> `freshness=stale`. **Do not treat WELL outputs as sovereign truth until
> fixed.** This is a RUNTIME trust issue, not a CONCEPT issue.

| # | Issue | Action |
|---|-------|--------|
| 1 | Identity invariant failing | F13 SOVEREIGN biometric injection required (state.json) |
| 2 | Authority boundary compromised | Server not yet stamping all output with reflect_only |
| 3 | Truth status UNVERIFIED | Evidence chain not yet promoted to VERIFIED |
| 4 | Freshness stale | Auto-sleeper + state.json refresh pending |

These are operational and **DO NOT block** the canon ratification. The canon
is a design statement; the operational fixes are separate work streams.

---

## HOLD VERDICT: 888_HOLD — do not auto-resolve

This register is a **living document**. New items may be added by sovereign
ratification; existing items may only be resolved by explicit F13 approval.
