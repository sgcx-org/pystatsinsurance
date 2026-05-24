# Roadmap — pystatsinsurance

A working **checklist** of features that plausibly belong at the *actuarial /
insurance* layer (both P&C/general insurance and life). Tick items off as they
land, in roughly the way `pystatistics/docs/ROADMAP.md` tracks its modules.

**This list is not a commitment.** It captures *what kind of thing belongs here*
and in roughly what order we'd build it. Re-order, drop, or promote/demote
freely. Tiers are priority bands, not deadlines.

## Layer rules (the gate every item must pass)

- **Stay in this layer.** Only genuinely *actuarial / insurance* methods.
  General statistics (distributions, GLM, MLE) live in `pystatistics`;
  finance/market methods in `pystatsfinance`. **Don't duplicate VaR/TVaR — reuse
  `pystatsfinance`** if a generic risk measure is needed.
- **Build on `pystatistics`** — GLM for frequency/severity models, `montecarlo`
  for bootstrap reserving. Don't reimplement.
- **Promotion rule:** a mechanic shared by ≥2 separate domains (e.g.
  distribution fitting, extreme-value tails — also used by finance) is a
  candidate to promote to `pystatistics`. See *Ambiguous*.
- Conventions: `pystatsbio` Coding Bible, typed, ruff/mypy clean, tests, version
  bump via the release flow.

## Tier 1 — reserving core (P&C)

- [ ] **Chain-ladder reserving** — development factors, completed triangle,
  ultimates, reserves. *v0.1.0 target — full spec in
  [FIRST_FEATURES.md](FIRST_FEATURES.md).*
- [ ] **Frequency–severity loss summary** — claim frequency, severity, aggregate
  loss (leans on `pystatistics` descriptives). *See FIRST_FEATURES.md.*
- [ ] **Mack chain-ladder** — distribution-free standard error of reserve
  estimates (Mack 1993); the natural quantification follow-up to chain-ladder.
- [ ] **Bornhuetter–Ferguson & Cape Cod** — a-priori-based reserving methods to
  sit alongside chain-ladder.

## Tier 2 — reserving uncertainty & claim models

- [ ] **ODP bootstrap reserving** — over-dispersed Poisson bootstrap of the
  triangle for a predictive reserve distribution (consumes `pystatistics`
  montecarlo).
- [ ] **LDF selection / tail factors** — averaging methods and tail
  extrapolation for development factors.
- [ ] **Frequency models** — Poisson / Negative-Binomial framing for claim
  counts (GLM from `pystatistics`).
- [ ] **Severity distribution fitting** — fit lognormal / gamma / Pareto /
  Weibull to claim sizes. *(General dist-fitting — home is ambiguous, see
  below.)*

## Tier 3 — pricing, credibility, life

- [ ] **Aggregate loss distribution** — Panjer recursion / collective-risk
  (compound) model.
- [ ] **Credibility theory** — Bühlmann and Bühlmann–Straub, limited-fluctuation
  credibility.
- [ ] **Premium principles** — expected-value, variance, standard-deviation
  principles; Wang transform.
- [ ] **Life actuarial** — life tables, commutation functions, annuity /
  insurance present values; mortality laws (Gompertz–Makeham, Lee–Carter).
  *(Demography overlap — see below.)*
- [ ] **Reinsurance pricing** — excess-of-loss layer losses, increased-limit
  factors.

## Ambiguous — discuss before building

- **Severity distribution fitting (MLE of parametric distributions)** — this is
  a *general* primitive; finance also fits parametric return/loss distributions.
  **Decided: promote to `pystatistics`** as a generic `fitdist` (on its roadmap
  as a demand-driven primitive) — do *not* build it here. Implement in
  `pystatistics` when the first insurance severity feature needs it, then peg the
  new version; a thin actuarial severity wrapper can live here.
- **Extreme-value theory / GPD for large losses** — identical mechanic to
  finance tail risk. **Decided: promote to `pystatistics`** (on its roadmap as a
  demand-driven primitive); don't build it twice. Pull it in when the first
  large-loss feature needs it.
- **Tweedie GLM for ratemaking** — the Tweedie *family* is a general GLM family
  (`pystatistics`); the *ratemaking* framing is actuarial. Add the family to
  `pystatistics` and wrap here?
- **Risk measures (VaR / TVaR)** — ground rule says reuse `pystatsfinance`.
  Confirm the dependency direction (insurance → finance) is acceptable, vs.
  promoting the generic measure to `pystatistics`.
- **Life tables / mortality** — arguably demography rather than insurance proper.
  Keep here (actuarial use is dominant), or carve out separately?
