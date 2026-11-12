ARG UBUNTU_VERSION=24.04

################################################################
## STAGE 1: BUILD
##
## Full .NET SDK + GDAL headers + build/debug tooling. This stage clones and
## compiles the core model, support libraries, and all extensions, then runs
## the test scenarios as a build gate. Nothing from this stage ships in the
## final image except the compiled `build/` tree (see STAGE 2), so the SDK
## (~480 MB), the NuGet cache (~560 MB), cloned source, and the GDAL dev/data
## packages never reach the runtime image.
################################################################
FROM ubuntu:${UBUNTU_VERSION} AS build
ARG UBUNTU_VERSION    ## must re-declare after FROM to stay in scope

ENV C_INCLUDE_PATH=/usr/include/gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8

## update and install build-time system dependencies:
## - `dotnet-sdk-8.0` compiles the core model and extensions;
## - `gdal-bin`/`libgdal-dev` provide GDAL headers some extensions compile against;
## - `mono-utils` provides `monodis` used to debug ext/lib builds;
## - python needed to run the Magic Harvest test scenario in this stage;
## - `xmlstarlet` used to edit xml in .csproj files;
RUN apt-get update && apt-get upgrade -y \
  && apt-get install -y software-properties-common \
  && if [ "${UBUNTU_VERSION}" = "26.04" ]; then \
       add-apt-repository ppa:dotnet/backports && apt-get update; \
     fi \
  && apt-get install -y \
    dotnet-sdk-8.0 \
    gdal-bin \
    git \
    libgdal-dev \
    libjpeg62 \
    libpng16-16t64 \
    mono-utils \
    python3 \
    python3-pip \
    python-is-python3 \
    wget \
    xmlstarlet \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/* ## clean up to save space

## Ubuntu 26.04 changed SO names for three libraries that Gdal.Core NuGet's bundled libgdal.so.20
## was compiled against: libxml2 (.so.2 → .so.16), libicuuc/libicudata (.so.74 → .so.78).
## Needed here so the test scenarios in this stage can load the bundled GDAL (and again in STAGE 2).
RUN if [ "${UBUNTU_VERSION}" = "26.04" ]; then \
      ln -s /usr/lib/x86_64-linux-gnu/libxml2.so.16 /usr/lib/x86_64-linux-gnu/libxml2.so.2 \
      && ln -s /usr/lib/x86_64-linux-gnu/libicuuc.so.78 /usr/lib/x86_64-linux-gnu/libicuuc.so.74 \
      && ln -s /usr/lib/x86_64-linux-gnu/libicudata.so.78 /usr/lib/x86_64-linux-gnu/libicudata.so.74 \
      && ldconfig; \
    fi

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
ARG LANDIS_CORE_DIR="$LANDIS_DIR/Core-Model-v8-LINUX"
ARG LANDIS_EXT_DIR="$LANDIS_CORE_DIR/build/extensions"
ARG LANDIS_REL_DIR="$LANDIS_CORE_DIR/build/Release"

ARG EXT_LOG_FILE="$LANDIS_DIR/build_exts.log"
ARG LIB_LOG_FILE="$LANDIS_DIR/build_libs.log"
ARG TESTS_DIR="$LANDIS_DIR/tests"

ENV LANDIS_CONSOLE="$LANDIS_REL_DIR/Landis.Console.dll"
ENV LANDIS_EXT_TOOL="$LANDIS_REL_DIR/Landis.Extensions.dll"
ENV LANDIS_FPS="$LANDIS_REL_DIR/Landis.Extension.FPS-v1.dll"

WORKDIR $LANDIS_DIR

COPY scripts $LANDIS_DIR/scripts
RUN sed -i 's/\r$//' $LANDIS_DIR/scripts/*.sh \
    && chmod a+x $LANDIS_DIR/scripts/*.sh

################################################################
## COMPILING LANDIS-II AND EXTENSIONS
################################################################

WORKDIR $LANDIS_DIR

## get and build the core model (use specific commit in case of broken updates)
RUN git clone $LANDIS_GITHUB/Core-Model-v8-LINUX.git \
  # && git -C $LANDIS_CORE_DIR checkout 7b0f215705900423068b85cec5eb197de4a7b419 \
  && git -C $LANDIS_CORE_DIR checkout 8725da5cd7bfdf3ae28bbd59b1353ec442783d68 \
  && dotnet build $LANDIS_CORE_DIR/Tool-Console/src -c Release

## get the prebuilt support libraries
##
##  - the commit is pinned in `support-libraries-v8-UCL2-release.yaml`, so it is
##    reviewable alongside the extension and library pins rather than buried here;
##  - these are copied into `build/extensions` BEFORE the extensions are compiled,
##    because extensions reference them through HintPaths into that directory;
##  - they are NOT part of `libraries-v8-release.yaml`: those entries are built from
##    source with `dotnet build`, and applied after the extensions are built.

COPY support-libraries-v8-UCL2-release.yaml $LANDIS_DIR/support-libraries-v8-UCL2-release.yaml

RUN scripts/install_support_libraries_v8.sh support-libraries-v8-UCL2-release.yaml $LANDIS_DIR

## build the libraries the extensions must compile against
##
##  - each replaces its Support-Library-Dlls-v8 copy in `build/extensions`, so it has to
##    run after the step above and before the extensions are built;
##  - currently `Landis.Library.PnETCohorts-v2` 2.4.2, which PnET-Succession 6.1.3 needs;
##    see `libraries-v8-UCL2-release-prebuild.yaml`.

COPY libraries-v8-UCL2-release-prebuild.yaml $LANDIS_DIR/libraries-v8-UCL2-release-prebuild.yaml

RUN scripts/install_libraries_v8.sh libraries-v8-UCL2-release-prebuild.yaml $LANDIS_DIR

## get, build, and register all available extensions
##
##  - necessary files are downloaded and built using `scripts/install_extensions_v8.sh`;
##  - the script parses `extensions-v8-UCL2-release.yaml` to checkout specific commits;
##  - it uses sparse checkout of specific directories to avoid downloading the entire repo;
##  - it cleans up afterwards, removing the extension source files to save space in the image;
##  - `EXT_DROP_SHADOWING_DLLS=true` makes it delete an extension's committed copy of any
##    DLL already in `build/extensions` before building it. Otherwise Magic Harvest's
##    committed `Landis.Extension.BiomassHarvest-v7.dll` replaces the Biomass Harvest
##    build. Output Biomass PnET's committed `Landis.Library.UniversalCohorts-v2.dll`
##    now matches the Support-Library-Dlls-v8 copy, but would replace a newer one (earlier
##    pins of it, Social Climate Fire and Forest Roads committed the faulty 1.3.0.0);
##  - entries marked `type: tool` are skipped here and built after the console
##    rebuild (see below);

COPY extension_files $LANDIS_DIR/extension_files
COPY extensions-v8-UCL2-release.yaml $LANDIS_DIR/extensions-v8-UCL2-release.yaml

ENV EXT_DROP_SHADOWING_DLLS=true

RUN scripts/install_extensions_v8.sh extensions-v8-UCL2-release.yaml $LANDIS_DIR

## DEBUG: extension install and dependencies
# RUN echo "$(cat $EXT_LOG_FILE)" 1>&2 && exit 1

## recompile some support libraries to resolve library errors
##
##  - necessary files are downloaded and built using `scripts/install_libraries_v8.sh`;
##  - the script parses `libraries-v8-release.yaml` to checkout specific commits;
##  - it cleans up afterwards, removing the library source files to save space in the image;

COPY libraries-v8-release.yaml $LANDIS_DIR/libraries-v8-release.yaml

RUN scripts/install_libraries_v8.sh libraries-v8-release.yaml $LANDIS_DIR

## DEBUG: library install and dependencies
# RUN echo "$(cat $LIB_LOG_FILE)" 1>&2 && exit 1

## recompile console tool to reference extension libraries
##
##  - per <https://github.com/CU-ESIIL/ExtremeWildfire/blob/main/docker/landis2/Dockerfile>;
##  - this part seems absolutly essential: the core of LANDIS-II v8 needs to have all libraries
##    of all extensions clearly indicated as dependancies so that it can find them when running;
##  - all of the .dlls were copied from /build/extensions to /build/Release but need to be
##    referenced in the console tool, so it needs to be rebuilt.

WORKDIR $LANDIS_DIR
RUN scripts/add_console_csproj_dlls.sh $LANDIS_DIR \
  && dotnet build $LANDIS_CORE_DIR/Tool-Console/src -c Release

## build the tools listed in `extensions-v8-UCL2-release.yaml` (`type: tool`)
##
##  - the one tool is the Forest Product Sector Module (FPSM), a stand-alone
##    post-processor of ForC Succession's flux logs, run as
##    `dotnet $LANDIS_FPS <input file>`;
##  - tools are installed in build/Release only, so they are neither registered
##    nor referenced by the console;
##  - built after the console rebuild, which replaces `MathNet.Numerics.dll` in
##    build/Release (4.0.0.0 from the support libraries) with its own 5.0.0.0, so
##    that FPSM's shipped examples, run as a build gate, use the DLLs the image
##    ships;
##  - `EXT_DROP_SHADOWING_DLLS` (set above) applies to this pass too.

RUN scripts/install_extensions_v8.sh extensions-v8-UCL2-release.yaml $LANDIS_DIR tool

## DEBUG: rebuild of Tool-Console (Universal Cohorts 2.2.0.0 expected???)
# RUN monodis --assembly "$LANDIS_EXT_DIR/Landis.Library.UniversalCohorts-v1.dll" 1>&2 && exit 1

################################################################
## Testing (build gate; runs in this stage with the full toolchain)
##
## NOTE: these run with GDAL dev/data present, so they verify the *build*.
## The slim runtime image (STAGE 2) is smoke-tested separately after build
## (see this flavour's README) to verify the trimmed runtime dependencies.
################################################################

COPY ./tests $TESTS_DIR

## The `scenario_UCLv2.txt` files live beside the `scenario.txt` the v8 image uses and
## share the same inputs; they only comment out the extensions this image doesn't ship
## (see each test's README).
WORKDIR $TESTS_DIR/TestNECN_AllExtension

RUN dotnet $LANDIS_CONSOLE scenario_UCLv2.txt

## PnET Succession + Output Biomass PnET, alongside the disturbance/output extensions
## this image ships. This also exercises `Landis.Library.PnETCohorts-v2` built in the
## prebuild pass above.
WORKDIR $TESTS_DIR/TestPnET_AllExtension

RUN dotnet $LANDIS_CONSOLE scenario_UCLv2.txt

## PnET cohort-removal regression check: Biomass Harvest clear-cuts every stand (all 259 active
## cells) at year 10, so at year 20 no cohort may be older than 20 years. With PnETCohorts-v2
## 2.3.0.0 and PnET-Succession before 6.1.2, harvest removed cohorts from a copy that PnET
## rebuilt from its own cohorts every timestep, so the initial cohorts came back (aged 30-100).
## The first check makes sure the clear-cut happened, so the second one tests something.
RUN rm -f community-input-file-*.csv \
 && dotnet $LANDIS_CONSOLE scenario_UCLv2_harvest-check.txt

RUN [ -s community-input-file-20.csv ] || { echo "FAIL: no year-20 community output"; exit 1; }; \
    N=$(awk -F, '{sub(/\r$/, "")} NR==1{for (i = 1; i <= NF; i++) {if ($i == "Time") t = i; if ($i == "TotalCohortsCompleteHarvest") c = i}; next} $t == 10 {n += $c} END {print n + 0}' \
      output/harvestCheck/biomass-harvest-summary-log.csv); \
    A20=$(awk -F, 'NR>1{print $3}' community-input-file-20.csv | sort -n | tail -1); \
    echo "PnET harvest check: cohorts clear-cut at yr10=$N; oldest cohort at yr20=${A20:-none}"; \
    [ "$N" -gt 0 ] || { echo "FAIL: the year-10 clear-cut removed no cohorts, so this check tests nothing"; exit 1; }; \
    [ "${A20:-0}" -le 20 ] || { echo "FAIL: cohorts older than the year-10 clear-cut are still in PnET (harvest acted on a copy)"; exit 1; }

WORKDIR $TESTS_DIR/TestForCS_v8

RUN dotnet $LANDIS_CONSOLE scenario.txt

## Biomass Succession (inputs vintage-matched to the pinned UCLv2 commit; see the test README).
## The second RUN is a cohort-aging regression check: Output Biomass Community writes per-cell
## cohort ages, and the maximum must advance by ~the succession timestep each step (~+50 yr over
## this 50-yr run). A stale Biomass Succession that aged cohorts +1 per timestep instead of per
## year (fixed in spin-up overhaul #53) would advance only ~+5 yr and fail here.
WORKDIR $TESTS_DIR/TestBiomassSuccession_UCLv2_v8

RUN dotnet $LANDIS_CONSOLE scenario.txt

RUN A0=$(awk -F, 'NR>1{print $3}' community-input-file-0.csv | sort -n | tail -1); \
    A50=$(awk -F, 'NR>1{print $3}' community-input-file-50.csv | sort -n | tail -1); \
    echo "Biomass Succession cohort-aging check: max age yr0=$A0 yr50=$A50 (delta=$((A50 - A0)))"; \
    [ "$((A50 - A0))" -ge 40 ] || { echo "FAIL: cohorts did not age -- stale Biomass Succession (+1/timestep) bug"; exit 1; }

################################################################
## STAGE 2: RUNTIME
##
## Slim Ubuntu with only what's needed to *run* LANDIS-II: the .NET runtime
## (no SDK), the handful of system libs the bundled GDAL links at runtime, and
## python for Magic Harvest. The compiled `build/` tree is copied from STAGE 1.
## No gdal-bin/gdal-data/PROJ: LANDIS ships its own libgdal.so.20 and writes
## ungeoreferenced rasters, so no GDAL data or projection support is required.
################################################################
FROM ubuntu:${UBUNTU_VERSION} AS runtime
ARG UBUNTU_VERSION    ## must re-declare after FROM to stay in scope

LABEL org.opencontainers.image.authors="clem.hardy@pm.me; achubaty@for-cast.ca;"

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8

## update and install runtime-only system dependencies:
## - `dotnet-runtime-8.0` runs the compiled Landis.Console.dll (the SDK is not needed at runtime);
## - libxml2/libexpat1/libjpeg62/libpng16 are the only system libs the bundled libgdal.so.20
##   links at runtime (confirmed via ldd); LANDIS uses its own bundled GDAL. The libxml2 runtime
##   package is `libxml2` on 24.04 but `libxml2-16` on 26.04 (soname bumped .so.2 -> .so.16);
## - python needed for Magic Harvest.
RUN apt-get update && apt-get upgrade -y \
  && if [ "${UBUNTU_VERSION}" = "26.04" ]; then \
       apt-get install -y software-properties-common \
       && add-apt-repository ppa:dotnet/backports && apt-get update \
       && LIBXML2_PKG=libxml2-16; \
     else \
       LIBXML2_PKG=libxml2; \
     fi \
  && apt-get install -y --no-install-recommends \
    dotnet-runtime-8.0 \
    libexpat1 \
    libjpeg62 \
    libpng16-16t64 \
    python3 \
    python-is-python3 \
    "$LIBXML2_PKG" \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/* ## clean up to save space

## Ubuntu 26.04 SO-name workaround for the bundled libgdal.so.20 (see STAGE 1 for details).
RUN if [ "${UBUNTU_VERSION}" = "26.04" ]; then \
      ln -s /usr/lib/x86_64-linux-gnu/libxml2.so.16 /usr/lib/x86_64-linux-gnu/libxml2.so.2 \
      && ln -s /usr/lib/x86_64-linux-gnu/libicuuc.so.78 /usr/lib/x86_64-linux-gnu/libicuuc.so.74 \
      && ln -s /usr/lib/x86_64-linux-gnu/libicudata.so.78 /usr/lib/x86_64-linux-gnu/libicudata.so.74 \
      && ldconfig; \
    fi

ARG LANDIS_DIR="/opt/landis-ii"
ARG LANDIS_CORE_DIR="$LANDIS_DIR/Core-Model-v8-LINUX"
ARG LANDIS_REL_DIR="$LANDIS_CORE_DIR/build/Release"

ENV LANDIS_CONSOLE="$LANDIS_REL_DIR/Landis.Console.dll"
ENV LANDIS_EXT_TOOL="$LANDIS_REL_DIR/Landis.Extensions.dll"
ENV LANDIS_FPS="$LANDIS_REL_DIR/Landis.Extension.FPS-v1.dll"

## copy ONLY the compiled LANDIS-II tree (core + extensions + registry) from the build stage
COPY --from=build $LANDIS_CORE_DIR/build $LANDIS_CORE_DIR/build

WORKDIR $LANDIS_DIR
