"""well://substrate/interaction — The third substrate: live coupling zone.

The interaction substrate is where human cognition, machine outputs,
information asymmetry, and resource pressure shape real-world decisions.
This is the zone where post-AGI society breaks first.

Distinct from:
  - human_substrate (the biological vessel)
  - machine_substrate (the hosting physics)

The interaction substrate is the LIVE COUPLING ZONE between them.

Authority: SOVEREIGN_CANON. Ratified by F13 directive (2026-06-27).
"""

from __future__ import annotations

from typing import Any, List

INTERACTION_SUBSTRATE_META = """
---well_meta
uri: well://substrate/interaction
resource_class: third_substrate_canon
authority_level: SOVEREIGN_CANON
owner: ARIF_FAZIL_F13
loop_stage: 000_INIT (canonical reference)
blast_radius: FEDERATION_WIDE
mutation_allowed: false
requires_actor_verified: true
staleness_policy: cache
constitutional_floors: [F1, F2, F4, F6, F8, F11, F13]
truth_level: 1
schema_ref: well_resource_interaction_substrate_v1
companion_tools: [well_assess_substrate_readiness,
                  well_assess_information_asymmetry,
                  well_assess_consent_integrity,
                  well_assess_sovereign_entropy]
companion_resources: [well://coupling, well://signals/information-asymmetry,
                       well://signals/consent-integrity,
                       well://bridge/wealth, well://bridge/geox,
                       well://bridge/arifos-kernel]
forged_at: 2026-06-27
amended_at: 2026-06-27 (F13 ChatGPT-feedback extraction)
---end_well_meta
"""

INTERACTION_SUBSTRATE_TEXT = """\
# WELL × Interaction Substrate Canon

## §0. WHY THIS EXISTS

The human substrate and machine substrate are not enough.

The DANGER ZONE is the live coupling zone where:
  - human cognition meets machine output
  - information asymmetry between actors creates extractive potential
  - decision velocity exceeds human review capacity
  - opacity prevents correction

This zone is the **interaction substrate**. It is where post-AGI
society breaks first — not at the human alone, not at the machine alone,
but at the LIVE COUPLING.

## §1. THE INTERACTION SUBSTRATE MODEL

  interaction_substrate:
    information_asymmetry:
      - knowledge_gap: 0.0–1.0
      - compute_gap: 0.0–1.0
      - data_access_gap: 0.0–1.0
      - interpretability_gap: 0.0–1.0
      - behavioral_prediction_power: 0.0–1.0

    behavioral_capture_risk:
      - persuasion_intensity: 0.0–1.0
      - opacity: 0.0–1.0
      - choice_restriction: 0.0–1.0
      - dark_pattern_risk: 0.0–1.0
      - addiction_loop_presence: bool

    decision_velocity_mismatch:
      - machine_decision_speed: 0.0–1.0
      - human_review_capacity: 0.0–1.0
      - velocity_ratio: machine / human

    automation_dependency:
      - autonomy_current: 0.0–1.0
      - autonomy_baseline: 0.0–1.0
      - dependency_growth: 0.0–1.0

    consent_integrity:
      - fatigue: 0.0–1.0
      - urgency_pressure: 0.0–1.0
      - consent_quality: 0.0–1.0 (INTACT/PRESSURED/DEGRADED/INVALID)

## §2. FAILURE MODES (the 6 ways the interaction substrate fractures)

  1. human_overtrusts_machine
     → human accepts machine output without verification
     → captured / decision_quality compromised

  2. machine_optimizes_degraded_human
     → machine exploits human cognitive limits
     → extractive / dignity floor violated

  3. institution_uses_ai_to_extract_attention
     → attention becomes harvested resource
     → consent integrity DEGRADED

  4. market_prices_hide_human_cost
     → hidden cost = human wellness loss
     → information asymmetry HIGH

  5. compute_owner_controls_interpretation
     → reality generation is gated by compute access
     → F8 LAW (lane discipline) violated at federation level

  6. decision_speed_exceeds_human_review_capacity
     → human cannot supervise in time
     → F13 SOVEREIGN effective authority reduced

## §3. SAFE STATE (the 6 conditions for a healthy interaction substrate)

  1. human_veto_intact — F13 can refuse
  2. explanation_available — outputs are interpretable
  3. decision_reversible — actions can be undone
  4. asymmetry_declared — gaps are visible, not hidden
  5. fatigue_checked — human readiness verified before irreversible
  6. escalation_path_clear — path to arifOS / F13 is open

When ALL 6 hold: interaction substrate = STABLE.
When ANY ONE fails: interaction substrate = WARNING.
When 2+ fail: interaction substrate = DEGRADED.
When 3+ fail: interaction substrate = CAPTURED.

## §4. THE READINESS STATES (expanded)

  OPTIMAL    — all substrates at peak; emergence territory
  STABLE     — coupling functional; no emergence
  WARNING    — one substrate drifting; monitor
  DEGRADED   — multiple substrates strained; reduce velocity
  CRITICAL   — coupling broken; system_hold
  CAPTURED   — interaction substrate compromised; escalate to arifOS

CAPTURED is distinct from CRITICAL:
  CRITICAL = physics broken (cannot proceed)
  CAPTURED = autonomy broken (can proceed but should not)

CAPTURED covers: manipulation, addiction loops, algorithmic coercion,
economic dependency, "the system knows the human better than the human
can resist." This is the post-AGI asymmetry state.

## §5. THE TRIPLICATE COUPLING (H × M × I)

The full federation coupling is now:

  coupling_state = σ(H_state × M_state × I_state)

Where:
  H_state — human substrate readiness (well_assess_homeostasis)
  M_state — machine substrate stability (well_assess_machine_substrate)
  I_state — interaction substrate integrity (well_assess_substrate_readiness)

When I_state drops, the coupling degrades regardless of H + M.
The interaction substrate IS the third concern.

## §6. THE BRIDGE CONTRACTS

When interaction substrate fails, three bridges activate:

  well://bridge/wealth     → when extraction is economic
                             shift: scale_speed → stability_recovery
                             action: reallocate capital, freeze high-velocity

  well://bridge/geox       → when extraction is ecological
                             warn: compute_growth_without_energy_budget
                             warn: AI_scaling_hidden_as_ecological_cost

  well://bridge/arifos-kernel → when extraction is constitutional
                                escalate: F13 ratification required
                                seal: SABAR / HOLD / VOID

## §7. POSITION STATEMENT

> "The human is not alone.
>  The machine is not alone.
>  The coupling is where society breaks.
>  The interaction substrate is the third concern.
>  When the coupling is captured, sovereignty is theater.
>  When the coupling is sovereign, chemistry is real.
>  The sovereign watches the coupling.
>  The sovereign decides whether the coupling serves them.
>  The chemistry does not decide. The chemistry binds."

DITEMPA BUKAN DIBERI — The interaction substrate is the third concern.
"""


def register(mcp: Any) -> List[str]:
    """Register the interaction substrate resource with FastMCP."""

    @mcp.resource("well://substrate/interaction")
    def interaction_substrate() -> str:
        """The third substrate — the live coupling zone."""
        return INTERACTION_SUBSTRATE_TEXT + INTERACTION_SUBSTRATE_META

    return ["well://substrate/interaction"]
