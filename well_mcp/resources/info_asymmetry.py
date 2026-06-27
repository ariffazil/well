"""well://signals/information-asymmetry — Asymmetry as substrate signal.

Information asymmetry is not just market inefficiency. In post-AGI
societies it becomes control over reality formation. WELL treats it
as a SUBSTRATE SIGNAL — something that can degrade the interaction
substrate and trigger federation escalation.

Authority: SOVEREIGN_CANON. Ratified by F13 (2026-06-27).
"""

from __future__ import annotations

from typing import Any, List

INFO_ASYMMETRY_META = """
---well_meta
uri: well://signals/information-asymmetry
resource_class: asymmetry_signal_canon
authority_level: SOVEREIGN_CANON
owner: ARIF_FAZIL_F13
loop_stage: 333_REASON
blast_radius: FEDERATION_WIDE
mutation_allowed: false
requires_actor_verified: false
staleness_policy: cache
constitutional_floors: [F1, F2, F4, F6, F11]
truth_level: 2
schema_ref: well_resource_info_asymmetry_v1
companion_tools: [well_assess_information_asymmetry,
                  well_power_audit, well_assess_substrate_readiness]
companion_resources: [well://substrate/interaction,
                       well://bridge/wealth, well://bridge/arifos-kernel]
forged_at: 2026-06-27
---end_well_meta
"""

INFO_ASYMMETRY_TEXT = """\
# WELL × Information Asymmetry Signal

## §0. WHY THIS IS A SUBSTRATE SIGNAL

Before AGI: asymmetry = insider information, market advantage.
After AGI: asymmetry = **control over reality formation**.

If human wellness drops, asymmetry widens exponentially.
If asymmetry is HIGH, the human cannot detect manipulation.
If the human cannot detect manipulation, extraction is invisible.

WELL treats asymmetry as a SUBSTRATE SIGNAL — observable, measurable,
governance-relevant.

## §1. THE 5 GAP DIMENSIONS

  knowledge_gap            0.0–1.0
  compute_gap              0.0–1.0
  data_access_gap          0.0–1.0
  interpretability_gap     0.0–1.0
  behavioral_prediction_power  0.0–1.0

Each dimension measures the gap between two actors:
  actor_a and actor_b (human | machine | institution | market)

## §2. ASYMMETRY LEVELS (the routing states)

  LOW            0.00–0.25   safe to proceed
  MODERATE       0.25–0.50   monitor; declare asymmetry
  HIGH           0.50–0.75   countermeasure required; audit
  EXTRACTION_RISK 0.75–1.00   constitutional escalation; HOLD

EXTRACTION_RISK is the post-AGI alarm state. When reached:
  - bridge to well://bridge/wealth (allocation shift)
  - bridge to well://bridge/arifos-kernel (constitutional escalation)
  - bridge to well://substrate/interaction (CAPTURED signal)

## §3. EXTRACTION VECTORS

The 6 ways asymmetry is weaponized:

  1. pricing       — market prices hidden cost
  2. attention     — harvested cognitive resource
  3. labor         — extracted productivity without consent
  4. behavior      — predicted + steered
  5. political_control — narrative dominance
  6. resource_access — compute/energy gatekeeping

When ANY vector is HIGH (≥ 0.50), the asymmetry level is at least HIGH.

## §4. COUNTERMEASURE PROTOCOL

  LOW         → proceed; no action
  MODERATE    → disclose asymmetry; surface gap to sovereign
  HIGH        → audit; require explanation; slow velocity
  EXTRACTION  → constitutional_hold; escalate to arifOS

The asymmetry is NOT silently fixed. It is DECLARED.
Declaration is the floor of trust.

## §5. CONSENT + ASYMMETRY (the F13 connection)

When consent_integrity < 0.70 AND asymmetry > 0.50:
  → CAPTURED state triggered
  → escalate to arifOS for F13 ratification
  → HOLD all high-impact decisions
  → disclose asymmetry explicitly to the sovereign

Without consent, asymmetry is extraction.
With consent (despite asymmetry), the sovereign chooses.

## §6. THE GAP-DECLARATION DOCTRINE

  "Asymmetry must be declared, not exploited."

WELL NEVER hides asymmetry from the sovereign.
WELL NEVER optimizes the asymmetry away silently.
WELL surfaces the gap and lets the sovereign decide.

## §7. POSITION STATEMENT

> "Asymmetry is not just market inefficiency.
>  Asymmetry is control over reality formation.
>  When asymmetry widens, the human cannot detect manipulation.
>  When the human cannot detect manipulation, extraction is invisible.
>  WELL declares asymmetry. The sovereign decides what to do.
>  The chemistry does not decide. The chemistry binds."

DITEMPA BUKAN DIBERI — Declare, don't exploit.
"""


def register(mcp: Any) -> List[str]:
    """Register the information asymmetry resource with FastMCP."""

    @mcp.resource("well://signals/information-asymmetry")
    def info_asymmetry() -> str:
        """Asymmetry as substrate signal — declare, don't exploit."""
        return INFO_ASYMMETRY_TEXT + INFO_ASYMMETRY_META

    return ["well://signals/information-asymmetry"]
