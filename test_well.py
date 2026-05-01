"""
WELL MCP Audit Test Suite
Red · Blue · Gold Team Validation
"""

import asyncio
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

well_dir = Path(__file__).parent
test_dir = Path(tempfile.mkdtemp(prefix="afwell-test-"))
os.environ["WELL_STATE_PATH"] = str(test_dir / "state.json")
os.environ["WELL_EVENTS_PATH"] = str(test_dir / "events.jsonl")
os.environ["WELL_VAULT_PATH"] = str(test_dir / "vault_ledger.jsonl")
server_path = well_dir / "server.py"
spec = importlib.util.spec_from_file_location("afwell_server_under_test", server_path)
assert spec and spec.loader
server_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server_module)
mcp = server_module.mcp


def _write_canonical_state(**overrides):
    """Write a canonical WELL state with optional overrides."""
    import datetime
    state = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "operator_id": "arif",
        "identity": "WELL",
        "role": "Body / Human Intelligence",
        "authority": "REFLECT_ONLY",
        "delta_s": 0.0,
        "peace2": 1.0,
        "kappa_r": 0.95,
        "rasa": True,
        "amanah": "LOCK",
        "metrics": {
            "sleep": {"last_night_hours": 8, "sleep_debt_days": 0, "quality_score": 9},
            "stress": {"subjective_load": 2, "restlessness": 1},
            "cognitive": {"clarity": 10, "decision_fatigue": 2.1, "focus_durability": 9, "pressure_sources": {}},
            "metabolic": {"fasting_window_hours": 0, "perceived_stability": 10, "hydration_status": "STABLE"},
            "structural": {"pain_map": [], "movement_frequency_daily": 5},
        },
        "well_score": 93.8,
        "floors_violated": [],
        "m_machine": {
            "model_reliability": 1.0,
            "tool_availability": 1.0,
            "latency_ms": 200,
            "context_length_pressure": 0.0,
            "memory_integrity": 1.0,
            "api_failure_rate": 0.0,
            "data_freshness": 1.0,
            "compute_budget_pct": 100.0,
            "token_budget_pct": 100.0,
            "security_flags": [],
            "vault_status": "ok",
            "schema_valid": True,
        },
    }
    state.update(overrides)
    Path(os.environ["WELL_STATE_PATH"]).write_text(json.dumps(state))
    return state


def get_data(result):
    """Helper to extract dict from ToolResult."""
    if hasattr(result, "structured_content") and result.structured_content:
        return result.structured_content
    if hasattr(result, "content") and result.content:
        return json.loads(result.content[0].text)
    return {}


# ═══════════════════════════════════════════════════════════════════════════════
# GOLD TEAM — Identity Invariant Tests
# ═══════════════════════════════════════════════════════════════════════════════


def test_identity_invariant_pass():
    _write_canonical_state()
    assert server_module.is_well() is True


def test_identity_invariant_missing_identity():
    _write_canonical_state(identity="NOT_WELL")
    assert server_module.is_well() is False


def test_identity_invariant_missing_role():
    _write_canonical_state(role="Executor")
    assert server_module.is_well() is False


def test_identity_invariant_low_delta_s():
    _write_canonical_state(delta_s=-0.1)
    assert server_module.is_well() is False


def test_identity_invariant_low_peace2():
    _write_canonical_state(peace2=0.5)
    assert server_module.is_well() is False


def test_identity_invariant_low_kappa_r():
    _write_canonical_state(kappa_r=0.5)
    assert server_module.is_well() is False


def test_identity_invariant_rasa_false():
    _write_canonical_state(rasa=False)
    assert server_module.is_well() is False


def test_identity_invariant_amanah_unlocked():
    _write_canonical_state(amanah="UNLOCKED")
    assert server_module.is_well() is False


def test_identity_invariant_authority_overclaim():
    _write_canonical_state(authority="JUDGE")
    assert server_module.is_well() is False


# ═══════════════════════════════════════════════════════════════════════════════
# BLUE TEAM — Input Validation & Adversarial Tests
# ═══════════════════════════════════════════════════════════════════════════════


