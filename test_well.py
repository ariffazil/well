import sys
import asyncio
import json
from pathlib import Path

# Add the WELL directory to sys.path so we can import the mcp object
well_dir = Path(__file__).parent
sys.path.append(str(well_dir))

from server import mcp

def get_data(result):
    """Helper to extract dict from ToolResult."""
    if hasattr(result, "structured_content") and result.structured_content:
        return result.structured_content
    if hasattr(result, "content") and result.content:
        return json.loads(result.content[0].text)
    return {}

async def test_well_tools():
    print("🧪 Testing WELL MCP Server tools...")
    
    # 1. Test well_state
    print("\n--- Testing well_state ---")
    res = await mcp.call_tool("well_state")
    data = get_data(res)
    print(f"Result: {data}")
    assert data["ok"] is True
    
    # 2. Test well_check_floors
    print("\n--- Testing well_check_floors ---")
    res = await mcp.call_tool("well_check_floors")
    data = get_data(res)
    print(f"Result: {data}")
    assert data["ok"] is True
    
    # 3. Test well_readiness
    print("\n--- Testing well_readiness ---")
    res = await mcp.call_tool("well_readiness")
    data = get_data(res)
    print(f"Result: {data}")
    assert data["ok"] is True
    
    # 4. Test well_log
    print("\n--- Testing well_log ---")
    res = await mcp.call_tool("well_log", arguments={"note": "Automated test run"})
    data = get_data(res)
    print(f"Result: {data}")
    assert data["ok"] is True
    
    # 5. Test well_anchor
    print("\n--- Testing well_anchor ---")
    # Using force=True to ensure it writes even if score delta is small
    res = await mcp.call_tool("well_anchor", arguments={"force": True})
    data = get_data(res)
    print(f"Result: {data}")
    # anchor might fail if arifOS budget is not set, but ok=False is a valid tool response
    print(f"Anchor success: {data.get('ok')}")

async def test_well_phase2_tools():
    print("\n🧪 Testing WELL Phase 2 tools...")
    
    # 1. Test well_log_state (Green path)
    print("\n--- Testing well_log_state (GREEN) ---")
    res = await mcp.call_tool("well_log_state", arguments={
        "sleep_hours": 8,
        "stress_level": 2,
        "clarity_score": 9,
        "note": "Test Green Path"
    })
    data = get_data(res)
    print(f"Result: {data}")
    assert data["tier"] == "GREEN"
    
    # 2. Test well_get_readiness
    print("\n--- Testing well_get_readiness ---")
    res = await mcp.call_tool("well_get_readiness")
    data = get_data(res)
    print(f"Result: {data}")
    assert data["ok"] is True
    assert "readiness" in data
    
    # 3. Test well_log (RED Path - complex)
    print("\n--- Testing well_log (RED - Multiple Violations) ---")
    # Using well_log directly to pass complex metrics
    res = await mcp.call_tool("well_log", arguments={
        "sleep_hours": 2,
        "sleep_debt_days": 5, # W1 Violation
        "stress_load": 10,
        "clarity": 2,         # W5 Violation
        "decision_fatigue": 9,
        "note": "Test Red Path - Extreme Stress"
    })
    data = get_data(res)
    print(f"Result: {data}")
    # With these penalties:
    # sleep: (7-2)*3 = 15
    # sleep_debt: min(5*8, 24) = 24
    # clarity: (8-2)*2 = 12
    # fatigue: 9 * 1.5 = 13.5
    # stress: 10 * 1.2 = 12
    # Total: 15+24+12+13.5+12 = 76.5
    # Score: 100 - 76.5 = 23.5 (< 40)
    assert data["tier"] == "RED"
    assert data["human_decision_required"] is True
    assert "W1_SLEEP_DEBT" in data["floors_violated"]
    assert "W5_COGNITIVE_ENTROPY" in data["floors_violated"]
    
    # 4. Test well_check_floor
    print("\n--- Testing well_check_floor (W1) ---")
    res = await mcp.call_tool("well_check_floor", arguments={"floor_id": "W1"})
    data = get_data(res)
    print(f"Result: {data}")
    assert data["floor"] == "W1"
    assert data["status"] == "VIOLATED"
    
    # 5. Test well_list_log
    print("\n--- Testing well_list_log ---")
    res = await mcp.call_tool("well_list_log", arguments={"limit": 5})
    data = get_data(res)
    print(f"Result: {data}")
    assert data["ok"] is True
    assert len(data["entries"]) > 0
    
    # 6. Test well_seal_vault
    print("\n--- Testing well_seal_vault ---")
    res = await mcp.call_tool("well_seal_vault", arguments={"force": True})
    data = get_data(res)
    print(f"Result: {data}")

if __name__ == "__main__":
    try:
        asyncio.run(test_well_tools())
        asyncio.run(test_well_phase2_tools())
        print("\n✅ All Phase 2 tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
