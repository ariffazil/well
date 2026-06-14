# WELL Tool Surface Registry
> **Canonical Source:** `ariffazil/well`
> **Authority:** WELL organ, governed by `ariffazil/arifOS`
> **Purpose:** Document the live public MCP surface and its invariants
> **Status:** OPERATIONAL | 17 somatic tools

---

## Live MCP Surface

**Production endpoint:** `https://well.arif-fazil.com/mcp`
**Transport:** `streamable-http` (MCP protocol)
**Live tool count:** 17 somatic (15 public MCP + 2 internal diagnostics stripped at runtime)
**Health endpoint:** `https://well.arif-fazil.com/health`

### Invariant

```
/health tool_count (17) = canonical WELL somatic set (17)
```

This invariant is enforced at startup by `_enforce_somatic_boundary()` in `server.py`. Any `@mcp.tool` not in the canonical somatic set is removed before the server begins accepting connections.

---

## Canonical SOMATIC_TOOLS Set (17)

| # | Tool | Class | Note |
|---|------|-------|------|
| 1 | `mcp_health_check` | `DEPRECATED_ALIAS` | Delegates to `well_assess_reliability(mode="health")`. Retained for backward compatibility. |
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
| 16 | `well_system_registry_status` | `INTERNAL_DIAGNOSTIC` | Registry truth diagnostic (stripped from public surface). |
| 17 | `well_registry_status` | `INTERNAL_DIAGNOSTIC` | Internal tool surface audit (stripped from public surface). |

---

## Public MCP Surface (15)

The two `INTERNAL_DIAGNOSTIC` tools above are removed by the somatic boundary, leaving **15 tools** on the public MCP surface.

---

## Deprecation Notes

- `mcp_health_check` — deprecated alias. Use `well_assess_reliability(mode="health")` directly.
- No stage aliases (`well_NNN_*`) on the public MCP surface — stripped at startup.
- `well_reflect_intelligence` and `well_anchor_evidence` were removed from the public surface per orthogonal MCP alignment (2026-05-14).

---

## Source Counts

| Metric | Count |
|--------|-------|
| Total `@mcp.tool` decorators in source | 61 |
| Canonical somatic set | 17 |
| Public MCP surface (boundary enforced) | 15 |
| Internal / autonomic helpers and aliases | 44 |

---

## What Is NOT On the Public MCP Surface

The following remain internal-only (no public exposure):

- `well_system_registry_status` / `well_registry_status` — internal diagnostics
- All `well_NNN_*` stage aliases (000–999) — stripped by somatic boundary
- All legacy helpers not in the canonical somatic set — stripped by somatic boundary

---

## Absorption Log

| Alias | Canonical | Absorbed |
|-------|-----------|----------|
| `well_contrast_report` | `well_state(include="trend")` | ✅ 2026-05-26 |
| `well_fatigue_accumulator(mode="check")` | `well_assess_homeostasis(mode="fatigue")` | ✅ 2026-05-26 |
| `mcp_health_check` | `well_assess_reliability(mode="health")` | ✅ 2026-05-26 |

---

*Last Updated: 2026-06-14 | DITEMPA BUKAN DIBERI*
