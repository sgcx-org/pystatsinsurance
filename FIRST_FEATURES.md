# First Features — pystatsinsurance

This package is currently a **reserved `0.0.1` skeleton**. This file specifies the
first 1–2 features a future session should implement to turn it into a real
`0.1.0` (the "harden later" step of SGC-Bio roadmap item B-3).

## Ground rules (read first)

- **Stay in this layer.** Only implement things that are genuinely *actuarial /
  insurance*. General statistics belong in `pystatistics`; finance/market
  methods belong in `pystatsfinance` (don't duplicate VaR here — if a generic
  risk measure is needed, prefer reusing it). Apply the "which-of-the-4-layers"
  test.
- **Build on `pystatistics`** for the general statistical layer; don't
  reimplement it.
- **Follow `pystatsbio`'s conventions** — hatchling packaging, the Coding Bible
  (`CLAUDE.md` there: fail loud, one job per module, tests first, deterministic),
  typed, ruff/mypy clean.
- **Ship with tests** (normal / edge / failure) and bump to `0.1.0` once landed.

## Feature 1 (primary): chain-ladder loss reserving

The canonical actuarial reserving method — well-specified, deterministic, and
unmistakably insurance.

- Suggested API: `chain_ladder(triangle) -> ChainLadderResult`
  - Input: a cumulative claims **development triangle** (2D array; rows = origin
    periods, cols = development periods; lower-right is unknown / NaN).
  - Compute: volume-weighted **age-to-age development factors**, the completed
    (projected) triangle, **ultimate** claims per origin period, and the
    **reserve** = ultimate − latest paid (latest diagonal), per origin and total.
- Result object fields: `development_factors, full_triangle, ultimates,
  reserves, total_reserve, summary`.
- Failure behavior (fail loud): reject a non-triangular / ragged input, negative
  cumulative values, or a triangle too small to derive factors.
- Reference: Mack T, "Distribution-free calculation of the standard error of
  chain ladder reserve estimates," ASTIN Bulletin 1993 (Mack's variance is a
  natural follow-up, not required for `0.1.0`).
- Tests: Mack's textbook triangle with known development factors / ultimates;
  reserve = ultimate − latest diagonal; the failure cases above.

## Feature 2 (optional secondary): frequency–severity loss summary

- Suggested API: `loss_summary(claim_counts, claim_amounts) -> LossSummary`
  — claim frequency, severity (mean/median/dispersion), and aggregate loss
  summary, leaning on `pystatistics` for the underlying descriptive stats.
