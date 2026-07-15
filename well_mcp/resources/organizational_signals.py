"""well://organizational/signals — Tier 5 organizational/relational signal map.

BACKFILL 2026-07-15: Extends WELL's 13-signal human substrate model
with organizational/relational signals that reflect the sovereign's
context in roles, institutions, and relationships.

Authority: SOVEREIGN_CANON. Draft status until 3 calibration cases.

These signals require OPERATOR SELF-REPORT paths — they cannot be
inferred from wearables or system state. The human must answer.

DITEMPA BUKAN DIBERI — Organizational signals complete the human.
"""

# ============================================================================
# TIER 5 — ORGANIZATIONAL / RELATIONAL SIGNALS
# ============================================================================
# These extend S13 (environment_livelihood) with work-role signals
# that sit at the boundary of WELL (human readiness) and WEALTH
# (institutional capital). WELL reflects; WEALTH computes.
#
# All five require operator self-report (survey or daily check-in).
# No biometric inference is possible for organizational signals.
# ============================================================================

ORGANIZATIONAL_SIGNAL_MAP = {
    # S14 — Role Clarity & Role Integrity
    # Already exists as parameter in well_assess_livelihood (role_clarity).
    # Formalized here as a dedicated signal with self-report path.
    "S14": {
        "name": "role_clarity_integrity",
        "description": "Clarity of role definition, boundaries, and authority. "
        "Measures whether the operator knows what their role is, "
        "where the boundaries are, and whether the role is stable.",
        "tier": 5,
        "companion_tool": "well_assess_livelihood(mode='role')",
        "parameters": ["role_clarity", "role_burden", "duty_load"],
        "self_report_path": {
            "type": "scale_1_10",
            "prompt": "How clear is your current role — its scope, authority, and boundaries? (1=completely unclear, 10=crystal clear)",
            "frequency": "weekly",
            "minimum_gap_hours": 24,
            "companion_questions": [
                "Has your role changed significantly in the last 30 days?",
                "Do you have the authority to make decisions in your scope?",
                "Are you being asked to operate outside your role boundaries?",
            ],
        },
        "freshness_policy": "operator_report_only",
        "cross_organ_handoff": None,
        "status": "ACTIVE_VIA_S13",
        "backfill_epoch": "2026-07-15",
    },
    # S15 — Feedback Loop Health
    "S15": {
        "name": "feedback_loop_health",
        "description": "Health of organizational feedback loops — whether the "
        "operator receives timely, honest feedback on their work, "
        "and whether their input flows upward effectively.",
        "tier": 5,
        "companion_tool": "well_assess_livelihood (proposed extension)",
        "parameters": [
            "feedback_receipt_quality",
            "feedback_upward_flow",
            "feedback_loop_latency",
            "feedback_safety",
        ],
        "self_report_path": {
            "type": "composite_scale",
            "primary_prompt": "When was the last time you received meaningful feedback on your work? (1=never, 10=today/yesterday)",
            "secondary_prompt": "When you raise a concern upward, does it get addressed? (1=ignored, 5=sometimes, 10=always)",
            "safety_check": "Do you feel safe giving honest upward feedback?",
            "frequency": "biweekly",
            "minimum_gap_hours": 72,
        },
        "freshness_policy": "operator_report_only",
        "cross_organ_handoff": None,
        "status": "DRAFT — needs 3 calibration cases before promotion",
        "backfill_epoch": "2026-07-15",
        "scar_reference": "scar_feedback_loop_2025",
    },
    # S16 — Mentoring & Knowledge Transfer
    "S16": {
        "name": "mentoring_knowledge_transfer",
        "description": "Presence and quality of mentoring relationships — both "
        "receiving mentorship and providing it. Measures whether "
        "knowledge is flowing between experience levels.",
        "tier": 5,
        "companion_tool": "well_assess_livelihood (proposed extension)",
        "parameters": [
            "mentoring_received",
            "mentoring_provided",
            "knowledge_transfer_rate",
            "isolation_risk",
        ],
        "self_report_path": {
            "type": "composite_scale",
            "primary_prompt": "Do you have someone whose experience you can draw on for guidance? (1=no one, 10=active mentor relationship)",
            "secondary_prompt": "Are you actively developing others? (1=no, 10=structured mentoring)",
            "loss_detection": "Has a key mentor or protege left in the last 90 days?",
            "frequency": "monthly",
            "minimum_gap_hours": 168,
        },
        "freshness_policy": "operator_report_only",
        "cross_organ_handoff": None,
        "status": "DRAFT — needs 3 calibration cases before promotion",
        "backfill_epoch": "2026-07-15",
    },
    # S17 — Meeting-to-Decision Ratio
    "S17": {
        "name": "meeting_to_decision_ratio",
        "description": "Ratio of meetings held to decisions made. High meeting "
        "volume with low decision output indicates institutional "
        "entropy — consensus-seeking as delay, not alignment.",
        "tier": 5,
        "companion_tool": "well_assess_livelihood (proposed extension) + WEALTH entropy",
        "parameters": [
            "meetings_per_week",
            "decisions_per_week",
            "decision_latency",
            "meeting_satisfaction",
            "ratio_signal",
        ],
        "self_report_path": {
            "type": "numeric_tracking",
            "primary_prompt": "How many meetings did you attend this week that had a clear decision outcome?",
            "secondary_prompt": "How many meetings were information-sharing only (no decision)?",
            "decision_tracking": "Of decisions needed this week, how many were made?",
            "frequency": "weekly",
            "minimum_gap_hours": 24,
        },
        "freshness_policy": "operator_report_only",
        "cross_organ_handoff": "WEALTH — high meeting-to-decision ratio with falling decision count is institutional entropy signal",
        "status": "DRAFT — needs 3 calibration cases before promotion",
        "backfill_epoch": "2026-07-15",
    },
    # S18 — Exit Narratives
    "S18": {
        "name": "exit_narratives",
        "description": "Patterns in how people leave the operator's organizational "
        "context. Exit narratives reveal institutional health.",
        "tier": 5,
        "companion_tool": "well_assess_livelihood (proposed) + WEALTH collapse_signature",
        "parameters": [
            "recent_departures_count",
            "exit_quality",
            "capability_loss",
            "succession_quality",
            "exit_narrative_contagion",
            "institutional_memory_loss",
        ],
        "self_report_path": {
            "type": "periodic_review",
            "primary_prompt": "How would you characterize the last departure in your team? (regenerative/neutral/corrosive)",
            "secondary_prompt": "Did the departing person's knowledge transfer before leaving? (fully/partially/not at all)",
            "contagion_check": "Are you aware of others planning to leave?",
            "capability_check": "Is there a capability gap that can't be easily filled?",
            "frequency": "monthly or on departure event",
            "minimum_gap_hours": 0,
        },
        "freshness_policy": "event_triggered",
        "cross_organ_handoff": "WEALTH — exit narrative pattern matching against institutional collapse_signature axes",
        "status": "DRAFT — needs 3 calibration cases before promotion",
        "backfill_epoch": "2026-07-15",
    },
}

# ============================================================================
# COVERAGE SUMMARY
# ============================================================================
# Tier 5 adds 5 new signals (S14-S18) to the existing 13-signal model:
#
#   S14 role_clarity_integrity       -> ACTIVE (via well_assess_livelihood)
#   S15 feedback_loop_health         -> DRAFT
#   S16 mentoring_knowledge_transfer -> DRAFT
#   S17 meeting_to_decision_ratio    -> DRAFT
#   S18 exit_narratives              -> DRAFT
#
# All DRAFT signals require 3 calibration cases before promotion to ACTIVE.
# Calibration cases should be drawn from operator self-reports over time.

REGISTERED = list(ORGANIZATIONAL_SIGNAL_MAP.keys())
