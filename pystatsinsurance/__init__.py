"""
PyStatsInsurance: Actuarial and insurance statistical computing.

Part of the PyStatistics open-core ecosystem (alongside ``pystatistics`` and
``pystatsbio``). Provides actuarial / insurance methods built on the general
statistical layer.

Usage:
    from pystatsinsurance import reserving
    result = reserving.chain_ladder(triangle)
"""

__version__ = "0.1.0"
__author__ = "Hai-Shuo"
__email__ = "contact@sgcx.org"

from pystatsinsurance import reserving

__all__ = [
    "__version__",
    "reserving",
]
