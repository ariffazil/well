# WELL Tool Surface Registry
> **Canonical Source:** `ariffazil/well`
> **Authority:** WELL organ, governed by `ariffazil/arifOS`
> **Purpose:** Document the live public MCP surface and its invariants
> **Status:** OPERATIONAL | 22 somatic tools

---

## Live MCP Surface

**Production endpoint:** `https://well.arif-fazil.com/mcp`
**Transport:** `streamable-http` (MCP protocol)
**Live tool count:** 22 somatic
**Health endpoint:** `https://well.arif-fazil.com/health`

### Invariant

```
/health tool_count (22) = canonical WELL somatic set (22)
```

This invariant is enforced at startup by `_enforce_somatic_boundary()` in `server.py`. Any `@mcp.tool` not in the canonical somatic set is removed before the server begins accepting connections.

---

## Canonical SOMATIC_TOOLS Set (22)

| # | Tool | Class | Note |
|---|------|-------|------|
| 1 | `well_health_check` | `CANONICAL_PUBLIC` | Canonical health probe. Legacy `mcp_health_check` alias removed 2026-06-28. |
| 2 | `well_classify_substrate` | `CANONICAL_PUBLIC` | Substrate classification and boundary sensing. |
| 3 | `well_trace_lineage` | `CANONICAL_PUBLIC` | Memory, trend, ledger, and vault chain tracing. |
| 4 | `well_detect_boundary` | `CANONICAL_PUBLIC` | Boundary detection across membrane, body, machine, and federation. |
| 5 | `well_measure_gradient` | `CANONICAL_PUBLIC` | Measure chemical, energy, pressure, attention, and compute gradients. |
| 6 | `well_assess_metabolism` | `CANONICAL_PUBLIC` | Assess biological metabolism and system throughput across substrates. |
| 7 | `well_assess_homeostasis` | `CANONICAL_PUBLIC` | Assess regulation, stability, and empathic balance under change. |
| 8 | `well_check_repair` | `CANONICAL_PUBLIC` | Check repair, recovery, resilience, and forge cycle integrity. |
| 9 | `well_validate_vitality` | `CANONICAL_PUBLIC` | Validate vitality, readiness, and NIAT. |
| 10 | `well_assess_livelihood` | `CANONICAL_PUBLIC` | Assess human wellness, role, dignity, support, and meaning. |
| 11 | `well_assess_reliability` | `CANONICAL_PUBLIC` | Assess machine, tool, institution, and operational reliability. |
| 12 | `well_compute_metabolic_flux` | `CANONICAL_PUBLIC` | Compute unified metabolic entropy rate (cognitive + machine). |
| 13 | `well_assess_sovereign_entropy` | `CANONICAL_PUBLIC` | Measure sovereign unpredictability / extraction resistance. |
| 14 | `well_guard_dignity` | `CANONICAL_PUBLIC` | Guard soul, personhood, meaning, and symbolic boundaries. |
| 15 | `well_medical_boundary` | `CANONICAL_PUBLIC` | Explicit non-diagnosis guard with F9 Soul Contract. |
| 16 | `well_13_signal_coverage` | `CANONICAL_PUBLIC` | Audit of 13 canonical signal coverage. |
| 17 | `well_registry_status` | `CANONICAL_PUBLIC` | Registry truth diagnostic (blueprint canonical format). |
| 18 | `well_handoff_dignity_to_arifos` | `CANONICAL_PUBLIC` | S12 → arifOS 888_JUDGE dignity handoff. |
| 19 | `well_handoff_livelihood_to_wealth` | `CANONICAL_PUBLIC` | S13 → WEALTH livelihood handoff. |
| 20 | `well_attest_to_kernel` | `CANONICAL_PUBLIC` | WELL → arifOS organ attest. |
| 21 | `well_classify_state` | `CANONICAL_PUBLIC` | Human state classifier (Phase 1 + Phase 3). |
| 22 | `well_readiness` | `CANONICAL_PUBLIC` | ZEN single verdict — color/score/TTL/action. |

---

## Public MCP Surface (22)

All 22 tools in the canonical somatic set are exposed on the public MCP surface. No diagnostics are stripped at runtime.

---

## Deprecation Notes

- `mcp_health_check` — removed 2026-06-28. Use `well_health_check` or `well_assess_reliability(mode="health")` directly.
- `well_system_registry_status` — deprecated. Use `well_registry_status` (blueprint canonical format).
- No stage aliases (`well_NNN_*`) on the public MCP surface — stripped at startup.
- `well_reflect_intelligence` and `well_anchor_evidence` were removed from the public surface per orthogonal MCP alignment (2026-05-14).

---

## Source Counts

| Metric | Count |
|--------|-------|
| Total `@mcp.tool` decorators in source | 72 |
| Canonical somatic set | 22 |
| Public MCP surface (boundary enforced) | 22 |
| Internal / autonomic helpers and aliases | 50 |

---

## What Is NOT On the Public MCP Surface

The following remain internal-only (no public exposure):

- `well_system_registry_status` — deprecated internal diagnostic
- All `well_NNN_*` stage aliases (000–999) — stripped by somatic boundary
- All legacy helpers not in the canonical somatic set — stripped by somatic boundary

---

## Absorption Log

| Alias | Canonical | Absorbed |
|-------|-----------|----------|
| `well_contrast_report` | `well_state(include="trend")` | ✅ 2026-05-26 |
| `well_fatigue_accumulator(mode="check")` | `well_assess_homeostasis(mode="fatigue")` | ✅ 2026-05-26 |
| `mcp_health_check` | `well_health_check` / `well_assess_reliability(mode="health")` | ✅ 2026-06-28 |

---

*Last Updated: 2026-07-01 | DITEMPA BUKAN DIBERI*
