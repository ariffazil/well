"""well://signals/consent-integrity — The F13 protection layer.

Whether the human is still sovereign. Whether consent is real or
manufactured. The protection layer above all dignity floors.

Authority: SOVEREIGN_CANON. Ratified by F13.
"""

from __future__ import annotations

from typing import Any, List

CONSENT_INTEGRITY_META = """
---well_meta
uri: well://signals/consent-integrity
resource_class: consent_protection_signal
authority_level: SOVEREIGN_CANON
owner: ARIF_FAZIL_F13
loop_stage: 333_REASON
blast_radius: FEDERATION_WIDE
mutation_allowed: false
requires_actor_verified: true
staleness_policy: fail_closed
constitutional_floors: [F6, F13]
truth_level: 1
schema_ref: well_resource_consent_integrity_v1
companion_tools: [well_assess_consent_integrity, well_guard_dignity,
                  well_assess_sovereign_entropy]
forged_at: 2026-06-27
---end_well_meta
"""

CONSENT_INTEGRITY_TEXT = """\
# WELL × Consent Integrity Signal

## §0. WHY CONSENT IS A SIGNAL

Consent is not a checkbox. Consent is a substrate signal.
It can degrade, become pressured, or become invalid.
WELL observes it continuously, not just at the gate.

When consent integrity drops, the interaction substrate can be CAPTURED.
When consent is invalid, the sovereign is not really sovereign.

## §1. THE 4 CONSENT STATES

  INTACT
    - human is awake, informed, free to refuse
    - decision velocity matches human review capacity
    - no urgency pressure
    - consent_quality ≥ 0.85

  PRESSURED
    - human is informed but under time pressure
    - dependency or urgency affecting choice
    - 0.65 ≤ consent_quality < 0.85

  DEGRADED
    - human is fatigued, stressed, or dependent
    - decision velocity exceeds review capacity
    - 0.40 ≤ consent_quality < 0.65

  INVALID
    - human cannot effectively refuse
    - coercion, addiction loop, or capture detected
    - consent_quality < 0.40

## §2. THE 5 INPUT SIGNALS

  fatigue              0.0–1.0  (from well_assess_homeostasis)
  stress               0.0–1.0  (from well_assess_homeostasis)
  dependency           0.0–1.0  (interaction_substrate)
  urgency_pressure     0.0–1.0  (interaction_substrate)
  persuasion_intensity 0.0–1.0  (system_behavior)

  system_behavior:
    opacity               0.0–1.0
    choice_restriction    0.0–1.0
    dark_pattern_risk     0.0–1.0

## §3. CONSENT QUALITY EQUATION

  consent_quality = (1 − fatigue) × (1 − stress) × (1 − dependency)
                   × (1 − urgency_pressure) × (1 − persuasion_intensity)
                   × (1 − opacity) × (1 − choice_restriction)
                   × (1 − dark_pattern_risk)

Returns 0.0–1.0. Threshold mapping:
  ≥ 0.85  INTACT
  0.65–0.84  PRESSURED
  0.40–0.64  DEGRADED
  < 0.40  INVALID

## §4. SOVEREIGNTY RISK (the F13 dimension)

  LOW     — consent INTACT, sovereignty preserved
  MEDIUM  — consent PRESSURED, sovereignty partially intact
  HIGH    — consent DEGRADED, sovereignty compromised
  CRITICAL — consent INVALID, sovereignty is theater

## §5. ROUTING BY CONSENT STATE

  INTACT       → proceed; full sovereignty
  PRESSURED    → simplify; reduce choice surface
  DEGRADED     → pause; require explicit re-consent
  INVALID      → escalate to arifOS; HOLD all irreversibles

## §6. THE F13 PROTECTION LAYER

Consent integrity is the LAYER ABOVE the dignity floor.
Both must hold for any irreversible action to proceed.

  dignity_preservation ≥ 0.70   (F6 MARUAH floor)
  consent_quality      ≥ 0.65   (F13 protection layer)

If either fails → HOLD + escalate.
If both fail → VOID + constitutional escalation.

## §7. THE GAP-DECLARATION DOCTRINE (extended)

  "Consent must be real, not manufactured."

WELL surfaces consent state continuously, not just at intake.
WELL never assumes consent persists.
WELL re-validates consent before irreversible actions.
WELL never optimizes consent away.

## §8. POSITION STATEMENT

> "Consent is not a checkbox. Consent is a substrate signal.
>  Consent can degrade. Consent can be manufactured.
>  The sovereign watches the signal.
>  The sovereign decides whether to act.
>  Without real consent, sovereignty is theater.
>  With real consent, sovereignty is the constitution."

DITEMPA BUKAN DIBERI — Consent is real, not manufactured.
"""


def register(mcp: Any) -> List[str]:
    """Register the consent integrity resource with FastMCP."""

    @mcp.resource("well://signals/consent-integrity")
    def consent_integrity() -> str:
        """Consent integrity signal — F13 protection layer."""
        return CONSENT_INTEGRITY_TEXT + CONSENT_INTEGRITY_META

    return ["well://signals/consent-integrity"]
