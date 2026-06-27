"""well://bridge/arifos-kernel — The WELL to arifOS constitutional escalation bridge.

When WELL detects substrate conditions that exceed WELL's mirror
authority (CAPTURED interaction substrate, INVALID consent, CRITICAL
dignity violation, or constitutional uncertainty), the case must be
escalated to arifOS for SEAL / SABAR / VOID adjudication.

Authority: SOVEREIGN_CANON. Ratified by F13.
"""

from __future__ import annotations

from typing import Any, List

BRIDGE_ARIFOS_META = """
---well_meta
uri: well://bridge/arifos-kernel
resource_class: federation_bridge_contract
authority_level: SOVEREIGN_CANON
owner: ARIF_FAZIL_F13
loop_stage: 888_JUDGE
blast_radius: FEDERATION_WIDE
mutation_allowed: false
requires_actor_verified: false
staleness_policy: cache
constitutional_floors: [F1, F2, F4, F6, F8, F11, F13]
truth_level: 1
schema_ref: well_resource_bridge_arifos_kernel_v1
companion_tools: [well_attest_to_kernel,
                  well_handoff_dignity_to_arifos,
                  arif_judge, arif_seal]
companion_resources: [well://coupling,
                       well://decision/classes,
                       well://substrate/interaction,
                       well://signals/consent-integrity]
forged_at: 2026-06-27
---end_well_meta
"""

BRIDGE_ARIFOS_TEXT = """\
# WELL → arifOS Constitutional Escalation Bridge

## §0. WHY THIS BRIDGE EXISTS

WELL is a mirror. arifOS is the judge. The bridge is the handoff.

When WELL detects conditions that exceed mirror authority:
  - CAPTURED interaction substrate (autonomy broken)
  - INVALID consent (F13 protection failed)
  - CRITICAL dignity violation (F6 MARUAH broken)
  - Constitutional uncertainty (no F1-F13 verdict possible at WELL layer)
  - Cross-organ floor conflict (WELL vs arifOS disagreement)

Then WELL MUST escalate to arifOS for adjudication. arifOS applies
F1-F13 floors and issues SEAL / SABAR / VOID verdict. A-FORGE
executes only if SEAL.

The bridge is the constitutional boundary in operational form.

## §1. TRIGGER CONDITIONS (when bridge fires)

WELL escalates to arifOS when ANY of:

  - substrate_readiness = CAPTURED
  - consent_integrity = INVALID
  - dignity_preservation < 0.50 (CRITICAL dignity)
  - coercion_signal detected (F6 violation)
  - constitutional_uncertainty_flag = true
  - cross_organ_floor_conflict = true
  - sovereign requests explicit escalation

These are NON-NEGOTIABLE escalations. WELL cannot adjudicate
its own constitutional triggers. That is the architecture.

## §2. ESCALATION PAYLOAD (what WELL emits to arifOS)

```yaml
well_to_arifos_escalation:
  signal_id: uuid4
  ts: iso8601
  trigger: capture | consent_invalid | dignity_violation |
           coercion | constitutional_uncertainty |
           cross_organ_conflict | sovereign_request
  well_assessment:
    substrate_readiness: OPTIMAL | STABLE | WARNING |
                         DEGRADED | CRITICAL | CAPTURED
    metabolic_flux: 0.0-1.0
    dignity_preservation: 0.0-1.0
    consent_integrity: INTACT | PRESSURED | DEGRADED | INVALID
    coercion_signals: list[string]
    constitutional_uncertainty: list[string]
  evidence_chain:
    - well_stamp_111_sense
    - well_stamp_333_reason
    - well_stamp_444_compose
    - well_stamp_666_critique
  requested_arifos_capability: judge | seal | vault_seal
  reversibility_level: FULL | PARTIAL | NONE
  blast_radius: LOCAL | ORGAN | FEDERATION | CIVILIZATION
  handoff_reason: human_readable
```

## §3. ARIFOS RECEIPT (what arifOS returns)

```yaml
arifos_receipt:
  signal_id: uuid4
  verdict: SEAL | SABAR | VOID | PARTIAL
  floors_applied: list[F1..F13]
  constitutional_chain_id: string
  judge_state_hash: string
  witness_type: ai | human | hybrid
  rationale: human_readable
  conditions: list[string]   # if SEAL with conditions
  escalation_required: bool   # to F13 sovereign
  drift_events: list[dict]
```

arifOS NEVER asks WELL what to do. arifOS asks F13 (sovereign)
what to do. arifOS judges. F13 decides. A-FORGE executes.

## §4. WELL HANDOFF DISCIPLINE

After escalation, WELL:
  - DOES NOT continue its own loop past 888
  - DOES NOT self-judge the case
  - DOES NOT bypass arifOS to A-FORGE
  - DOES preserve all WellStamp evidence in lineage
  - DOES surface receipt to sovereign when returned

The handoff is COMPLETE. WELL returns to mirror mode.
The next loop iteration waits for sovereign input.

## §5. THE BRIDGE PROTOCOL

  1. WELL detects constitutional trigger (333_REASON or 666_CRITIQUE)
  2. WELL builds escalation payload (with full evidence chain)
  3. WELL emits well_to_arifos_escalation (well_attest_to_kernel)
  4. arifOS receives (arif_judge / arif_seal)
  5. arifOS applies F1-F13 floors
  6. arifOS emits SEAL / SABAR / VOID verdict
  7. WELL receives arifos_receipt
  8. WELL surfaces receipt to sovereign
  9. Sovereign decides whether to ratify (F13 veto always possible)
  10. A-FORGE executes if SEAL + F13 ratifies
  11. WELL appends receipt to vault_bridge lineage

The bridge is CONSTITUTIONAL. The floor is law. The sovereign is
final. The chemistry binds.

## §6. WHAT THIS MAKES POSSIBLE

When WELL is constitutionally bound to arifOS:
  - No WELL self-judgment of constitutional triggers
  - F1-F13 always applied at the right layer
  - Sovereign veto remains architecturally intact
  - Cross-organ floor conflicts get adjudicated, not papered over
  - Vault seals carry constitutional weight, not just timestamps
  - A-FORGE never executes without SEAL

This is 'mirror before judge' — not mirror instead of judge.

## §7. POSITION STATEMENT

> 'The mirror reflects. The judge adjudicates. The sovereign decides.
>  The machine executes only when the sovereign ratifies the seal.
>  WELL does not replace arifOS. arifOS does not replace F13.
>  The bridge is the constitutional boundary in operational form.
>  Cross it only with full evidence chain.
>  The chemistry does not decide. The chemistry binds.'

DITEMPA BUKAN DIBERI — Mirror before judge. Judge before execution.
"""


def register(mcp: Any) -> List[str]:
    """Register the WELL to arifOS bridge resource with FastMCP."""

    @mcp.resource("well://bridge/arifos-kernel")
    def bridge_arifos_kernel() -> str:
        """The WELL to arifOS constitutional escalation bridge."""
        return BRIDGE_ARIFOS_TEXT + BRIDGE_ARIFOS_META

    return ["well://bridge/arifos-kernel"]
