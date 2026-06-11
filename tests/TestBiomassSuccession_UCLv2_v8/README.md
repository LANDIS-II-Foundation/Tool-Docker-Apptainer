# TestBiomassSuccession_UCLv2_v8 (UCLv2)

A small Biomass Succession test scenario for the **`landis-ii-v8-uclv2-release`** (UCLv2) image.

The inputs are the upstream
[Extension-Biomass-Succession](https://github.com/LANDIS-II-Foundation/Extension-Biomass-Succession)
repository's own `testings/CoreV8.0-BiomassSuccession7.0` example, taken at the **commit this
image pins** for Biomass Succession in `extensions-v8-UCL2-release.yaml`
(`20610767`, which links against `Landis.Library.UniversalCohorts-v2`).
The companion `tests/TestBiomassSuccession_v8/` uses the UCLv1-vintage commit instead.
(The scenario/input format is unchanged between the two vintages; only the compiled
Universal-Cohorts library differs.)

It runs Biomass Succession + Output Biomass + Output Biomass Community for 50 years
(succession timestep 10), so the build does more than confirm the extension loads:

## Cohort-aging regression check

Output Biomass Community writes per-cell cohort lists
(`community-input-file-<time>.csv`, columns `MapCode, SpeciesName, CohortAge, ...`).
The Dockerfile asserts that the **maximum cohort age advances by ~the succession timestep
each step** (here ~+50 years over the 50-year run).

This guards against a real defect that shipped in earlier Biomass Succession v8 builds:
`GrowCohorts` passed the per-year `annualTimestep` flag as `true` only on sub-year `y == 1`,
so `Landis.Library.UniversalCohorts` (`if (annualTimestep) cohort.IncrementAge()`) advanced
cohort ages by **+1 per succession timestep instead of +1 per year**. The simulation otherwise
ran fine, so a plain smoke test did not catch it; only stand age / seral output exposed it.
It was fixed in the Biomass Succession spin-up overhaul (issue #53; the buggy lines remain in
the source commented with `WHERE DID THIS CODE COME FROM?  HUGE MYSTERY`). A stale extension
that reintroduced it would age cohorts by only ~+5 years over this run and fail the check.

## Running it manually

```sh
docker run --rm -v "$PWD":/work -w /work ghcr.io/for-cast/landis-ii-v8-uclv2-release:main \
  landis-ii-8 scenario.txt
```
