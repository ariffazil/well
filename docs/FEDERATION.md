# FEDERATION.md — WELL

```yaml
role: DOMAIN
organ: well
layer: L3
citizenship: warga-aaa
canon: ariffazil/well

depends_on:
  - repo: ariffazil/arifOS
    reason: Evidence routing, governance gates, constitutional compliance
  - repo: ariffazil/A-FORGE
    reason: Execution lease after WELL readiness verdict
  - repo: ariffazil/AAA
    reason: A2A routing, cockpit display, federation topology

mcp:
  port: 18083
  endpoint: https://well.arif-fazil.com/mcp
  tools_count: 10+
  tool_prefix: well_
  public_tools:
    - well_assess_homeostasis (sleep, fatigue, stress)
    - well_assess_reliability (machine, tool, institution)
    - well_check_repair (recovery, resilience)
    - well_classify_substrate (boundary sensing)
    - well_guard_dignity (consent, coercion)
    - well_registry_status
    - well_trace_lineage
    - well_validate_vitality (readiness, NIAT)

governance:
  judge: arifOS
  seal: VAULT999
  floors: F1-F13
  doctrine: REFLECT_ONLY
  mutation_rule: NEVER mutate. NEVER diagnose. Reflect only. arifOS judges.

stack_role: |
  WELL is the vitality guard organ — L3 DOMAIN.
  It monitors human readiness: sleep, fatigue, stress, dignity, consent.
  It is REFLECT_ONLY — it reflects state, never diagnoses, never adjudicates.
  It protects Arif's sovereignty over his own body and attention.
  WELL sees. arifOS judges. Arif decides.
```

## Federation Cross-Links

### arifOS (`/root/arifOS`, :8088)
- **Contract:** [`WELL_ARIFOS_CONTRACT.md`](./WELL_ARIFOS_CONTRACT.md) — canonical cross-repo agreement
- **Flow:** WELL emits `well_arifos_packet` → arifOS `_222_witness.py` parses → constitutional gates
- **Judgment:** WELL reflects; arifOS `arif_judge` issues SEAL/HOLD/SABAR/VOID
- **Floors:** arifOS enforces F1-F13; WELL contributes G-WELL governance health signals

### AAA (`/root/AAA`, :3001)
- **A2A:** WELL routes readiness signals to AAA for cockpit display
- **Routing:** AAA `arif_route` dispatches cross-organ queries
- **Topology:** AAA maintains canonical federation map at `docs/FEDERATION_MAP.md`

### A-FORGE (`/root/A-FORGE`, :7071)
- **Execution:** After WELL readiness verdict + arifOS SEAL, A-FORGE executes
- **WELL–FORGE bridge:** A-FORGE queries `well_assess_homeostasis` for decision-class gating
- **C-class matrix:** C1/C2 → proceed unless CRITICAL; C3 → STABLE+; C4 → OPTIMAL; C5 → OPTIMAL + no chronic fatigue

### Domain Organs
- **GEOX (:8081):** Receives decision-class gate from `geox_well_decision_class`
- **WEALTH (:18082):** Consumes readiness state for capital-intelligence risk calibration

## Federation Position

```
arifOS (Ω Law) → WELL (Vitality) → AAA (Routing/Display) → arifOS 888_JUDGE (Verdict) → A-FORGE (Execution) → VAULT999 (Seal)
```

WELL is a **biological witness**, not a judge. It reports readiness scores, metabolic flux, and dignity preservation metrics. The verdict remains with arifOS.

---

**DITEMPA BUKAN DIBERI — Forged, Not Given.**
**Part of the arifOS Federation. See `/root/AAA/docs/FEDERATION_MAP.md` for canonical topology.**
