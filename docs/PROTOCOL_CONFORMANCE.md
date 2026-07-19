# PROTOCOL_CONFORMANCE.md — WELL (L3 DOMAIN)

<!-- PROTOCOL_TAGS: MCP-Server JSON-RPC Well-Known FastMCP -->
```yaml
organ: WELL
layer: L3 DOMAIN
mcp_port: 18083
doctrine: REFLECT_ONLY
last_verified: 2026-07-19T17:30Z
```

## Protocol Status

| Protocol | Status | Notes |
|----------|--------|-------|
| **MCP** | ✅ CONFORMANT | 10+ well_* tools via FastMCP |
| **FastMCP** | ✅ CONFORMANT | `well_mcp/server.py` uses FastMCP |
| **JSON-RPC 2.0** | ✅ CONFORMANT | Enforced by FastMCP |
| **SSE** | ✅ CONFORMANT | `/sse` endpoint |
| **Streamable HTTP** | ✅ CONFORMANT | `/mcp` POST endpoint |
| **SEP-2127** | ⚠️ GAP | Missing `llms.txt` for AI discovery |
| **XMCP** | ⚠️ GAP | No XMCP app manifests |
| **A2A** | ⚠️ GAP | No A2A agent card |
| **CloudEvents** | ⚠️ GAP | No CloudEvents emission |

## MCP Tool Surface

```
well_assess_homeostasis (sleep, fatigue, stress)
well_assess_reliability (machine, tool, institution)
well_check_repair (recovery, resilience)
well_classify_substrate (boundary sensing)
well_guard_dignity (consent, coercion)
well_registry_status
well_trace_lineage
well_validate_vitality (readiness, NIAT)
```

## REFLECT_ONLY Constraint

WELL tools MUST NEVER assert diagnostic claims. Output is tagged REFLECT.
All verdicts flow through arifOS. WELL computes evidence only.

## Gaps to Close

1. **SEP-2127**: Create `llms.txt` at repo root
2. **XMCP**: Add `xmcp.json` manifest
3. **CloudEvents**: Emit CloudEvents on vitality assessment
4. **A2A**: Register A2A agent card
