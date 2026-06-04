# Docker-LANDIS-II-v8-UCLv2-release

LANDIS-II v8 (Ubuntu 24.04 and 26.04) with extensions updated for **Universal Cohort Library (UCL) v2**, defined in [`extensions-v8-UCL2-release.yaml`](../extensions-v8-UCL2-release.yaml). UCL v2 fixes a significant biomass-removal bug present in earlier extensions — see the [warning in the main README](../README.md) for details.

> **Note:** Some extensions are still pending UCL v2 updates and are therefore not included. Extensions not yet updated include: PnET Succession, Base BDA, Dynamic Biomass Fuels, Dynamic Fire System, LinearWind, Forest Roads Simulation, Magic Harvest, Output Biomass (PnET), Output Wildlife Habitat, and Local Habitat Suitability Output. Use [`landis-ii-v8-release`](../Docker-LANDIS-II-v8-release/) if you need those extensions.

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

See [`extensions-v8-UCL2-release.yaml`](../extensions-v8-UCL2-release.yaml) and [`libraries-v8-release.yaml`](../libraries-v8-release.yaml) for the exact commit SHAs used.

**Succession**

| Extension |
| --------- |
| Biomass Succession |
| ForCS Succession |
| NECN Succession |

**Disturbance and other**

| Extension |
| --------- |
| Base Fire |
| Base Wind |
| Biomass Harvest |
| Biomass Hurricane |
| Land Use Plus |
| Social Climate Fire |
| Forest Roads Simulation |
| Magic Harvest |

**Output**

| Extension |
| --------- |
| Output Biomass |
| Output Biomass By Age |
| Output Biomass Community |
| Output Biomass Reclass |
| Output Cohort Statistics |
| Output Max Species Age |

## Enhancements over `landis-ii-v8-release`

This image builds on `Docker-LANDIS-II-v8-release` with the following addition:

- extensions updated for Universal Cohort Library (UCL) v2, fixing a biomass-removal bug;

All other enhancements from `Docker-LANDIS-II-v8-release` also apply:

- Ubuntu 24.04 (noble) and 26.04 (resolute) base images, selectable via `--build-arg UBUNTU_VERSION=<version>`; defaults to 24.04;
- `dotnet` installed from the `apt` repositories;
- LANDIS-II placed at `/opt/landis-ii`;
- extension and library versions defined in shared `*.yaml` files;
- shared `.csproj` files for Forest Roads and Magic Harvest extensions (`extension_files/`);
- build scripts in `bash`, shared in `scripts/`;
- shared tests (`tests/`) run as part of the build;

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