async def _test_input_validation():
    _write_canonical_state()

    # Negative sleep_hours should be clamped to 0, not crash
    res = await mcp.call_tool("well_log", arguments={"sleep_hours": -100})
    data = get_data(res)
    assert data["ok"] is True, f"Expected ok=True for clamped negative, got {data}"

    # Out-of-range clarity should be clamped
    res = await mcp.call_tool("well_log", arguments={"clarity": 999})
    data = get_data(res)
    assert data["ok"] is True, f"Expected ok=True for clamped high clarity, got {data}"

    # String where number expected should fail gracefully
    # FastMCP/Pydantic rejects at the transport layer; we verify it does not mutate state
    try:
        res = await mcp.call_tool("well_log", arguments={"sleep_hours": "hacked"})
        data = get_data(res)
        assert data["ok"] is False, f"Expected ok=False for string input, got {data}"
    except Exception as e:
        # Pydantic validation error is acceptable — it means schema enforcement is active
        assert "float_parsing" in str(e) or "ValidationError" in str(e) or "unable to parse" in str(e)

    # Verify state was not corrupted by the rejected call
    state_after = server_module._load_state()
    assert state_after.get("well_score") is not None

    # None values should pass (omitted fields)
    res = await mcp.call_tool("well_log", arguments={"sleep_hours": None})
    data = get_data(res)
    assert data["ok"] is True

    # Injection attempt in note should be sanitized
    res = await mcp.call_tool("well_log", arguments={"note": "malicious\x00null\x01byte"})
    data = get_data(res)
    assert data["ok"] is True


async def _test_well_state_reflect_only():
    _write_canonical_state()
    res = await mcp.call_tool("well_state")
    data = get_data(res)
    assert data["ok"] is True
    assert data.get("w0") == "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT"


async def _test_well_log_green_path():
    _write_canonical_state()
    res = await mcp.call_tool("well_log", arguments={"note": "Automated test run"})
    data = get_data(res)
    assert data["ok"] is True


async def _test_well_check_floors_canonical():
    _write_canonical_state()
    res = await mcp.call_tool("well_check_floors")
    data = get_data(res)
    assert data["mcp"] == "AFWELL"
    assert "status" in data
    assert data.get("authority", {}).get("level") == "advisory_only"


async def _test_well_readiness_canonical():
    _write_canonical_state()
    res = await mcp.call_tool("well_readiness")
    data = get_data(res)
    assert data["mcp"] == "AFWELL"
    assert "risk_level" in data
    assert data.get("authority", {}).get("level") == "advisory_only"


async def _test_well_log_state_green():
    _write_canonical_state()
    res = await mcp.call_tool("well_log_state", arguments={
        "sleep_hours": 8,
        "stress_level": 2,
        "clarity_score": 9,
        "note": "Test Green Path"
    })
    data = get_data(res)
    assert data["tier"] == "GREEN"


async def _test_well_log_state_red():
    _write_canonical_state()
    res = await mcp.call_tool("well_log", arguments={
        "sleep_hours": 2,
        "sleep_debt_days": 5,
        "stress_load": 10,
        "clarity": 2,
        "decision_fatigue": 9,
        "note": "Test Red Path - Extreme Stress"
    })
    data = get_data(res)
    assert data["tier"] == "RED"
    assert data["human_decision_required"] is True
    assert "W1_SLEEP_DEBT" in data["floors_violated"]
    assert "W5_COGNITIVE_ENTROPY" in data["floors_violated"]


async def _test_well_get_readiness():
    _write_canonical_state()
    res = await mcp.call_tool("well_get_readiness")
    data = get_data(res)
    assert data["ok"] is True
    assert "readiness" in data


async def _test_well_check_floor_w1():
    _write_canonical_state()
    res = await mcp.call_tool("well_check_floor", arguments={"floor_id": "W1"})
    data = get_data(res)
    if "mcp" in data:
        assert data["mcp"] == "AFWELL"
    else:
        assert data["floor"] == "W1"


async def _test_well_list_log():
    _write_canonical_state()
    res = await mcp.call_tool("well_list_log", arguments={"limit": 5})
    data = get_data(res)
    assert data["ok"] is True


async def _test_well_seal_vault():
    _write_canonical_state()
    res = await mcp.call_tool("well_seal_vault", arguments={"force": True})
    data = get_data(res)
    # Should fail gracefully (no arifOS in test env), but not leak secrets
    assert "error" not in data or "Vault bridge unavailable" in data.get("error", "")


async def _test_well_coupled_readiness():
    _write_canonical_state()
    res = await mcp.call_tool("well_coupled_readiness")
    data = get_data(res)
    assert data["mcp"] == "AFWELL"
    assert "risk_level" in data
    assert "final_authority" in data
    assert data["final_authority"] == "Arif"


async def _test_well_forge_precheck_conservative():
    _write_canonical_state()
    await mcp.call_tool("well_log", arguments={"stress_load": 9, "clarity": 4})
    res = await mcp.call_tool("well_forge_precheck", arguments={"task_description": "Critical Deployment"})
    data = get_data(res)
    assert data["risk_level"] in ("AMBER", "RED")
    assert data["recommended_mode"] in ("draft_only", "pause")
    assert "final_authority" in data


