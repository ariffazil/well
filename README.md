# well — Human Bio-Telemetry Substrate

> **Status:** HARDENED | **Organ:** SUBSTRATE | **Authority:** arifOS

## 🏛️ What this repo is
Governs the biological feedback loop. Monitors human readiness and health telemetry.

## 📦 Ownership
- **Owns**: Bio-telemetry server, readiness audit logs, `state.json` persistence.
- **Does NOT own**: Deployment orchestration (A-FORGE).

## 🏗️ Current Structure
- src/: Telemetry server and logic.
- data/: Canonical `state.json` persistence.
- docs/audit/: Readiness and health audit logs.
- specs/: Bio-governance contracts.

## 🚀 Verified Commands
- `python src/server.py`: Start the WELL telemetry node.

## 🔗 Federation Loop
- [arifOS](https://github.com/ariffazil/arifOS) (Kernel)
- [A-FORGE](https://github.com/ariffazil/A-FORGE) (Forge)

---
*Last Verified: 2026.05.16 | 999 SEAL ALIVE*
