# Docker-LANDIS-II-v8-UCLv2-release

LANDIS-II v8 (Ubuntu 24.04 and 26.04) with extensions updated for **Universal Cohort Library (UCL) v2**, defined in [`extensions-v8-UCL2-release.yaml`](../extensions-v8-UCL2-release.yaml). UCL v2 fixes a significant biomass-removal bug present in earlier extensions — see the [warning in the main README](../README.md) for details.

> **Note:** Some extensions are still pending UCL v2 updates and are therefore not included: Land Use Plus, Output Wildlife Habitat, and Local Habitat Suitability Output. Use [`landis-ii-v8-release`](../Docker-LANDIS-II-v8-release/) if you need those extensions.

**For users:** pull the pre-built image (no build step required).
**For developers:** build the image locally using the instructions below.

## Quick start: use the pre-built image

```shell
docker pull ghcr.io/landis-ii-foundation/landis-ii-v8-uclv2-release:ubuntu-latest
```

> 💡 **Tags:** `:ubuntu-latest`, `:latest`, and `:main` all point to the most recent Ubuntu LTS build (currently Ubuntu 26.04).
> Use `:ubuntu-24.04` or `:ubuntu-26.04` to pin to a specific OS version.

Then run a simulation (replace the path with your scenario folder):

```shell
## Linux / macOS
docker run --rm \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="/path/to/your/scenario",dst=/scenarioFolder \
  ghcr.io/landis-ii-foundation/landis-ii-v8-uclv2-release:ubuntu-latest \
  /bin/sh -c "cd /scenarioFolder && dotnet \$LANDIS_CONSOLE scenario.txt"

## Windows (PowerShell)
docker run --rm `
  --cpus=4 `
  --memory=64g `
  --mount type=bind,src="C:\path\to\your\scenario",dst=/scenarioFolder `
  ghcr.io/landis-ii-foundation/landis-ii-v8-uclv2-release:ubuntu-latest `
  /bin/sh -c "cd /scenarioFolder && dotnet `$LANDIS_CONSOLE scenario.txt"
```

## Included extensions

See [`extensions-v8-UCL2-release.yaml`](../extensions-v8-UCL2-release.yaml),
[`support-libraries-v8-UCL2-release.yaml`](../support-libraries-v8-UCL2-release.yaml),
[`libraries-v8-UCL2-release-prebuild.yaml`](../libraries-v8-UCL2-release-prebuild.yaml), and
[`libraries-v8-release.yaml`](../libraries-v8-release.yaml) for the exact commit SHAs used.

**Succession**

| Extension |
| --------- |
| Biomass Succession |
| ForCS Succession |
| NECN Succession |
| PnET Succession |

**Disturbance and other**

| Extension |
| --------- |
| Base Fire |
| Base Wind |
| Biomass Harvest |
| Biomass Hurricane |
| Climate BDA |
| Dynamic Biomass Fuels |
| Dynamic Fire System |
| Social Climate Fire (SCRAPPLE) [^scrapple] |
| Forest Roads Simulation |
| Magic Harvest |

[^scrapple]: **Only usable with NECN and PnET succession.** Under ForCS Succession or
    Biomass Succession it crashes at extension load with a `NullReferenceException` in
    `SiteVars.InitializeDisturbances()`. SCRAPPLE reads fine fuels from
    `Succession.FineFuels`; when that site variable is unregistered it falls back to
    `Succession.Litter`, but assigns the result into `SiteVars.FineFuels[site]` — whose
    getter returns the same field it just found null — so the fallback dereferences null.
    NECN registers `Succession.FineFuels` directly and PnET registers it via
    `Library-PnET-Cohort`, so both take the working branch; ForCS and Biomass Succession
    register only `Succession.Litter`. This is an upstream SCRAPPLE bug, **not** a UCLv2
    issue: it reproduces on the UCLv1 pin used by `landis-ii-v8-release`, and is still
    present on upstream master as of v4.3. Fixing it upstream is a one-liner — allocate
    the site variable (`NewSiteVar<double>()`) before populating it from the litter pool.

**Output**

| Extension |
| --------- |
| Output Biomass |
| Output Biomass By Age |
| Output Biomass Community |
| Output Biomass PnET |
| Output Biomass Reclass |
| Output Cohort Statistics |
| Output Max Species Age |

### Forest Product Sector Module

The image also includes the [Forest Product Sector Module](https://github.com/LANDIS-II-Foundation/Extension-Forest-Product-Sector) (FPSM), pinned in [`extensions-v8-UCL2-release.yaml`](../extensions-v8-UCL2-release.yaml) as a `type: tool` entry, and installed in `build/Release`.
FPSM is not a plug-in and is not listed in a scenario file: run it after a ForC Succession simulation, from a folder holding the FPSM input file and the ForC flux logs it names (`HarvestFileLive`, `HarvestFileDOM`; relative paths resolve against that folder, where FPSM also writes its outputs).

```shell
docker run --rm \
  --mount type=bind,src="/path/to/your/scenario",dst=/scenarioFolder \
  ghcr.io/landis-ii-foundation/landis-ii-v8-uclv2-release:ubuntu-latest \
  /bin/sh -c "cd /scenarioFolder && dotnet \$LANDIS_FPS fps-input.txt"
