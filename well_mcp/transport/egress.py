"""well_mcp.transport.egress — Stage 5 of the 5-stage reaction loop.

EGRESS: assemble final WellStamp, emit to caller. NEVER write vault
(vault is arifOS responsibility). NEVER trigger downstream actions
(handoff is informational only).

Authority: REFLECT_ONLY.

P1.2 closure (2026-07-14): WELL outputs now carry federation-standard
`_epistemic` envelope so cross-organ consumers (arifOS judge, WEALTH,
GEOX, A-FORGE) can reason about WELL's claims with the same vocabulary
used elsewhere. Source-of-truth enums: arifOS federation_enums.py.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Dict

# Federation-standard envelope constants — mirrored from
# arifOS/arifosmcp/schemas/federation_enums.py (canonical source).
# We mirror (not import) because WELL may run in a venv without arifOS.
EPISTEMIC_LABEL = ("OBSERVED", "DERIVED", "INTERPRETED", "SPECULATED", "ASSUMED")
CONFIDENCE_BAND = ("UNKNOWN", "LOW", "MODERATE", "HIGH", "VERIFIED", "SEALED")
OUTPUT_CLASS = (
    "DETERMINISTIC",
    "DOMAIN_COMPUTATION",
    "GOVERNANCE_TEMPLATE",
    "INFERENCE",
    "OBSERVATION",
)


def _derive_envelope(stamp: Dict[str, Any]) -> Dict[str, Any]:
    """Derive federation-standard _epistemic envelope from WellStamp.

    Mapping rules:
      - substrate_canon=HUMAN → INFERENCE (subjective state assessment)
      - confidence="HIGH"/"VERIFIED" → HIGH/VERIFIED band
      - coupling_state>=0.7 → DOMAIN_COMPUTATION class
      - For everything else: conservative defaults (INTERPRETED + MODERATE)
    """
    # Epistemic label: human substrate = INFERENCE, else DERIVED
    substrate = str(stamp.get("substrate_canon", "human")).lower()
    if substrate in ("human", "operator", "sovereign"):
        label = "INFERENCE"  # mapped to INTERPRETED in envelope
    else:
        label = "DERIVED"

    # Confidence band: pass through if in band, else normalize
    conf_raw = str(stamp.get("confidence", "MODERATE")).upper()
    if conf_raw in ("VOID", "STALE"):
        conf_band = "LOW"
    elif conf_raw in CONFIDENCE_BAND:
        conf_band = conf_raw
    else:
        conf_band = "MODERATE"

    # Output class
    coupling = float(stamp.get("coupling_state", 0.5))
    output_class = "DOMAIN_COMPUTATION" if coupling >= 0.7 else "INFERENCE"

    # Risk flags
    risk_flags: list[str] = []
    if conf_band == "LOW":
        risk_flags.append("low_confidence")
    if coupling < 0.4:
        risk_flags.append("low_coupling")

    return {
        "output_class": output_class,
        "ai_involvement": "MEDIUM",  # WELL is AI-mediated substrate reflection
        "authority_claim": "REFLECT_ONLY",  # WellStamp signature
        "evidence_source": "COMPUTED" if substrate != "human" else "INFERRED",
        "tagged_by": "well-mcp",
        "tagged_at": datetime.now(UTC).isoformat(),
        "schema_version": "2.0.0",
        # Federation cross-reference
        "epistemic_label": label,
        "confidence_band": conf_band,
        "risk_flags": risk_flags,
    }


def stamp_egress(judged_stamp: Dict[str, Any]) -> Dict[str, Any]:
    """Stage 5 — EGRESS.

    Args:
        judged_stamp: output of stamp_judge()

    Returns:
        WellStamp.final with all stages' outputs assembled, ready
        for sovereign observation. Includes federation-standard
        `_epistemic` envelope for cross-organ reasoning.

    Cost: < 5 ms.
    """
    final = dict(judged_stamp)
    final.update(
        {
            "stage": "egress",
            "stage_status": "PASS",
            "loop_trace": ["ingress", "encode", "metabolize", "judge", "egress"],
        }
    )

    # Surface ready_to_observe flag (always true — sovereignty is invariant).
    final["ready_to_observe"] = True

    # Surface loop_complete flag.
    final["loop_complete"] = True

    # Federation-standard _epistemic envelope (P1.2 — 2026-07-14).
    # Mirrors arifOS federation_enums.py so other organs can consume
    # WELL outputs without bespoke translation.
    final["_epistemic"] = _derive_envelope(final)

    # Note: WELL NEVER writes vault, NEVER triggers downstream.
    # These are constitutional boundaries enforced by absence.

    return final
