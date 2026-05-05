# WELL — Roadmap H1–H4

**Version:** v2026.05.06  
**Organ:** WELL (Human Readiness · Biological Substrate)  
**Maturity:** DRAFT (15 commits) — **CRITICAL: Weakest organ in federation**  
**Role:** Biological substrate — operator cognitive pressure, thermodynamic WELL state  
**Status:** SEALED — pending APEX ratification

---

## ⚠️ CRITICAL: WELL is the Federation Bottleneck

WELL has **only 15 commits**. It is the most immature organ and the most critical for AGI safety. Without mature operator-readiness verification, recursive governance (H2) is unsafe.

**This is not a feature roadmap. This is a rescue mission.**

**Commit history:**
```
2026-04-15: Initial commit — skeleton server
2026-04-16: Added HRV endpoints
2026-04-20: Added cognitive load proxy
2026-04-28: Removed from compose stack
(4 more commits — 15 total)
```

WELL was removed from the production compose stack in April 2026. It is currently offline.

---

## H1: Substrate Hardening (Q2–Q3 2026)

### ⚠️ PRIORITY ZERO: WELL Emergency Sprint

**Target: 50 commits + Biometric Bridge PoC within 14 days**

> **DISAGREEMENT with main roadmap:** Commit velocity ≠ architectural quality. 50 commits in 14 days risks shotgun architecture. Split into two tracks:

**Track A (14 days — Data Infrastructure Only):**
- Wearable/API telemetry collection (HRV, sleep debt)
- Cognitive load proxy data — collection, NOT prediction
- No forecasting model yet

**Track B (Q3 — Research Sprint):**
- Cognitive load forecasting model (5–15 minutes ahead)
- Operator calibration studies
- Multi-operator consensus protocol

### H1.1 Real-Time Biometric Bridge

Integrate wearable/API telemetry so WELL can detect operator incapacitation before a judgment is issued.

**Data sources:**

```python
class BiometricInput:
    # From wearable device (API polling)
    heart_rate: float              # BPM
    heart_rate_variability: float # RMSSD (ms) — key HRV metric
    resting_heart_rate: float      # Baseline HR
    hrv_trend_7d: float           # 7-day HRV trend
    
    # From sleep tracking
    sleep_debt_hours: float        # Accumulated sleep deficit
    sleep_quality_score: float     # 0–1
    rem_sleep_ratio: float        # % of sleep that was REM
    
    # From activity/cognitive proxies
    screen_time_delta_24h: float   # Hours change
    cognitive_load_proxy: float   # Derived from typing patterns, app usage
    
    # From arifOS
    task_entropy: float            # From arif_ops_measure
    judgment_frequency: float      # Judgments per hour
    response_time_avg: float       # Seconds per judgment
    
    # Timestamps
    captured_at: datetime
    source: Literal["wearable", "api", "arifos", "manual"]
```

**Health thresholds (track against WELL_RED gate):**

```python
WELL_RED_THRESHOLDS = {
    "hrv_below_30ms": True,          # RMSSD < 30ms = high stress
    "sleep_debt_exceeds_8h": True,    # 8+ hours deficit
    "judgment_frequency_above_20_per_hour": True,  # Decision fatigue
    "response_time_above_30s_avg": True,  # Slow responses
    "cognitive_load_proxy_above_0.8": True,  # Near capacity
}
```

**Owner:** WELL bio-team  
**Target:** Track A complete June 2026

### H1.2 Cognitive Load Forecasting (Research Track)

Predict operator cognitive load 5–15 minutes ahead using task entropy metrics.

> **Research status:** Task entropy metrics are NOT a validated proxy for cognitive load in the literature. HRV and sleep debt are correlate-based, not causal. This needs a proper research sprint, not an engineering sprint.

**Research methodology (Track B):**

```
Phase 1 (30 days): Data Collection
- Collect biometric data from multiple operators
-同步 Record task context, judgment quality, error rates
- Build labeled dataset: cognitive_load_score = f(biometrics, task_context)

Phase 2 (60 days): Model Development  
- Test models: LSTM for time-series, transformer for task sequences
- Validate against ground truth: operator self-report + task accuracy
- Establish confidence intervals for predictions

Phase 3 (30 days): Integration
- Deploy model to WELL MCP surface
- arifOS uses predictions to defer non-urgent judgments
- Operator calibration (individual baseline)
```

