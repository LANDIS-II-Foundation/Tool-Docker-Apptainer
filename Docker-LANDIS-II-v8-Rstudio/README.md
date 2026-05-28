# LANDIS-II-v8-Rstudio


This image closely follows the `Docker-LANDIS-II-release` image but uses `rocker/geospatial:4.6.0` as the base image,
so it provides an Rstudio Server instance for interactive workflows.
=======
LANDIS-II v8 with R 4.6.0 and RStudio Server, built on [`rocker/geospatial:4.6.0`](https://rocker-project.org/images/versioned/rstudio.html). Intended for interactive workflows: connect to the running container from your browser to use RStudio alongside LANDIS-II.


**For users:** pull the pre-built image (no build step required).
**For developers:** build the image locally using the instructions below.

## Quick start: use the pre-built image

```shell
docker pull ghcr.io/landis-ii-foundation/landis-ii-v8-rstudio:ubuntu-latest
```

> 💡 **Tags:** `:ubuntu-latest`, `:latest`, and `:main` all point to the same image (Ubuntu 24.04 via `rocker/geospatial:4.6.0`).
> `:main` is retained for backwards compatibility.

## Run a container

When launching an instance of the container:

- specify the local port with `-p` (e.g., `-p 127.0.0.1:8080:8787` maps local port 8080 to RStudio's port 8787 inside the container);
- set a `PASSWORD` for the `rstudio` user (if omitted, a random one is printed once at launch);
- mount local directories with `--mount` to make your project files accessible;
- set `USERID` and `GROUPID` to match your host user/group IDs so that file permissions on mounted volumes work correctly (defaults: `1000`);
- limit resources with `--memory` and `--cpus`;

### Linux / macOS (bash)

```shell
docker run -d -it \
  -e USERID=$(id -u) \
  -e GROUPID=$(id -g) \
  -e PASSWORD='<MySecretPassword>' \
  --cpus=4 \
  --memory=64g \
  -p 127.0.0.1:8080:8787 \
  --mount type=bind,source="/path/to/your/project",target=/home/rstudio/project \
  --name landis01 \
  ghcr.io/landis-ii-foundation/landis-ii-v8-rstudio:ubuntu-latest
```

### Windows (PowerShell)

```shell
docker run -d -it `
  -e PASSWORD='<MySecretPassword>' `
  --cpus=4 `
  --memory=64g `
  -p 127.0.0.1:8080:8787 `
  --mount type=bind,source="C:\path\to\your\project",target=/home/rstudio/project `
  --name landis01 `
  ghcr.io/landis-ii-foundation/landis-ii-v8-rstudio:ubuntu-latest
```

> **Note for Windows users:** `$(id -u)` and `$(id -g)` are Linux/macOS shell substitutions and are not available in PowerShell. Omitting `USERID`/`GROUPID` uses the defaults (1000); if you encounter permission issues on mounted files, set them explicitly (e.g., `-e USERID=1000`).

### Access the RStudio instance

Open your browser and navigate to `http://localhost:8080`.
Log in with username `rstudio` and the password you set above.

**See also:** <https://rocker-project.org/images/versioned/rstudio.html#how-to-use>

## Build the image

Build from the repository root so that shared files are available.

### Linux / macOS (bash)

```shell
cd ~/Tool-Docker-Apptainer

docker build . \
  -f Docker-LANDIS-II-v8-Rstudio/Dockerfile \
  -t landis-ii-v8-rstudio:release
```

### Windows (PowerShell)

```shell
cd ~/Tool-Docker-Apptainer

docker build . `
  -f Docker-LANDIS-II-v8-Rstudio/Dockerfile `
  -t landis-ii-v8-rstudio:release
```
