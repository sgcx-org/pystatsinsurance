"""Chain-ladder loss reserving from a cumulative development triangle.

The chain-ladder method projects a run-off triangle of cumulative claims to
ultimate using volume-weighted age-to-age development factors, then derives the
outstanding reserve per origin period as ultimate minus latest paid.

Reference
---------
Mack T. "Distribution-free calculation of the standard error of chain ladder
reserve estimates." ASTIN Bulletin 1993; 23:213-225. (Mack's variance is a
natural follow-up, not computed here.)
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

from pystatsinsurance.reserving._common import ChainLadderResult


def _validate_triangle(triangle: ArrayLike) -> tuple[NDArray, NDArray]:
    """Validate the input and return (float triangle, per-row known counts).

    Raises
    ------
    ValueError
        If the input is not 2-D, is smaller than 2x2, contains negative known
        values, or the known region is not a valid (staircase) run-off triangle.
    """
    tri = np.asarray(triangle, dtype=np.float64)
    if tri.ndim != 2:
        raise ValueError(f"triangle must be 2-dimensional, got {tri.ndim}-D")
    n_origin, n_dev = tri.shape
    if n_origin < 2 or n_dev < 2:
        raise ValueError(
            f"triangle must be at least 2x2 to derive factors, got {tri.shape}"
        )

    known = ~np.isnan(tri)
    if np.any(tri[known] < 0):
        raise ValueError("triangle must not contain negative cumulative values")

    counts = np.empty(n_origin, dtype=np.int64)
    for i in range(n_origin):
        row_known = known[i]
        k = int(np.sum(row_known))
        # Known cells must form a leading prefix (no gaps / no NaN before data).
        if not np.all(row_known[:k]) or np.any(row_known[k:]):
            raise ValueError(
                f"row {i} is ragged: known cells must be a contiguous prefix "
                "(NaN may appear only at the right end)"
            )
        counts[i] = k

    if counts[0] < 1:
        raise ValueError("the first origin row has no data")
    if np.any(np.diff(counts) > 0):
        raise ValueError(
            "not a valid run-off triangle: the number of known development "
            "periods must not increase from one origin row to the next"
        )
    return tri, counts


def _development_factors(tri: NDArray, counts: NDArray) -> NDArray:
    """Volume-weighted age-to-age factors (all-years weighted average)."""
    n_dev = tri.shape[1]
    factors = np.empty(n_dev - 1, dtype=np.float64)
    for j in range(n_dev - 1):
        # Rows that know both development period j and j+1.
        contributing = counts >= j + 2
        if not np.any(contributing):
            raise ValueError(
                f"cannot derive a development factor for period {j}->{j + 1}: "
                "no origin row has both periods observed"
            )
        denom = float(np.sum(tri[contributing, j]))
        if denom == 0.0:
            raise ValueError(
                f"cannot derive a development factor for period {j}->{j + 1}: "
                "cumulative claims at the earlier period sum to zero"
            )
        factors[j] = float(np.sum(tri[contributing, j + 1])) / denom
    return factors


def chain_ladder(triangle: ArrayLike) -> ChainLadderResult:
    """Project a cumulative-claims development triangle to ultimate.

    Parameters
    ----------
    triangle : array-like, shape (n_origin, n_dev)
        Cumulative claims triangle: rows are origin periods, columns are
        development periods. The unknown lower-right portion must be NaN. Known
        cells in each row must form a contiguous prefix, and the number of known
        periods must not increase down the rows (a standard run-off triangle).

    Returns
    -------
    ChainLadderResult
        Development factors, the completed triangle, ultimates, per-origin
        reserves, and the total reserve.

    Raises
    ------
    ValueError
        If the input is not a valid (non-ragged, non-negative, at-least-2x2)
        run-off triangle, or a development factor cannot be derived.
    """
    tri, counts = _validate_triangle(triangle)
    n_origin, n_dev = tri.shape

    factors = _development_factors(tri, counts)

    full = tri.copy()
    latest = np.empty(n_origin, dtype=np.float64)
    for i in range(n_origin):
        k = int(counts[i])
        latest[i] = full[i, k - 1]
        for j in range(k, n_dev):
            full[i, j] = full[i, j - 1] * factors[j - 1]

    ultimates = full[:, n_dev - 1].copy()
    reserves = ultimates - latest

    return ChainLadderResult(
        development_factors=factors,
        full_triangle=full,
        ultimates=ultimates,
        reserves=reserves,
        total_reserve=float(np.sum(reserves)),
        latest=latest,
    )
