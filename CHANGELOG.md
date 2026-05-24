# Changelog

## 0.1.1

### Documentation
- Expanded the README to document the chain-ladder module (`reserving`) with a
  usage example, and to list the full PyStatistics open-core ecosystem.


## 0.1.0

### Added
- `reserving` subpackage with `reserving.chain_ladder(triangle)`: the
  chain-ladder loss-reserving method on a cumulative-claims development
  triangle — volume-weighted age-to-age development factors, the completed
  (projected) triangle, ultimate claims per origin period, and the outstanding
  reserve per origin period and in total. Fails loud on a ragged / non-2x2 /
  negative triangle and when a development factor cannot be derived.

First feature release, promoting the package from a reserved skeleton.
