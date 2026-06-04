FROM ubuntu:22.04

LABEL org.opencontainers.image.authors="clem.hardy@pm.me; achubaty@for-cast.ca;"

################################################################
## PREREQUISITES
################################################################

ENV C_INCLUDE_PATH=/usr/include/gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV DEBIAN_FRONTEND=noninteractive
ENV DOTNET_ROOT="/opt/.dotnet"
ENV DOTNET_CLI_TELEMETRY_OPTOUT=true
ENV LC_ALL=C.UTF-8

## update and install additional system dependencies:
## - `mono-utils` provides `monodis` used to debug ext/lib builds;
## - python needed for Magic Harvest;
RUN apt-get update && apt-get upgrade -y \
  && apt-get install -y \
    gdal-bin \
    git \
    libgdal-dev \
    libjpeg62 \
    libpng16-16 \
    mono-utils \
    nano \
    pip \
    python3 \
    python-is-python3 \
    software-properties-common \
    vim \
    wget \
    xmlstarlet \
  ## Installing libssl1 needed for dotnet
  && wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb \
  && dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/* ## clean up to save space

WORKDIR $DOTNET_ROOT

## install dotnet SDK and runtime 2.2
RUN wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh \
  && chmod +x ./dotnet-install.sh \
  && ./dotnet-install.sh --channel 2.2 -InstallDir $DOTNET_ROOT/  \
  && ./dotnet-install.sh --channel 2.2 --runtime aspnetcore -InstallDir $DOTNET_ROOT/ \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH=$PATH:$DOTNET_ROOT:$DOTNET_ROOT/tools

WORKDIR /

## install yq (used to parse yaml files) from source
RUN wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/local/bin/yq \
  && chmod +x /usr/local/bin/yq

## configure git (be sure to unset anything changed here at the end):
## - `advice.detachedHead false` suppresses 'detached HEAD' messages during checkout;
## - `http.*` settings help with slow/high-latency network connections;
RUN  git config --global advice.detachedHead false \
  && git config --global http.lowSpeedLimit 0 \
  && git config --global http.lowSpeedTime 999999 \
  && git config --global http.postBuffer 524288000 \
  && git config --global http.version HTTP/1.1

## set variables to aid in readability and reuse:
## - ARG variable are set during build only;
## - ENV variables are set in the image and can be used e.g., to run LANDIS;
##
ARG LANDIS_GITHUB="https://github.com/LANDIS-II-Foundation"

ARG LANDIS_DIR="/opt/landis-ii" ## use /opt for non-OS-bundled software
ARG LANDIS_CORE_DIR="$LANDIS_DIR/Core-Model-v7-LINUX"
ARG LANDIS_EXT_DIR="$LANDIS_CORE_DIR/build/extensions"
ARG LANDIS_REL_DIR="$LANDIS_CORE_DIR/build/Release"

ARG EXT_LOG_FILE="$LANDIS_DIR/build_exts.log"
ARG LIB_LOG_FILE="$LANDIS_DIR/build_libs.log"
ARG TESTS_DIR="$LANDIS_DIR/tests"

ENV LANDIS_CONSOLE="$LANDIS_REL_DIR/Landis.Console.dll"
ENV LANDIS_EXT_TOOL="$LANDIS_REL_DIR/Landis.Extensions.dll"

WORKDIR $LANDIS_DIR

COPY scripts $LANDIS_DIR/scripts
RUN sed -i 's/\r$//' $LANDIS_DIR/scripts/*.sh \
    && chmod a+x $LANDIS_DIR/scripts/*.sh

################################################################
## COMPILING LANDIS-II AND EXTENSIONS
################################################################

WORKDIR $LANDIS_DIR

## get and build the core model
RUN git clone $LANDIS_GITHUB/Core-Model-v7-LINUX.git \
  && dotnet build $LANDIS_CORE_DIR/Tool-Console/src -c Release

## get support libraries
RUN git clone $LANDIS_GITHUB/Support-Library-Dlls-v7.git \
  && mv $LANDIS_DIR/Support-Library-Dlls-v7/* $LANDIS_EXT_DIR/ \
  && rm -r $LANDIS_DIR/Support-Library-Dlls-v7

## recompile some support libraries to resolve library errors
##
##  - necessary files are downloaded and built using `scripts/install_libraries_v7.sh`;
##  - the script parses `libraries-v7-release.yaml` to checkout specific commits;
##  - it cleans up afterwards, removing the library source files to save space in the image;

COPY libraries-v7-release.yaml $LANDIS_DIR/libraries-v7-release.yaml

RUN scripts/install_libraries_v7.sh libraries-v7-release.yaml $LANDIS_DIR

## DEBUG: library install and dependencies
# RUN echo "$(cat $LIB_LOG_FILE)" 1>&2 && exit 1

## get, build, and register all available extensions
##
##  - necessary files are downloaded and built using `scripts/install_extensions_v7.sh`;
##  - the script parses `extensions-v7-release.yaml` to checkout specific commits;
##  - it uses sparse checkout of specific directories to avoid downloading the entire repo;
##  - it cleans up afterwards, removing the extension source files to save space in the image;

COPY extension_files_v7 $LANDIS_DIR/extension_files
COPY extensions-v7-release.yaml $LANDIS_DIR/extensions-v7-release.yaml

RUN scripts/install_extensions_v7.sh extensions-v7-release.yaml $LANDIS_DIR

## DEBUG: extension install and dependencies
# RUN echo "$(cat $EXT_LOG_FILE)" 1>&2 && exit 1

## recompile console tool to reference extension libraries
##
##  - per <https://github.com/CU-ESIIL/ExtremeWildfire/blob/main/docker/landis2/Dockerfile>;
##  - this part seems absolutly essential: the core of LANDIS-II v7 needs to have all libraries
##    of all extensions clearly indicated as dependancies so that it can find them when running;
##  - all of the .dlls were copied from /build/extensions to /build/Release but need to be
##    referenced in the console tool, so it needs to be rebuilt.

## TODO: remove if not needed
# WORKDIR $LANDIS_DIR
# RUN scripts/add_console_csproj_dlls.sh $LANDIS_DIR \
#   && dotnet build $LANDIS_CORE_DIR/Tool-Console/src -c Release

## DEBUG: rebuild of Tool-Console
# RUN monodis --assembly "$LANDIS_EXT_DIR/Landis.Library.UniversalCohorts-v1.dll" 1>&2 && exit 1

################################################################
## Testing
################################################################

## TODO !!
# COPY ./tests $TESTS_DIR
#
# WORKDIR $TESTS_DIR/TestPnET_AllExtension
#
# RUN dotnet $LANDIS_CONSOLE scenario.txt

################################################################
## Cleanup
################################################################

WORKDIR /

## - remove extension and library build log files;
## - remove tests and their outputs from the image;
## - restore git config changes made previously;
RUN rm $EXT_LOG_FILE $LIB_LOG_FILE \
  # && rm -rf $TESTS_DIR \
  && git config --global --unset advice.detachedHead \
  && git config --global --unset http.lowSpeedLimit \
  && git config --global --unset http.lowSpeedTime \
  && git config --global --unset http.postBuffer \
  && git config --global --unset http.version

## TODO: refactor this to use multistage build to get smaller image

