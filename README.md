# PyStatsInsurance

**Actuarial and insurance statistical computing for Python.**

> **Status: `0.1.0` — first module shipped.** Chain-ladder reserving is
> available now; more actuarial methods are on the roadmap below.

PyStatsInsurance is part of the open-core PyStatistics family:

| Package | Layer |
|---|---|
| [`pystatistics`](https://github.com/sgcx-org/pystatistics) | Fundamental, general statistics |
| [`pystatsbio`](https://github.com/sgcx-org/pystatsbio) | Biotech / pharma statistics |
| [`pystatsclinical`](https://github.com/sgcx-org/pystatsclinical) | Clinical-trial / clinical-research statistics |
| [`pystatsgenomic`](https://github.com/sgcx-org/pystatsgenomic) | Genomics / computational-biology statistics |
| [`pystatsfinance`](https://github.com/sgcx-org/pystatsfinance) | Financial / quantitative statistics |
| **`pystatsinsurance`** | Actuarial / insurance statistics |

Like its siblings, it builds on `pystatistics` for the general statistical layer
and adds methods specific to actuarial and insurance work.

## What's available now (0.1.0)

**Chain-ladder loss reserving** from a cumulative-claims development triangle
(unknown lower-right entries marked `NaN`):

```python
import numpy as np
from pystatsinsurance import reserving

triangle = np.array([
    [100.0, 150.0, 180.0],
    [110.0, 165.0, np.nan],
    [120.0, np.nan, np.nan],
])
result = reserving.chain_ladder(triangle)
print(result.summary())
```

`chain_ladder` computes volume-weighted age-to-age development factors, the
completed triangle, ultimate claims per origin period, and the outstanding
reserve per origin period and in total. It fails loud on a ragged / non-2×2 /
negative triangle and when a development factor cannot be derived.

## Roadmap (candidates, not commitments)

- Mack chain-ladder (reserve standard error) and Bornhuetter–Ferguson reserving.
- Frequency / severity loss models and aggregate-loss distributions.
- Credibility theory and life-actuarial methods.

## Installation

```bash
pip install pystatsinsurance
```

## License

MIT © Hai-Shuo. Part of the [SGCX](https://sgcx.org) open-core ecosystem.
