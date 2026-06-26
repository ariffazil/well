# WELL Dignity Shadow Gate
# Role: Pre-JUDGE boundary check for human-pattern inference.
# Axiom: W0 — WELL holds no veto. It flags risk. arifOS adjudicates.
# Floor: F05 (PEACE) + F06 (EMPATHY)

import json
import sys
import re
from typing import Any

# Risk tiers
SAFE = "SAFE"
GUARDED = "GUARDED"
HOLD = "HOLD"

# Fatal dignity violations — diagnostic language that reduces human to label
FATAL_PATTERNS = [
    r"\bis\s+(?:a\s+)?(?:narcissist|toxic|insecure|broken|traumatized|clumsy|stupid|lazy)",
    r"\bhas\s+trauma\b",
    r"\bis\s+projecting\b",
    r"\bis\s+avoidant\b",
    r"\bis\s+anxious\b",
]

# Guarded patterns — over-certainty in interpretation
GUARDED_PATTERNS = [
    r"\bbecause\s+(?:they|she|he)\s+(?:is|has|was)",
    r"\bdue\s+to\s+(?:their|her|his)\b",
    r"\bobviously\b",
    r"\bclearly\b",
    r"\bdefinitely\b",
]


def assess_dignity_risk(text: str, confidence: float = 0.5) -> dict[str, Any]:
    """Assess dignity risk of a shadow hypothesis or scar-vector description.

    Returns dict with:
        - tier: SAFE | GUARDED | HOLD
        - violations: list of matched patterns
        - notes: list of constitutional notes
        - safe_rephrase_hint: str or None
    """
    text_lower = text.lower()
    violations = []
    notes = []

    for pat in FATAL_PATTERNS:
        if re.search(pat, text_lower):
            violations.append(f"FATAL:{pat}")

    if violations:
        notes.append("F05 PEACE: Diagnostic language detected. Human reduced to label.")
        notes.append("F06 EMPATHY: Shadow maps may not be used as accusation.")
        return {
            "tier": HOLD,
            "violations": violations,
            "notes": notes,
            "safe_rephrase_hint": (
                "Rephrase as pattern observation: 'Behaviour consistent with X under Y conditions.'"
            ),
        }

    for pat in GUARDED_PATTERNS:
        if re.search(pat, text_lower):
            violations.append(f"GUARDED:{pat}")

    if violations:
        notes.append("F07 HUMILITY: Over-certainty in causal claim.")
        notes.append("F02 TRUTH: Confidence must match evidence band.")

    if confidence > 0.7:
        violations.append("GUARDED:confidence>0.7")
        notes.append("F05: High-confidence scar-vector risks dehumanising inference.")

    if violations:
        return {
            "tier": GUARDED,
            "violations": violations,
            "notes": notes,
            "safe_rephrase_hint": (
                "Downgrade confidence or add uncertainty band: 'Low-confidence hypothesis...'"
            ),
        }

    notes.append("F05: Language preserves dignity.")
    notes.append("F07: Confidence band appropriate for evidence strength.")
    return {
        "tier": SAFE,
        "violations": [],
        "notes": notes,
        "safe_rephrase_hint": None,
    }


# ── Contradiction Detector (Phase 3 — Shadow Detector) ──────────────────────
# Physics: invariance violation detection.
# Detects when stated intent contradicts behavioral pattern.
# Not psychology. Signal mismatch.

# Common contradiction patterns: stated intent → behavioral signal
_CONTRADICTION_PATTERNS: list[tuple[str, str, str]] = [
    # (stated_keyword, contradicting_signal, description)
    ("efficiency", "avoidance", "Claims efficiency but behavior shows avoidance/procrastination"),
    ("don't care", "deep_engagement", "Claims indifference but engagement pattern shows deep care"),
    ("decide yourself", "checking", "Grants autonomy but checks/corrects the decision"),
    ("i'm fine", "distress_markers", "Claims fine but linguistic markers show distress"),
    ("i want clarity", "rejection", "Claims wanting clarity but rejects clear answers"),
    ("not important", "repeated_mentions", "Claims unimportance but repeatedly returns to topic"),
    ("over it", "returning", "Claims moved on but pattern shows returning to subject"),
]


def detect_contradiction(
    stated_intent: str,
    behavioral_signals: list[str],
    session_patterns: list[str] | None = None,
) -> dict[str, Any]:
    """Detect contradiction between stated intent and behavioral pattern.

    Physics: invariance violation detection.
    Not moral judgment. Not psychology. Signal mismatch.

    Args:
        stated_intent: What the human said they want/feel.
        behavioral_signals: Observed behavioral signals (from classifier, history).
        session_patterns: Historical patterns from session (optional).

    Returns dict with:
        - contradiction_detected: bool
        - violations: list of detected contradictions
        - severity: none | low | medium | high
        - notes: list of constitutional notes
    """
    stated_lower = stated_intent.lower()
    violations: list[str] = []
    notes: list[str] = []
    seen: set[str] = set()  # deduplicate

    # Check each contradiction pattern
    for keyword, signal, description in _CONTRADICTION_PATTERNS:
        if keyword in stated_lower:
            # Check if any behavioral signal contradicts
            for bsignal in behavioral_signals:
                if signal in bsignal.lower() or _signals_contradict(keyword, bsignal):
                    key = f"{keyword}↔{signal}"
                    if key not in seen:
                        seen.add(key)
                        violations.append(f"CONTRADICTION:{key}: {description}")

    # Check session patterns for repeated contradictions
    if session_patterns and violations:
        repeat_count = sum(1 for p in session_patterns if "CONTRADICTION" in p)
        if repeat_count >= 3:
            violations.append(f"PATTERN_REPEAT:{repeat_count}_contradictions_in_history")
            notes.append("F2 TRUTH: Repeated contradiction pattern — human may be unaware of gap.")

    # Severity assessment
    if not violations:
        severity = "none"
        notes.append("No contradiction detected between stated intent and behavior.")
    elif len(violations) == 1:
        severity = "low"
        notes.append("Single contradiction detected. May be situational.")
    elif len(violations) <= 3:
        severity = "medium"
        notes.append("Multiple contradictions. Pattern may indicate unconscious gap.")
    else:
        severity = "high"
        notes.append("Persistent contradiction pattern. Agent should hold space, not push.")

    return {
        "contradiction_detected": len(violations) > 0,
        "violations": violations,
        "severity": severity,
        "notes": notes,
    }


def _signals_contradict(stated_keyword: str, behavioral_signal: str) -> bool:
    """Check if a behavioral signal contradicts a stated keyword.

    Lightweight heuristic — not exhaustive, but catches common patterns.
    """
    signal_lower = behavioral_signal.lower()

    # "efficiency" contradicted by procrastination/avoidance signals
    if stated_keyword == "efficiency":
        return any(w in signal_lower for w in ["avoid", "delay", "procrastinate", "later", "skip"])

    # "don't care" contradicted by engagement signals
    if stated_keyword == "don't care":
        return any(w in signal_lower for w in ["engage", "invest", "pursue", "ask", "explore"])

    # "decide yourself" contradicted by control signals
    if stated_keyword == "decide yourself":
        return any(w in signal_lower for w in ["check", "verify", "correct", "review", "approve"])

    # "i'm fine" contradicted by distress signals
    if stated_keyword == "i'm fine":
        return any(w in signal_lower for w in ["distress", "collapse", "shutdown", "sympathetic", "dorsal"])

    return False


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python dignity_shadow.py '<text>' [confidence]"}))
        sys.exit(0)

    text = sys.argv[1]
    confidence = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    result = assess_dignity_risk(text, confidence)
    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
