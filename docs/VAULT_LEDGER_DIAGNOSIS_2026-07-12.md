# VAULT / Cooling Ledger Diagnosis — 2026-07-12

## Observations (T1)

| Signal | Result |
|--------|--------|
| `seal_chain.js length` | 52 |
| `seal_chain.js verify` | **FAIL** — `prev_hash mismatch` (expected ≠ actual at break) |
| Conformance spine (prior audit) | 9/9 GREEN with cooling_ledger DEGRADED / UNKNOWN |
| Sovereign historical gaps | Pre-May-2026 migration gaps ruled **non-issue** (AGENTS.md) |

## Named causes (ranked)

1. **Dual / desynced writers** — head was repaired earlier (seq 18 vs actual 50); later appends may not share the same prev_hash lineage as older verify walk.  
2. **Optional cooling ledger ≠ constitutional seal chain** — Supabase/cooling_queue analytical path can report DEGRADED while seal_chain replay of *tested* windows still passes.  
3. **Self-report actor seals** — recent writes downgraded SEAL→HOLD (INV actor_verified); not the same as hash break.

## Policy (binding — also in MEASUREMENT_BOUNDARY_CONTRACT)

| Condition | Action |
|-----------|--------|
| **Current** constitutional chain cannot verify *new* append integrity | HOLD mutations that require VAULT SEAL |
| Historical gap only (ids 18–60 era / migration) | WARN; observe OK |
| Cooling / analytical ledger degraded | WARN; analytics read-only; **do not** invent GREEN chain_ok |
| Chain verify FAIL on whole file | **Do not** “fix” by rewrite; diagnose dual-writer; append-only repair under F13 if needed |

## Next repair (not done in this pass)

1. Identify which process writes `seal_chain.jsonl` without head lock.  
2. Single-writer rule: only `seal_chain.js` / approved Python mirror.  
3. Reconcile head hash with last line; re-verify.  
4. Separate metrics in conformance: `constitutional_chain_ok` vs `cooling_ledger_ok`.

## Status

- **Constitutional ledger:** DEGRADED integrity signal (verify fail) — treat as **WARN/HOLD for high-impact seals**, not silent GREEN.  
- **Cooling ledger:** analytical; DEGRADED ≠ automatic mutation block unless policy couples them.  
- **No rewrite** of historical seals performed.
