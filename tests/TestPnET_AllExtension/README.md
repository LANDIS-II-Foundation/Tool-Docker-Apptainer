This is a simple test scenario created by Clement Hardy to test if the Docker image for LANDIS-II v8 resulting from the corresponding Dockerfile can run properly.

I've tried to put as much extensions working at the same time as possible to try to detect potential conflicts between extensions and libraries.

## Two scenario files, one set of inputs

| File | Used by | Difference |
| ---- | ------- | ---------- |
| `scenario.txt` | `landis-ii-v8-release` (and the R / RStudio images) | all extensions enabled |
| `scenario_UCLv2.txt` | `landis-ii-v8-uclv2-release` | Land Use Plus, Local Habitat Output and Wildlife Habitat Output commented out |

Those three are commented out of the UCLv2 scenario because that image does not ship them:
all but Land Use Plus have no UCL v2 update upstream yet, and Land Use Plus is excluded
while its upstream UCL v2 migration is unfinished (see issue #59). Re-enable them there as
they get their updates. The inputs are shared, so a change to the inputs affects both runs.

Beyond confirming the extensions load, the UCLv2 run exercises `Landis.Library.PnETCohorts-v2`
2.4.2, which that image builds from source (see `libraries-v8-UCL2-release-prebuild.yaml`).

## Harvest check (UCLv2 image only)

`scenario_UCLv2_harvest-check.txt` runs PnET-Succession, Biomass Harvest and Output Biomass
Community for 20 years. Biomass Harvest
(`inputs/disturbances/biomassHarvest/harvest_ClearcutAll_yr10.txt`) clear-cuts every stand,
and so all 259 active cells, at year 10. The Dockerfile then fails the build if the year-10
clear-cut removed no cohorts, or if any cohort in `community-input-file-20.csv` is older
than 20 years.

It guards against PnET keeping cohorts that a disturbance removed. With
`Landis.Library.PnETCohorts-v2` 2.3.0.0 and PnET-Succession before 6.1.2, other extensions
saw a copy of PnET's cohorts that was rebuilt every timestep. Harvest removed cohorts from
the copy, and the initial cohorts (then aged 30 to 100) came back.

## Running it manually

```sh
docker run --rm -v "$PWD":/work -w /work ghcr.io/for-cast/landis-ii-v8-uclv2-release:main \
  /bin/sh -c "dotnet \$LANDIS_CONSOLE scenario_UCLv2.txt"
```
