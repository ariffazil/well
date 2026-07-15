# WELL Loop — Bounded Self-Regulation

```
Sense → Interpret → Propose → Judge(A_eff) → Act≤1 → Verify → Learn(advisory)
```

**Not** unrestricted autonomy. One allowlisted service. Max one mutation. Authority shrinks with weak evidence.

## CLI

```bash
cd /root/WELL
# Observe / recommend only
PYTHONPATH=/root/WELL .venv/bin/python3 loop/recovery_v1.py --json

# Controlled recovery (allowlisted only)
PYTHONPATH=/root/WELL .venv/bin/python3 loop/recovery_v1.py --mutate --json

# Tests
PYTHONPATH=/root/WELL .venv/bin/python3 loop/test_loop.py
```

## Allowlist (hard)

- `well-heartbeat.service` only

## Modules

| File | Role |
|------|------|
| `state_envelope.py` | Typed evidence (no prose authority) |
| `a_effective.py` | A×E×R×G×S power reduction |
| `recommend.py` | ≥3 options + VOID traps |
| `recovery_v1.py` | Closed loop + receipts |
| `catalogues/autonomic_recovery_v1.yaml` | Policy surface |

## Receipts

`loop/receipts/recovery_*.json` + `recovery_ledger.jsonl`

## Law

- Human state: REFLECT_ONLY — never invent biometrics
- Constitution / bands / allowlist: not self-modifiable
- Learning: advisory only