async def _test_well_decision_classify_advisory_language():
    _write_canonical_state()
    res = await mcp.call_tool("well_decision_classify", arguments={"decision_class": "C5"})
    data = get_data(res)
    assert data["ok"] is True
    # Must not overclaim with BLOCKED / APPROVED
    assert "ADVISORY" in data["verdict"], f"Expected advisory verdict, got {data['verdict']}"


async def _test_well_niat_check_advisory_language():
    _write_canonical_state()
    res = await mcp.call_tool("well_niat_check", arguments={
        "intent": "Deploy production",
        "reversibility": "irreversible"
    })
    data = get_data(res)
    assert data["ok"] is True
    assert "ADVISORY" in data["readiness"], f"Expected advisory readiness, got {data['readiness']}"
    assert "ADVISORY" in data["recommendation"], f"Expected advisory recommendation, got {data['recommendation']}"


async def _test_well_bandwidth_advisory_language():
    _write_canonical_state()
    res = await mcp.call_tool("well_bandwidth_recommendation")
    data = get_data(res)
    assert data["ok"] is True
    # Must not command with LOCKED / FORBIDDEN
    assert "LOCKED" not in data.get("mode", ""), f"Expected non-commanding mode, got {data['mode']}"
    assert "forbidden" not in data, "Must not use 'forbidden' — use 'advised_against'"
    assert "advised_against" in data or "decision_classes_advised_against" in data


async def _test_well_forge_closeout_fatigue_increases():
    _write_canonical_state(metrics={
        "sleep": {"last_night_hours": 8, "sleep_debt_days": 0, "quality_score": 9},
        "stress": {"subjective_load": 2, "restlessness": 1},
        "cognitive": {"clarity": 10, "decision_fatigue": 5.0, "focus_durability": 9, "pressure_sources": {}},
        "metabolic": {"fasting_window_hours": 0, "perceived_stability": 10, "hydration_status": "STABLE"},
        "structural": {"pain_map": [], "movement_frequency_daily": 5},
    })
    res = await mcp.call_tool("well_forge_closeout", arguments={
        "task_description": "test",
        "outcome": "success",
        "errors_encountered": 0,
    })
    data = get_data(res)
    assert data["ok"] is True
    # Fatigue must increase after work (success costs 0.5)
    assert data["fatigue_delta"] > 0, f"Expected fatigue_delta > 0, got {data['fatigue_delta']}"
    assert data["new_fatigue"] > 5.0, f"Expected new_fatigue > 5.0, got {data['new_fatigue']}"


async def _test_well_init_error_no_leak():
    _write_canonical_state()
    res = await mcp.call_tool("well_init")
    data = get_data(res)
    # In test env, arifOS is not available; error must not leak paths
    if not data.get("ok", False):
        err = data.get("error", "")
        assert "arifOS" in err or "Vault bridge unavailable" in err, f"Safe error expected, got: {err}"
        assert "/root/" not in err, f"Path leak in error: {err}"
        assert "traceback" not in err.lower()


async def _test_health_endpoint_identity():
    from starlette.testclient import TestClient
    import uvicorn
    from fastmcp import FastMCP

    # We can't easily mount the HTTP app here, but we can test the handler directly
    _write_canonical_state()
    # The health_handler is defined inside __main__ block; test via is_well + state
    state = server_module._load_state()
    assert server_module.is_well(state) is True
    assert state.get("identity") == "WELL"
    assert state.get("authority") == "REFLECT_ONLY"


# ═══════════════════════════════════════════════════════════════════════════════
# Test Runners
# ═══════════════════════════════════════════════════════════════════════════════


def test_identity_invariants():
    test_identity_invariant_pass()
    test_identity_invariant_missing_identity()
    test_identity_invariant_missing_role()
    test_identity_invariant_low_delta_s()
    test_identity_invariant_low_peace2()
    test_identity_invariant_low_kappa_r()
    test_identity_invariant_rasa_false()
    test_identity_invariant_amanah_unlocked()
    test_identity_invariant_authority_overclaim()
    print("✅ All identity invariant tests passed")


def test_well_tools():
    asyncio.run(_test_well_tools_core())


async def _test_well_tools_core():
    await _test_well_state_reflect_only()
    await _test_well_log_green_path()
    await _test_well_check_floors_canonical()
    await _test_well_readiness_canonical()
    await _test_well_seal_vault()
    print("✅ Core tool tests passed")


