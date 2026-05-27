# Docker-LANDIS-II-v8-release

LANDIS-II v8 (Ubuntu 24.04) with a fixed, tested set of extensions defined in [`extensions-v8-release.yaml`](../extensions-v8-release.yaml).

**For users:** pull the pre-built image (no build step required).
**For developers:** build the image locally using the instructions below.

## Quick start: use the pre-built image

```shell
docker pull ghcr.io/landis-ii-foundation/landis-ii-v8-release:main
```

Then run a simulation (replace the path with your scenario folder):

```shell
## Linux / macOS
docker run --rm \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="/path/to/your/scenario",dst=/scenarioFolder \
  ghcr.io/landis-ii-foundation/landis-ii-v8-release:main \
  /bin/sh -c "cd /scenarioFolder && dotnet \$LANDIS_CONSOLE scenario.txt"

## Windows (PowerShell)
docker run --rm `
  --cpus=4 `
  --memory=64g `
  --mount type=bind,src="C:\path\to\your\scenario",dst=/scenarioFolder `
  ghcr.io/landis-ii-foundation/landis-ii-v8-release:main `
  /bin/sh -c "cd /scenarioFolder && dotnet `$LANDIS_CONSOLE scenario.txt"
```

## Included extensions

See [`extensions-v8-release.yaml`](../extensions-v8-release.yaml) and [`libraries-v8-release.yaml`](../libraries-v8-release.yaml) for the exact commit SHAs used.

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
| Base BDA |
| Base Fire |
| Base Wind |
| Biomass Harvest |
| Biomass Hurricane |
| Dynamic Biomass Fuels |
| Dynamic Fire System |
| Land Use Plus |
| LinearWind |
| Social Climate Fire |
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
| Output Max Species Age |
| Output Wildlife Habitat |
| Local Habitat Suitability Output |

## Enhancements over `landis-ii-v8-linux`

This image supersedes `Clean_Docker_LANDIS-II_8_AllExtensions` with the following improvements:

- Ubuntu 24.04 (noble) base image instead of 22.04 (jammy);
- `dotnet` installed from the `apt` repositories;
- LANDIS-II placed at `/opt/landis-ii` (standard location for third-party software);
- extension and library versions defined in shared `*.yaml` files, not hardcoded in the Dockerfile;
- shared `.csproj` files for Forest Roads and Magic Harvest extensions (`extension_files/`);
- build scripts rewritten in `bash`, shared in `scripts/`, reusable across image flavours;
- `yq` used to parse yaml; `xmlstarlet` used to edit `.csproj` XML;
- shared tests (`tests/`) run as part of the build;

## Build the image

Build from the repository root so that shared files (`extension_files/`, `scripts/`, `*.yaml`) are available.

### Linux / macOS (bash)

```shell
cd ~/Tool-Docker-Apptainer

docker build . \
  -f Docker-LANDIS-II-v8-release/Dockerfile \
  -t landis-ii-v8-release:release
```

### Windows (PowerShell)

```shell
cd ~/Tool-Docker-Apptainer

docker build . `
  -f Docker-LANDIS-II-v8-release/Dockerfile `
  -t landis-ii-v8-release:release
```

## Run a locally built container

Replace `landis-ii-v8-release:release` with `ghcr.io/landis-ii-foundation/landis-ii-v8-release:main` if you pulled the pre-built image instead.

### Interactive container

#### Linux / macOS (bash)

```shell
docker run -it \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="/path/to/your/scenario",dst=/scenarioFolder \
  --name landis01 \
  landis-ii-v8-release:release
```

#### Windows (PowerShell)

```shell
docker run -it `
  --cpus=4 `
  --memory=64g `
  --mount type=bind,src="C:\path\to\your\scenario",dst=/scenarioFolder `
  --name landis01 `
  landis-ii-v8-release:release
```

### Non-interactive container (run a single simulation)

#### Linux / macOS (bash)

```shell
docker run --rm \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="/path/to/your/scenario",dst=/scenarioFolder \
  --name landis01 \
  landis-ii-v8-release:release \
  /bin/sh -c "cd /scenarioFolder && dotnet \$LANDIS_CONSOLE scenario.txt"
```

#### Windows (PowerShell)

```shell
docker run --rm `
  --cpus=4 `
  --memory=64g `
  --mount type=bind,src="C:\path\to\your\scenario",dst=/scenarioFolder `
  --name landis01 `
  landis-ii-v8-release:release `
  /bin/sh -c "cd /scenarioFolder && dotnet `$LANDIS_CONSOLE scenario.txt"
```