```

## Enhancements over `landis-ii-v8-release`

This image builds on `Docker-LANDIS-II-v8-release` with the following addition:

- extensions updated for Universal Cohort Library (UCL) v2, fixing a biomass-removal bug;
- the extensions that read climate (NECN, PnET, Biomass Succession, Climate BDA, and
  Social Climate Fire) all use Climate Library v6;
- Forest Roads and Magic Harvest now build from their own SDK-style `.csproj`, patched by
  `scripts/update_csproj_*.sh` exactly like every other extension. The hand-maintained
  UCLv2 overrides that used to live in `extension_files/` were retired once those two
  repos converted to SDK-style projects; the UCLv1 images still use overrides, named by
  the `csproj:` field on a YAML entry;
- before building an extension, the build deletes the extension's committed copy of any
  DLL that `build/extensions` already holds (`EXT_DROP_SHADOWING_DLLS` in the Dockerfile),
  so the image ships the support libraries and extensions pinned in the `*.yaml` files.
  Without this, the `Landis.Library.UniversalCohorts-v2.dll` 1.3.0.0 that three
  extensions commit replaces the 2.0.1 copy from `Support-Library-Dlls-v8`; in 1.3.0.0,
  partial cohort removals (e.g. Biomass Harvest `(30%)`) remove nothing;

All other enhancements from `Docker-LANDIS-II-v8-release` also apply:

- Ubuntu 24.04 (noble) and 26.04 (resolute) base images, selectable via `--build-arg UBUNTU_VERSION=<version>`; defaults to 24.04;
- `dotnet` installed from the `apt` repositories;
- LANDIS-II placed at `/opt/landis-ii`;
- extension and library versions defined in shared `*.yaml` files;
- build scripts in `bash`, shared in `scripts/`;
- shared tests (`tests/`) run as part of the build;
- **multi-stage build** that ships only the .NET *runtime* and the compiled model:
  the .NET SDK, NuGet caches, cloned sources, and GDAL build/dev packages are all left
  behind in a throwaway build stage. The final image is **≈0.6 GB** (previously ≈4 GB),
  which matters most when converting to an Apptainer `.sif` for HPC use;

## Build the image

Build from the repository root so that shared files (`extension_files/`, `scripts/`, `*.yaml`) are available.

### Linux / macOS (bash)

```shell
cd ~/Tool-Docker-Apptainer

## Ubuntu 26.04 (resolute) — recommended
docker build . \
  -f Docker-LANDIS-II-v8-UCL2-release/Dockerfile \
  --build-arg UBUNTU_VERSION=26.04 \
  -t landis-ii-v8-uclv2-release:ubuntu-26.04

## Ubuntu 24.04 (noble)
docker build . \
  -f Docker-LANDIS-II-v8-UCL2-release/Dockerfile \
  --build-arg UBUNTU_VERSION=24.04 \
  -t landis-ii-v8-uclv2-release:ubuntu-24.04
```

### Windows (PowerShell)

```shell
cd ~/Tool-Docker-Apptainer

## Ubuntu 26.04 (resolute) — recommended
docker build . `
  -f Docker-LANDIS-II-v8-UCL2-release/Dockerfile `
  --build-arg UBUNTU_VERSION=26.04 `
  -t landis-ii-v8-uclv2-release:ubuntu-26.04

## Ubuntu 24.04 (noble)
docker build . `
  -f Docker-LANDIS-II-v8-UCL2-release/Dockerfile `
  --build-arg UBUNTU_VERSION=24.04 `
  -t landis-ii-v8-uclv2-release:ubuntu-24.04
```

> 💡 **Multi-stage build.** This Dockerfile builds in two stages: a `build` stage with the full
> .NET SDK and GDAL build dependencies that compiles and tests LANDIS-II, and a slim `runtime`
> stage (Ubuntu + the .NET runtime only) that becomes the final image. When customizing the image,
> add **runtime** dependencies (e.g. extra Python packages a scenario needs) to the `runtime` stage,
> and **build-time** dependencies (e.g. to compile an additional extension) to the `build` stage.

## Run a locally built container

Replace `landis-ii-v8-uclv2-release:ubuntu-26.04` with `ghcr.io/landis-ii-foundation/landis-ii-v8-uclv2-release:ubuntu-latest` if you pulled the pre-built image instead.

### Interactive container

#### Linux / macOS (bash)

```shell
docker run -it \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="/path/to/your/scenario",dst=/scenarioFolder \
  --name landis01 \
  landis-ii-v8-uclv2-release:ubuntu-26.04
```

#### Windows (PowerShell)

```shell
docker run -it `
  --cpus=4 `
  --memory=64g `
  --mount type=bind,src="C:\path\to\your\scenario",dst=/scenarioFolder `
  --name landis01 `
  landis-ii-v8-uclv2-release:ubuntu-26.04
```

### Non-interactive container (run a single simulation)

#### Linux / macOS (bash)

```shell
docker run --rm \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="/path/to/your/scenario",dst=/scenarioFolder \
  --name landis01 \
  landis-ii-v8-uclv2-release:ubuntu-26.04 \
  /bin/sh -c "cd /scenarioFolder && dotnet \$LANDIS_CONSOLE scenario.txt"
```

#### Windows (PowerShell)

```shell
docker run --rm `
  --cpus=4 `
  --memory=64g `
  --mount type=bind,src="C:\path\to\your\scenario",dst=/scenarioFolder `
  --name landis01 `
  landis-ii-v8-uclv2-release:ubuntu-26.04 `
  /bin/sh -c "cd /scenarioFolder && dotnet `$LANDIS_CONSOLE scenario.txt"
```