def test_well_phase2_tools():
    asyncio.run(_test_well_phase2_core())


async def _test_well_phase2_core():
    await _test_input_validation()
    await _test_well_log_state_green()
    await _test_well_log_state_red()
    await _test_well_get_readiness()
    await _test_well_check_floor_w1()
    await _test_well_list_log()
    print("✅ Phase 2 tool tests passed")


def test_well_integration_fixes():
    asyncio.run(_test_integration_core())


async def _test_well_unknown_telemetry():
    print("\n🧪 Testing WELL UNKNOWN telemetry paths...")

    # Write state with EMPTY metrics but valid identity
    _write_canonical_state(
        metrics={},
        well_score=50,
        floors_violated=[],
        truth_status="UNVERIFIED"
    )

    # 1. well_check_floors must return UNKNOWN, not PASS/GREEN
    print("\n--- Testing well_check_floors (no telemetry) ---")
    res = await mcp.call_tool("well_check_floors")
    data = get_data(res)
    print(f"Result: {data}")
    assert data["domain_verdict"] == "UNKNOWN_TELEMETRY"
    assert data["risk_level"] == "UNKNOWN"
    assert data["recommended_mode"] == "draft_only"

    # 2. well_readiness must return UNKNOWN
    print("\n--- Testing well_readiness (no telemetry) ---")
    res = await mcp.call_tool("well_readiness")
    data = get_data(res)
    print(f"Result: {data}")
    assert data["domain_verdict"] == "UNKNOWN"
    assert data["risk_level"] == "UNKNOWN"
    assert data["confidence"] == "LOW"

    # 3. well_arifos_packet must redact operator_snapshot
    print("\n--- Testing well_arifos_packet (no telemetry) ---")
    res = await mcp.call_tool("well_arifos_packet")
    data = get_data(res)
    print(f"Result: {data}")
    assert data["readiness"] == "UNKNOWN"
    assert data["has_telemetry"] is False
    snap = data.get("operator_snapshot", {})
    assert snap.get("clarity") is None
    assert snap.get("decision_fatigue") is None

    # 4. well_forge_precheck must return UNKNOWN_TELEMETRY
    print("\n--- Testing well_forge_precheck (no telemetry) ---")
    res = await mcp.call_tool("well_forge_precheck", arguments={"task_description": "test"})
    data = get_data(res)
    print(f"Result: {data}")
    assert data["domain_verdict"] == "UNKNOWN_TELEMETRY"
    assert data["risk_level"] == "UNKNOWN"

    # 5. well_bandwidth_recommendation must return UNKNOWN
    print("\n--- Testing well_bandwidth_recommendation (no telemetry) ---")
    res = await mcp.call_tool("well_bandwidth_recommendation")
    data = get_data(res)
    print(f"Result: {data}")
    assert data["verdict"] == "UNKNOWN"
    assert data["has_telemetry"] is False

    # 6. well_daily_brief must return UNKNOWN
    print("\n--- Testing well_daily_brief (no telemetry) ---")
    res = await mcp.call_tool("well_daily_brief")
    data = get_data(res)
    print(f"Result: {data}")
    assert data["readiness"] == "UNKNOWN"
    assert data["has_telemetry"] is False

    # 7. well_check_floor W1 must return UNKNOWN
    print("\n--- Testing well_check_floor W1 (no telemetry) ---")
    res = await mcp.call_tool("well_check_floor", arguments={"floor_id": "W1"})
    data = get_data(res)
    print(f"Result: {data}")
    assert data["domain_verdict"] == "UNKNOWN_TELEMETRY"

    # 8. well_get_readiness must return UNKNOWN tier
    print("\n--- Testing well_get_readiness (no telemetry) ---")
    res = await mcp.call_tool("well_get_readiness")
    data = get_data(res)
    print(f"Result: {data}")
    assert data["readiness"]["tier"] == "UNKNOWN"
    assert data["has_telemetry"] is False

    print("✅ UNKNOWN telemetry tests passed")


async def _test_integration_core():
    await _test_well_coupled_readiness()
    await _test_well_forge_precheck_conservative()
    await _test_well_decision_classify_advisory_language()
    await _test_well_niat_check_advisory_language()
    await _test_well_bandwidth_advisory_language()
    await _test_well_forge_closeout_fatigue_increases()
    await _test_well_init_error_no_leak()
    await _test_health_endpoint_identity()
    print("✅ Integration fix tests passed")


