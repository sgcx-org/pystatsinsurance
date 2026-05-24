# PyStatsInsurance

**Actuarial and insurance statistical computing for Python.**

> **Status: early / reserved (`0.0.1`).** This package reserves the
> `pystatsinsurance` name within the **PyStatistics open-core ecosystem** and will
> grow into a full actuarial/insurance statistics library. The public API is
> forthcoming.

PyStatsInsurance is part of the open-core PyStatistics family:

| Package | Layer |
|---|---|
| [`pystatistics`](https://github.com/sgcx-org/pystatistics) | Fundamental, general statistics |
| [`pystatsbio`](https://github.com/sgcx-org/pystatsbio) | Biotech / pharma statistics |
| **`pystatsinsurance`** | Actuarial / insurance statistics |

Like its siblings, it builds on `pystatistics` for the general statistical layer
and adds methods specific to actuarial and insurance work.

## Planned scope (candidates, not commitments)

- Loss-model summaries (frequency / severity).
- Basic reserving (e.g. chain-ladder) and elementary risk measures.

## Installation

```bash
pip install pystatsinsurance
```

## License

MIT © Hai-Shuo. Part of the [SGCX](https://sgcx.org) open-core ecosystem.
