# LANDIS-II-v8-Rstudio

This image closely follows the `Docker-LANDIS-II-release` image but uses `rocker/geospatial:4.5.1` as the base image,
so it provides an Rstudio Server instance for interactive workflows.

## Build the image

### Linux (bash)

```shell
cd ~/Tool-Docker-Apptainer

docker build . \
  -f Docker-LANDIS-II-v8-Rstudio/Dockerfile \
  -t landis-ii-8-rstudio:release
```

## Run a container

- specify the local port to use to connect to the container by passing `-p` with appropriate arguments
  (e.g., `-p 127.0.0.1:8080:8787` allows connections on local port 8080; 8787 is the port used by Rstudio on the container);
- a custom `PASSWORD` can be specified (if not specified, a random one will be used and displayed *once* at container launch);
- local directories can be mounted as above;
- `USERID` and `GROUPID` specify the user and group ids, respectively, and can be specified
  to ensure user file permissions of the container match those of the mounted volume (defaults: `1000`)
  (see <https://rocker-project.org/images/versioned/rstudio.html#userid-and-groupid>);
- limit system resources available to the container by passing e.g., `--memory=64g` and `--cpus=8`;

### Linux (bash)

```shell
## example
docker run -d -it \
  -e USERID=$(id -u) \
  -e GROUPID=$(id -g) \
  -e PASSWORD='<MySecretPassword>' \
  --cpus=4 \
  --memory=64g \
  -p 127.0.0.1:8080:8787 \
  --mount type=bind,source=/home/$(id -un)/projects/LANDIS-II,target=/home/rstudio/LANDIS-II \
  --name landis01 \
  landis-ii-8-rstudio:release
```

### Access the Rstudio instance

Open your web browser and connect to `localhost:8080`.
Log in using username `rstudio` and the password set above.

**See also:** <https://rocker-project.org/images/versioned/rstudio.html#how-to-use>
