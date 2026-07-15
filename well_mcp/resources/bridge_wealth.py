"""well://bridge/wealth — The WELL→WEALTH federation bridge contract.

When WELL detects substrate degradation, WEALTH must shift allocation
from growth to recovery. This is the bridge that makes wellness an
allocation signal — not just a reflection.

Authority: SOVEREIGN_CANON. Ratified by F13.
"""

from __future__ import annotations

from typing import Any, List

BRIDGE_WEALTH_META = """
---well_meta
uri: well://bridge/wealth
resource_class: federation_bridge_contract
authority_level: SOVEREIGN_CANON
owner: ARIF_FAZIL_F13
loop_stage: 555_ROUTE
blast_radius: FEDERATION_WIDE
mutation_allowed: false
requires_actor_verified: false
staleness_policy: cache
constitutional_floors: [F1, F4, F11]
truth_level: 1
schema_ref: well_resource_bridge_wealth_v1
companion_tools: [well_trigger_resource_reallocation,
                  wealth_arifos_judge_handoff]
companion_resources: [well://substrate/interaction,
                       well://signals/information-asymmetry]
forged_at: 2026-06-27
---end_well_meta
"""

BRIDGE_WEALTH_TEXT = """\
# WELL → WEALTH Federation Bridge

## §0. WHY THIS BRIDGE EXISTS

Markets alone fail at substrate-aware allocation because:
  - Information asymmetry breaks price signals
  - Compute concentration creates monopolies
  - Human degradation is not priced correctly
  - Interaction substrate cost is hidden

Post-AGI economics needs WELL because markets do not naturally price
cognitive exhaustion, consent invalidation, or capture risk.

WELL emits allocation signals. WEALTH receives them. WEALTH acts
within its lane (computation, not authorization).

## §1. TRIGGER CONDITIONS (when bridge fires)

WELL triggers the bridge when ANY of:

  - substrate_readiness = DEGRADED
  - substrate_readiness = CRITICAL
  - substrate_readiness = CAPTURED
  - metabolic_flux ≥ 0.65
  - information_asymmetry = HIGH or EXTRACTION_RISK
  - consent_integrity = DEGRADED or INVALID

## §2. ALLOCATION RESPONSE MATRIX

  substrate DEGRADED:
    action: reduce_velocity
    shift_resources_to:
      - rest
      - review
      - interpretability
      - human_support

  substrate CRITICAL:
    action: freeze_high_impact_decisions
    shift_resources_to:
      - recovery
      - oversight
      - redundancy

  substrate CAPTURED:
    action: constitutional_escalation
    shift_resources_to:
      - transparency
      - audit
      - anti_coercion
      - human_veto_restoration

  information_asymmetry HIGH:
    action: disclose
    shift_resources_to:
      - transparency
      - audit
      - explanation_surfaces

  consent_integrity DEGRADED:
    action: pause_irreversibles
    shift_resources_to:
      - re_consent_flows
      - human_review_buffers

## §3. SIGNAL PAYLOAD (what WELL emits to WEALTH)

```yaml
well_to_wealth_signal:
  signal_id: uuid4
  ts: iso8601
  trigger: substrate_state | asymmetry | consent
  trigger_state: DEGRADED | CRITICAL | CAPTURED | HIGH | INVALID
  priority_shift:
    from: scale_speed
    to: stability_recovery
  resource_pressure:
    compute: 0.0–1.0
    attention: 0.0–1.0
    capital: 0.0–1.0
    time: 0.0–1.0
    energy: 0.0–1.0
  capital_type: cognitive | temporal | financial | ecological | compute
  allocation_reason: human_readable
  escalation_required: bool
```

## §4. WEALTH RECEIPT (what WEALTH returns)

WEALTH computes a reallocation recommendation:

```yaml
wealth_receipt:
  signal_id: uuid4
  reallocation_signal: NONE | WATCH | REALLOCATE | FREEZE
  shift_vector:
    from_dimension: scale_speed | optimization | growth
    to_dimension: stability | recovery | audit | transparency
  magnitude: 0.0–1.0
  estimated_cost: currency
  estimated_recovery_window: hours
  escalation_to_arifos: bool
```

WEALTH NEVER authorizes execution. WEALTH computes.
arifOS judges. Arif decides.

## §5. THE BRIDGE PROTOCOL

  1. WELL detects trigger condition (333_REASON or 666_CRITIQUE)
  2. WELL emits well_to_wealth_signal
  3. WEALTH receives signal (via wealth_arifos_judge_handoff or similar)
  4. WEALTH computes reallocation recommendation
  5. WEALTH returns wealth_receipt
  6. WELL surfaces receipt to sovereign
  7. Sovereign decides whether to ratify
  8. arifOS judges
  9. A-FORGE executes if SEAL

The bridge is INFORMATIONAL. Neither WELL nor WEALTH acts alone.
The sovereign ratifies. arifOS judges. A-FORGE executes.

## §6. WHAT THIS MAKES POSSIBLE

When WELL is wired into WEALTH's allocation loop:
  - Capital flows toward recovery when substrate is degraded
  - High-velocity decisions freeze when consent is invalid
  - Audit resources scale with asymmetry detection
  - Rest is priced as legitimate allocation, not waste
  - Anti-coercion resources scale with capture risk

This is "wellness as allocation signal" — not wellness advice,
but actual capital routing.

## §7. POSITION STATEMENT

> "Markets alone do not price cognitive exhaustion.
>  Markets alone do not price consent invalidation.
>  Markets alone do not price capture risk.
>  The bridge prices what markets miss.
>  The bridge does not replace markets.
>  The bridge supplements markets with substrate truth.
>  The sovereign decides whether to ratify.
>  The chemistry does not decide. The chemistry binds."

DITEMPA BUKAN DIBERI — Wellness as allocation signal.
"""


def register(mcp: Any) -> List[str]:
    """Register the WELL→WEALTH bridge resource with FastMCP."""

    @mcp.resource("well://bridge/wealth")
    def bridge_wealth() -> str:
        """The WELL→WEALTH federation bridge contract."""
        return BRIDGE_WEALTH_TEXT + BRIDGE_WEALTH_META

    return ["well://bridge/wealth"]
