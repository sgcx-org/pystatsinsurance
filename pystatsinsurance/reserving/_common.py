"""Result type for chain-ladder loss reserving."""

from __future__ import annotations

from dataclasses import dataclass

from numpy.typing import NDArray


@dataclass(frozen=True)
class ChainLadderResult:
    """Output of the chain-ladder reserving method.

    Attributes
    ----------
    development_factors : NDArray
        Volume-weighted age-to-age development factors, length ``n_dev - 1``;
        element ``j`` projects cumulative claims from development period ``j`` to
        ``j + 1``.
    full_triangle : NDArray
        The completed (projected) cumulative-claims triangle, same shape as the
        input, with the lower-right unknowns filled in.
    ultimates : NDArray
        Projected ultimate cumulative claims per origin period.
    reserves : NDArray
        Outstanding reserve per origin period = ultimate - latest paid.
    total_reserve : float
        Sum of the per-origin reserves.
    latest : NDArray
        Latest paid (latest cumulative diagonal) per origin period.
    """

    development_factors: NDArray
    full_triangle: NDArray
    ultimates: NDArray
    reserves: NDArray
    total_reserve: float
    latest: NDArray

    def summary(self) -> str:
        """Human-readable summary."""
        lines = [
            "Chain-Ladder Reserving",
            "=" * 50,
            "Development factors: "
            + ", ".join(f"{f:.4f}" for f in self.development_factors),
            "",
            f"{'Origin':>6} {'Latest':>14} {'Ultimate':>14} {'Reserve':>14}",
        ]
        for i in range(self.ultimates.shape[0]):
            lines.append(
                f"{i:>6} {self.latest[i]:>14,.2f} "
                f"{self.ultimates[i]:>14,.2f} {self.reserves[i]:>14,.2f}"
            )
        lines.append("-" * 50)
        lines.append(f"{'Total reserve':>36}: {self.total_reserve:,.2f}")
        return "\n".join(lines)
