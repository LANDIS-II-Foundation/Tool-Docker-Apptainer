# LANDIS-II-v8-R


This image closely follows the `Docker-LANDIS-II-release` image but uses `rocker/r-ver:4.6.0` as the base image,
and adds geospatial libraries.
=======
LANDIS-II v8 with R 4.6.0, built on [`rocker/r-ver:4.6.0`](https://rocker-project.org/images/versioned/r-ver.html). Includes LANDIS-II, geospatial libraries, and a full R environment — but no RStudio Server. For an interactive RStudio workflow, use [`landis-ii-v8-rstudio`](../Docker-LANDIS-II-v8-Rstudio/) instead.

**For users:** pull the pre-built image (no build step required).
**For developers:** build the image locally using the instructions below.

## Quick start: use the pre-built image

```shell
docker pull ghcr.io/landis-ii-foundation/landis-ii-v8-r:ubuntu-latest
```

> 💡 **Tags:** `:ubuntu-latest`, `:latest`, and `:main` all point to the same image (Ubuntu 24.04 via `rocker/r-ver:4.6.0`).
> `:main` is retained for backwards compatibility.

Run an interactive R session with your project files available inside the container:

```shell
## Linux / macOS
docker run -it --rm \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="/path/to/your/project",dst=/home/project \
  ghcr.io/landis-ii-foundation/landis-ii-v8-r:ubuntu-latest \
  R

## Windows (PowerShell)
docker run -it --rm `
  --cpus=4 `
  --memory=64g `
  --mount type=bind,src="C:\path\to\your\project",dst=/home/project `
  ghcr.io/landis-ii-foundation/landis-ii-v8-r:ubuntu-latest `
  R
```

**See also:** <https://rocker-project.org/images/versioned/r-ver.html#how-to-use>


## Build the image

Build from the repository root so that shared files are available.

### Linux / macOS (bash)

```shell
cd ~/Tool-Docker-Apptainer

docker build . \
  -f Docker-LANDIS-II-v8-R/Dockerfile \
  -t landis-ii-v8-r:release
```

### Windows (PowerShell)

```shell
cd ~/Tool-Docker-Apptainer

docker build . `
  -f Docker-LANDIS-II-v8-R/Dockerfile `
  -t landis-ii-v8-r:release
```