async def _test_canonical_tools():
    print("\n🧪 Testing WELL Canonical 13 tools...")

    _write_canonical_state()

    # WELL-01 well_get_health
    print("\n--- well_get_health ---")
    res = await mcp.call_tool("well_get_health")
    data = get_data(res)
    assert data["identity"] == "WELL"
    assert data["authority"] == "REFLECT_ONLY"
    assert data["verdict"] in ("WELL_PASS", "PASS")

    # WELL-02 well_get_state
    print("\n--- well_get_state ---")
    res = await mcp.call_tool("well_get_state")
    data = get_data(res)
    assert data["ok"] is True
    assert data["has_telemetry"] is True
    res = await mcp.call_tool("well_get_state", arguments={"domain": "machine"})
    data = get_data(res)
    assert "m_machine" in data

    # WELL-03 well_check_invariant (identity + floors)
    print("\n--- well_check_invariant ---")
    res = await mcp.call_tool("well_check_invariant")
    data = get_data(res)
    assert data["identity_verdict"] == "WELL_PASS"
    res = await mcp.call_tool("well_check_invariant", arguments={"floor_id": "W0"})
    data = get_data(res)
    assert data["floor"] == "W0"

    # WELL-04 well_log_signal (human)
    print("\n--- well_log_signal (human) ---")
    res = await mcp.call_tool("well_log_signal", arguments={
        "domain": "human",
        "signal": "clarity",
        "value": 8,
        "note": "Canonical test"
    })
    data = get_data(res)
    assert data["ok"] is True

    # WELL-04 well_log_signal (machine)
    print("\n--- well_log_signal (machine) ---")
    res = await mcp.call_tool("well_log_signal", arguments={
        "domain": "machine",
        "signal": "tool_availability",
        "value": 0.95,
    })
    data = get_data(res)
    assert data["ok"] is True

    # WELL-05 well_list_events
    print("\n--- well_list_events ---")
    res = await mcp.call_tool("well_list_events", arguments={"limit": 5, "redact": True})
    data = get_data(res)
    assert data["ok"] is True
    assert data.get("redacted") is True

    # WELL-06 well_reflect_trend
    print("\n--- well_reflect_trend ---")
    res = await mcp.call_tool("well_reflect_trend")
    data = get_data(res)
    assert data["ok"] is True

    # WELL-07 well_reflect_readiness (coupled)
    print("\n--- well_reflect_readiness ---")
    res = await mcp.call_tool("well_reflect_readiness", arguments={"domain": "coupled"})
    data = get_data(res)
    # coupled returns canonical verdict (mcp, task, status) not ok wrapper
    assert data.get("ok") is True or data.get("mcp") == "AFWELL"

    # WELL-08 well_suggest_mode
    print("\n--- well_suggest_mode ---")
    res = await mcp.call_tool("well_suggest_mode", arguments={"domain": "forge", "task_description": "test"})
    data = get_data(res)
    assert data.get("ok") or data.get("mcp") == "AFWELL"

    # WELL-09 well_suggest_recovery
    print("\n--- well_suggest_recovery ---")
    res = await mcp.call_tool("well_suggest_recovery")
    data = get_data(res)
    assert data["ok"] is True

    # WELL-10 well_reflect_niat
    print("\n--- well_reflect_niat ---")
    res = await mcp.call_tool("well_reflect_niat", arguments={"intent": "Deploy to production"})
    data = get_data(res)
    assert data["ok"] is True

    # WELL-11 well_classify_task
    print("\n--- well_classify_task ---")
    res = await mcp.call_tool("well_classify_task", arguments={"decision_class": "C2"})
    data = get_data(res)
    assert data["ok"] is True

    # WELL-12 well_get_packet
    print("\n--- well_get_packet ---")
    res = await mcp.call_tool("well_get_packet", arguments={"target": "arifos", "detail": "minimal"})
    data = get_data(res)
    assert data["ok"] is True

    # WELL-13 well_request_anchor (dry_run)
    print("\n--- well_request_anchor (dry_run) ---")
    res = await mcp.call_tool("well_request_anchor", arguments={"dry_run": True})
    data = get_data(res)
    assert data["ok"] is True
    assert data["dry_run"] is True

    print("✅ Canonical 13 tests passed")


def test_well_unknown_telemetry():
    asyncio.run(_test_well_unknown_telemetry())


def test_canonical_tools():
    asyncio.run(_test_canonical_tools())


if __name__ == "__main__":
    try:
        test_identity_invariants()
        test_well_tools()
        test_well_phase2_tools()
        test_well_integration_fixes()
        test_well_unknown_telemetry()
        test_canonical_tools()
        print("\n✅ All AFWELL Audit tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
