"""WELL closed decision loop — sense → interpret → propose → (judge) → act ≤1 → verify → learn.

REFLECT_ONLY for human state. Mutations only via allowlisted catalogue + A_effective.
DITEMPA BUKAN DIBERI.
"""

from loop.state_envelope import build_state_envelope
from loop.a_effective import compute_a_effective
from loop.recommend import recommend
from loop.recovery_v1 import run_recovery_loop

__all__ = [
    "build_state_envelope",
    "compute_a_effective",
    "recommend",
    "run_recovery_loop",
]
