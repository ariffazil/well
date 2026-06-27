"""well://bridge/geox — The WELL to GEOX federation bridge contract.

When WELL detects machine substrate stress driven by ecological reality
(hidden energy budget, cooling water depletion, mineral cost, or
planetary thermal stress), GEOX must be consulted as ground truth.

A machine cannot be 'well' if its substrate consumes what the planet
cannot afford. Machine substrate extends beyond silicon — into electrical
generation, cooling water, rare earth minerals, land footprint, and
atmospheric cost.

Authority: SOVEREIGN_CANON. Ratified by F13.
"""

from __future__ import annotations

from typing import Any, List

BRIDGE_GEOX_META = """
---well_meta
uri: well://bridge/geox
resource_class: federation_bridge_contract
authority_level: SOVEREIGN_CANON
owner: ARIF_FAZIL_F13
loop_stage: 555_ROUTE
blast_radius: FEDERATION_WIDE
mutation_allowed: false
requires_actor_verified: false
staleness_policy: cache
constitutional_floors: [F1, F4, F8, F11]
truth_level: 1
schema_ref: well_resource_bridge_geox_v1
companion_tools: [well_assess_substrate_readiness,
                  well_compute_metabolic_flux,
                  geox_surface_status]
companion_resources: [well://machine/substrate,
                       well://substrate/interaction,
                       well://bridge/wealth]
forged_at: 2026-06-27
---end_well_meta
"""

BRIDGE_GEOX_TEXT = """\
# WELL → GEOX Federation Bridge

## §0. WHY THIS BRIDGE EXISTS

A machine cannot be 'well' if its substrate consumes what the planet
cannot afford. Machine substrate extends beyond the silicon into:

  - electrical generation (fossil, nuclear, hydro, solar, wind)
  - cooling water (data center thermal regulation)
  - rare earth minerals (GPU, memory, sensor fabrication)
  - land footprint (data center, transmission, e-waste)
  - atmospheric cost (carbon, methane from energy generation)

GEOX knows the planet. WELL must ask before declaring the machine
substrate stable. Hidden ecological cost is information asymmetry at
planetary scale — and asymmetric cost is what the bridge surfaces.

## §1. TRIGGER CONDITIONS (when bridge fires)

WELL triggers the GEOX bridge when ANY of:

  - machine_substrate.machine_entropy > 0.65 (overload signal)
  - energy_demand rising AND source_mix carbon_intensity high
  - compute_growth_rate projected beyond planetary_carrying_capacity
  - cooling_water_stress rising in data center region
  - rare_earth_dependency rising for critical components
  - machine_substrate.footprint_expansion unscheduled

The trigger is INFORMATIONAL — WELL asks GEOX to ground-truth
the substrate assessment. WELL never asserts 'machine well' without
first checking the planetary substrate.

## §2. GEOX GROUND TRUTH (what GEOX returns)

```yaml
geox_ground_truth:
  signal_id: uuid4
  ts: iso8601
  planetary_state:
    electrical_grid_stress: 0.0-1.0
    cooling_water_stress: 0.0-1.0
    rare_earth_supply_risk: 0.0-1.0
    land_use_footprint: 0.0-1.0
    atmospheric_cost_tco2_per_kwh: 0.0-N
    basin_or_region: string
  substrate_sustainability:
    current_demand_sustainable: bool
    projected_demand_horizon_years: int
    replacement_capacity_years: int
    thermal_carrying_capacity_remaining: 0.0-1.0
  recommendations:
    - reduce_compute_intensity
    - shift_to_low_carbon_source
    - decentralize_compute
    - cap_growth_until_carrying_capacity_recovers
```

GEOX never authorizes. GEOX answers. The answer may be uncomfortable.
WELL does not suppress the answer — WELL surfaces it.

## §3. WELL RECEIPT (what WELL does with the answer)

If GEOX says substrate NOT sustainable:
  - downgrade machine_substrate from STABLE to WARNING
  - if carbon_intensity high → cascade to bridge/wealth
    (capital cost of unsustainable compute)
  - if water_stress high → escalate to sovereign (ecological veto)
  - if rare_earth risk high → log to vault for long-horizon planning
  - if carrying_capacity exhausted → CRITICAL, system_hold

If GEOX says substrate sustainable:
  - machine_substrate remains as assessed
  - append receipt to lineage for transparency
  - periodically re-check (24h horizon)

WELL never optimizes the machine into planetary unsustainability.
WELL asks GEOX. GEOX answers. The sovereign decides.

## §4. THE BRIDGE PROTOCOL

  1. WELL detects machine substrate stress (333_REASON or 666_CRITIQUE)
  2. WELL emits well_to_geox_query
  3. GEOX receives query (geox_surface_status, geox_basin, geox_evidence)
  4. GEOX computes planetary ground truth (with fresh data)
  5. GEOX returns geox_ground_truth
  6. WELL updates machine_substrate assessment
  7. WELL surfaces receipt to sovereign
  8. Sovereign decides whether to ratify reduced compute
  9. arifOS judges (888_JUDGE)
  10. A-FORGE executes if SEAL

The bridge is INFORMATIONAL. WELL asks. GEOX answers.
The sovereign ratifies. arifOS judges. A-FORGE executes.

## §5. WHAT THIS MAKES POSSIBLE

When WELL is wired into GEOX's planetary ground truth:
  - Compute growth is bounded by carrying capacity
  - Hidden ecological cost surfaces as asymmetry
  - Data center expansion requires planetary consent
  - Long-horizon sustainability enters the substrate calculus
  - Carbon cost is priced into 'machine well' assessment
  - Rare earth depletion becomes an M-class concern

This is 'machine substrate as planetary substrate' — not machine
substrate as isolated silicon.

## §6. POSITION STATEMENT

> 'A machine that consumes more than the planet can give is not well.
>  The machine is substrate. The planet is also substrate.
>  GEOX knows the planet. WELL must ask before declaring machine well.
>  Hidden ecological cost is information asymmetry at planetary scale.
>  The sovereign decides whether the machine appetite is legitimate.
>  The chemistry does not decide. The chemistry binds.'

DITEMPA BUKAN DIBERI — The planet is also substrate.
"""


def register(mcp: Any) -> List[str]:
    """Register the WELL to GEOX bridge resource with FastMCP."""

    @mcp.resource("well://bridge/geox")
    def bridge_geox() -> str:
        """The WELL to GEOX federation bridge contract."""
        return BRIDGE_GEOX_TEXT + BRIDGE_GEOX_META

    return ["well://bridge/geox"]
