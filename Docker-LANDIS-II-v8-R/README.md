# LANDIS-II-v8-R

This image closely follows the `Docker-LANDIS-II-release` image but uses `rocker/r-ver:4.5.1` as the base image,
and adds geospatial libraries.

## Build the image

### Linux (bash)

```shell
cd ~/Tool-Docker-Apptainer

docker build . \
  -f Docker-LANDIS-II-v8-R/Dockerfile \
  -t landis-ii-8-r:release
```

## Run a container

### Linux (bash)

```shell
## example
docker run -d -it landis-ii-8-r:release
```

**See also:** <https://rocker-project.org/images/versioned/r-ver.html#how-to-use>
