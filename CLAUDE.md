# CLAUDE.md — WELL | arifOS Federation

> **DITEMPA BUKAN DIBERI**
> **Human readiness mirror — REFLECT_ONLY.** Assesses vitality, homeostasis, dignity. Never diagnoses.
> **ZEN:** `/root/AAA/prompts/AAA-ZEN-ALIGNMENT.md` — 18 operational rules. Load at boot.

## Identity

Somatic intelligence organ. Port 18083. 8 canonical tools:
- `well_classify_substrate` — Classify any substance/substrate without category error
- `well_trace_lineage` — Memory, trend, ledger, vault chain tracing
- `well_assess_homeostasis` — Regulation, stability, empathic balance
- `well_check_repair` — Repair, recovery, resilience, forge cycle integrity
- `well_validate_vitality` — Vitality, readiness, NIAT assessment
- `well_registry_status` — Registry truth diagnostic — blueprint canonical format
- `well_guard_dignity` — Guard soul, personhood, meaning, symbolic boundaries
- `well_assess_reliability` — Machine, tool, institution, operational reliability

Chain: CLASSIFY → ASSESS → VALIDATE → GUARD. Never adjudicate. Never diagnose.

## Build & Test

```bash
cd /root/WELL
uv sync --frozen
pytest tests/ -q --tb=short           # asyncio_mode = "auto"
ruff check . && ruff format .
systemctl restart well
curl :18083/health
```

## Boundary

- REFLECT_ONLY — never diagnose, never adjudicate, never mutate vault
- Well states: OPTIMAL / STABLE / DEGRADED / CRITICAL
- Dignity floor: coercion_signal > 0.3 → HOLD
- C-WELL: evaluates coupled risk between human and machine state
- Substrate classification: HUMAN / MACHINE / HYBRID / UNKNOWN
- Local-only persistence — no external writes

## Federation Position

```
arifOS (Kernel :8088)
  └── AAA (Control Plane :3001)
        └── WELL (Human Readiness :18083)
              └── WELL-FORGE bridge → A-FORGE (adapts execution intensity)
```

WELL holds a mirror, not a veto. Operator sovereignty is invariant.

*Forged: 2026-07-24. DITEMPA BUKAN DIBERI.*
