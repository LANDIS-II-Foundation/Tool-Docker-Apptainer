# Docker-LANDIS-II-v7-release

LANDIS-II v7 (Ubuntu 22.04) with a fixed, tested set of extensions defined in [`extensions-v7-release.yaml`](../extensions-v7-release.yaml).

**For users:** pull the pre-built image (no build step required).
**For developers:** build the image locally using the instructions below.

## Quick start: use the pre-built image

```shell
docker pull ghcr.io/landis-ii-foundation/landis-ii-v7-release:ubuntu-latest
```

> 💡 **Tags:** `:ubuntu-latest`, `:latest`, and `:main` all point to the same image (Ubuntu 22.04 — the only supported OS for v7).
> `:main` is retained for backwards compatibility.

Then run a simulation (replace the path with your scenario folder):

```shell
## Linux / macOS
docker run --rm \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="/path/to/your/scenario",dst=/scenarioFolder \
  ghcr.io/landis-ii-foundation/landis-ii-v7-release:ubuntu-latest \
  /bin/sh -c "cd /scenarioFolder && dotnet \$LANDIS_CONSOLE scenario.txt"

## Windows (PowerShell)
docker run --rm `
  --cpus=4 `
  --memory=64g `
  --mount type=bind,src="C:\path\to\your\scenario",dst=/scenarioFolder `
  ghcr.io/landis-ii-foundation/landis-ii-v7-release:ubuntu-latest `
  /bin/sh -c "cd /scenarioFolder && dotnet `$LANDIS_CONSOLE scenario.txt"
```

## Included extensions

See [`extensions-v7-release.yaml`](../extensions-v7-release.yaml) and [`libraries-v7-release.yaml`](../libraries-v7-release.yaml) for the exact commit SHAs used.

**Succession**

| Extension |
| --------- |
| Age-Only Succession |
| Biomass Succession |
| ForCS Succession |
| NECN Succession |
| PnET Succession |

**Disturbance and other**

| Extension |
| --------- |
| Base BDA |
| Base Fire |
| Base Harvest |
| Base Wind |
| BFOLDS Fire (precompiled DLL — source not yet open) |
| Biomass Browse |
| Biomass Harvest |
| Biomass Hurricane |
| Dynamic Biomass Fuels |
| Dynamic Fire System |
| Dynamic Fuel System |
| Land Use Plus |
| LinearWind |
| Root Rot |
| Social Climate Fire |
| SOSIEL Harvest |
| Forest Roads Simulation |
| Magic Harvest |

**Output**

| Extension |
| --------- |
| Output Biomass |
| Output Biomass By Age |
| Output Biomass Community |
| Output Biomass (PnET) |
| Output Biomass Reclass |
| Output Cohort Statistics |
| Output Landscape Habitat |
| Output Max Species Age |
| Output Wildlife Habitat |
| Local Habitat Suitability Output |

## Enhancements over `landis-ii-v7-linux`

This image supersedes `Clean_Docker_LANDIS-II_7_AllExtensions` with the following improvements:

- LANDIS-II placed at `/opt/landis-ii` (standard location for third-party software);
- extension and library versions defined in shared `*.yaml` files, not hardcoded in the Dockerfile;
- shared `.csproj` files for Forest Roads and Magic Harvest extensions (`extension_files_v7/`);
- build scripts rewritten in `bash`, shared in `scripts/`, reusable across image flavours;
- `yq` used to parse yaml; `xmlstarlet` used to edit `.csproj` XML;
- shared tests (`tests/`) run as part of the build;

## Build the image

Build from the repository root so that shared files (`extension_files_v7/`, `scripts/`, `*.yaml`) are available.

### Linux / macOS (bash)

```shell
cd ~/Tool-Docker-Apptainer

docker build . \
  -f Docker-LANDIS-II-v7-release/Dockerfile \
  -t landis-ii-v7-release:release
```

### Windows (PowerShell)

```shell
cd ~/Tool-Docker-Apptainer

docker build . `
  -f Docker-LANDIS-II-v7-release/Dockerfile `
  -t landis-ii-v7-release:release
```

## Run a locally built container

Replace `landis-ii-v7-release:release` with `ghcr.io/landis-ii-foundation/landis-ii-v7-release:ubuntu-latest` if you pulled the pre-built image instead.

### Interactive container

#### Linux / macOS (bash)

```shell
docker run -it \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="/path/to/your/scenario",dst=/scenarioFolder \
  --name landis01 \
  landis-ii-v7-release:release
```

#### Windows (PowerShell)

```shell
docker run -it `
  --cpus=4 `
  --memory=64g `
  --mount type=bind,src="C:\path\to\your\scenario",dst=/scenarioFolder `
  --name landis01 `
  landis-ii-v7-release:release
```

### Non-interactive container (run a single simulation)

#### Linux / macOS (bash)

```shell
docker run --rm \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="/path/to/your/scenario",dst=/scenarioFolder \
  --name landis01 \
  landis-ii-v7-release:release \
  /bin/sh -c "cd /scenarioFolder && dotnet \$LANDIS_CONSOLE scenario.txt"
```

#### Windows (PowerShell)

```shell
docker run --rm `
  --cpus=4 `
  --memory=64g `
  --mount type=bind,src="C:\path\to\your\scenario",dst=/scenarioFolder `
  --name landis01 `
  landis-ii-v7-release:release `
  /bin/sh -c "cd /scenarioFolder && dotnet `$LANDIS_CONSOLE scenario.txt"
```
