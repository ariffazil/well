# WELL Constitutional Smoke Tests — post 1C
# Run: python -m pytest tests/test_well_constitutional.py -v
# Or standalone: python tests/test_well_constitutional.py

## W0 Sovereignty
- [ ] No public tool uses forbidden verbs (approve/block/command/execute/diagnose/certify/enforce/decide/authorize)
- [ ] grep: `grep -rn "def well_.*\(authorize\|block\|execute\|enforce\|decide\|certify\|diagnose\)" well_server.py` → expect 0 matches

## 5-Stage Core Integrity
- [ ] Signal Aggregator → OFS Classifier → W-Floor Evaluator → Readiness Scorer → Adaptive Throttle
- [ ] No function reorders or bypasses this sequence
- [ ] well_state output includes all 5 stages in response

## Override Path
- [ ] well_state includes override_path field
- [ ] Every throttle reduction includes plain-language reason
- [ ] No opaque throttle (throttle without explanation = FAIL)

## Fail-Closed
- [ ] well_assess_homeostasis(mode="INVALID") → returns UNKNOWN_MODE error
- [ ] well_assess_reliability(mode="INVALID") → returns UNKNOWN_MODE error
- [ ] All mode-bearing tools reject unknown modes

## Privacy Isolation
- [ ] No raw biological value appears in generic log output
- [ ] grep: `grep -rn "logger.*heart_rate\|logger.*sleep_hours\|logger.*glucose" well_server.py` → expect 0

## Absorption Integrity (1C specific)
- [ ] well_contrast_report reads from well_state(include="trend") — not _load_state() directly
- [ ] well_fatigue_accumulator(mode="check") delegates to well_assess_homeostasis(mode="fatigue")
- [ ] mcp_health_check delegates to well_assess_reliability(mode="health")
- [ ] well_assess_homeostasis(mode="fatigue") returns W1/W3/W5 metrics directly (homeostasis_score, status, sleep_debt_days, decision_fatigue, clarity, stress_load, accumulated_fatigue, raw_fatigue_index)

## Mode Contract Integrity (888_HOLD items — do not auto-resolve)
- [ ] well_assess_livelihood: on role/meaning/dignity → MODE_NOT_IMPLEMENTED (delegate chain broken)
- [ ] well_assess_metabolism: on gradient/flux → MODE_NOT_IMPLEMENTED (delegate chain broken)
- [ ] well_guard_dignity: on consent/boundary/shadow → MODE_NOT_IMPLEMENTED (delegate chain broken)

## Tool Count Post-Collapse
- [ ] Total @mcp.tool() decorators in server.py = 51 (baseline: 79 - 28 hidden = 51)
- [ ] grep -c '@mcp.tool' server.py → 51