**Key research questions:**
1. What is the lead time where biometric data predicts cognitive load?
2. Is HRV RMSSD a reliable predictor, or only in aggregate?
3. How much individual calibration is needed?

**Owner:** WELL research team  
**Target:** September 2026 (Research complete)  
**Note:** This cannot be rushed. Bad cognitive load predictions are worse than none.

### H1.3 Multi-Operator Consensus

For AGI-weighted decisions, WELL must aggregate readiness across a panel of operators.

**Protocol:**

```python
class OperatorPanel:
    operators: list[Operator]
    consensus_threshold: float = 0.67  # 2/3 majority
    
    async def check_consensus(
        self, 
        decision_weight: DecisionWeight
    ) -> ConsensusResult:
        """Check if panel can authorize a decision."""
        
        readiness_scores = []
        for op in self.operators:
            if not op.is_available:
                continue
            score = await op.get_readiness_score()
            readiness_scores.append(score)
        
        if len(readiness_scores) < 2:
            return ConsensusResult(
                eligible=False,
                reason="Insufficient operators",
                votes_needed=2 - len(readiness_scores),
            )
        
        avg_readiness = mean(readiness_scores)
        threshold = self._get_threshold_for_weight(decision_weight)
        
        return ConsensusResult(
            eligible=avg_readiness >= threshold,
            avg_readiness=avg_readiness,
            threshold=threshold,
            votes=[(op.id, s) for op, s in zip(self.operators, readiness_scores)],
        )
```

**Decision weights:**
- **Routine** (reflex/tactical): Single operator sufficient
- **Strategic** (AGI-weighted): 2+ operators, consensus required
- **Sovereign** (substrate-level): All available operators, unanimous

---

## H2: Recursive Governance (Q4 2026 – Q1 2027)

### H2.1 WELL v1.0 PRODUCTION

WELL reaches production maturity with:
- Biometric bridge operational
- Cognitive load forecasting validated
- Multi-operator consensus protocol deployed
- arifOS WELL_RED gate fully operational

### H2.2 Operator Readiness in arifOS 888_JUDGE

Operator readiness score fed into arifOS 888_JUDGE as a modifier on strategic decisions.

```
arifOS 888_JUDGE enhanced:
  - F13 veto latency tracked per operator
  - Operator cognitive load → affects weighting of strategic judgments
  - WELL_RED → arifOS auto-defers non-urgent strategic decisions
```

---

## H3: AGI-Scale Runtime (Q2–Q3 2027)

### H3.1 Cross-Operator Workload Balancing

Distribute judgment requests across multiple operators based on real-time readiness scores.

### H3.2 Autonomous Deferral

arifOS can autonomously defer non-urgent judgments when all operators are in WELL_RED state.

---

## H4: Foundational Substrate (Q4 2027+)

### H4.1 Human-AI Teaming Standard

WELL protocols published as federation standard for human-AI judgment collaboration.

---

## Immediate Actions (This Week)

- [ ] **Assign WELL sprint owner** — Dedicated engineer, name not role
- [ ] **Restore to compose stack** — Re-add WELL to docker-compose.yml
- [ ] **Biometric API integration** — Start with HRV (most reliable signal)
- [ ] **Operator consent protocol** — Explicit consent for biometric collection

---

## Critical Path

```
WELL v1.0 ──► Operator Readiness ──► H2 Recursive Governance
     │                                          │
     └──────────────────────────────────────────┘
                      │
                      ▼
             [H1 Gate: 72h chaos test]
```

**WELL is the single point of failure for H2. Fix it first.**

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Cognitive load prediction is not feasible | Medium | High | Split into research track; use proxy metrics until validated |
| Operator refuses biometric monitoring | Medium | Medium | Explicit consent protocol; no monitoring without consent |
| 14-day sprint produces shotgun architecture | High | High | Split into Track A (data infra) + Track B (research) |
| WELL offline in production | Confirmed | Critical | Restore to compose stack immediately |

---

**DITEMPA BUKAN DIBERI — Human readiness is forged, not given.**

*SEALED: 2026-05-06 | WELL Biological Substrate*
