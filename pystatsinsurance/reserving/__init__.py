"""Loss reserving methods for general (P&C) insurance.

Chain-ladder projection of a cumulative-claims run-off triangle to ultimate,
yielding development factors, the completed triangle, ultimates, and reserves.

Validates against: Mack (1993) textbook triangle.
"""

from pystatsinsurance.reserving._chain_ladder import chain_ladder
from pystatsinsurance.reserving._common import ChainLadderResult

__all__ = [
    "ChainLadderResult",
    "chain_ladder",
]
