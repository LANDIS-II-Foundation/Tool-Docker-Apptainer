# Clean_Docker_LANDIS-II_7_AllExtensions

> [!WARNING]
> **This image is deprecated.** Use [`landis-ii-v7-release`](../Docker-LANDIS-II-v7-release/) instead.
> It provides the same extensions with improved build infrastructure and a pre-built image you can pull without building locally.

This folder contains the Dockerfile necessary to create the Docker image that will contain LANDIS-II v7 and all of its available extensions.

All extensions are in their most recent version compatible with v7, before the switch to v8; except for Biomass Harvest, whose latest version before v7 had a compatibility issue (see comments in the Dockerfile).

⚠ WARNING : You might encounter some bugs during the build process, which are due to the fact that downloads from github often fail for an unknown reason. Just re-launch the build process if this happens, and it will eventually succeed.

The other files are here to help the build process of the Dockerfile, especially to prepare the files of the extensions before compiling them. Here is a quick summary :

- `buildDockerImage.sh`: shell script to launch the docker command to build the dockerfile with the name `landis-ii_v7_linux` given to the resulting docker image. Launch it in a terminal to quickly build the image.
- `downloadSpecificGitCommitAndFolder.sh`: a script used by the Dockerfile to retrieve files from the different Github repositories containing the LANDIS-II code and the code of its extensions. It's made to download as few files as possible instead of clonign the entire repository every time.
- `editing_csproj_LANDIS-II_files.py`: A python script use to edit the .csproj files used to compile LANDIS-II and its extensions. These edits are made to allow the compilation in a linux environment. See the informations in the readme of https://github.com/LANDIS-II-Foundation/Core-Model-v7-LINUX to know more.
- `Magic Harvest.csproj` and `Forest-Roads-Extension.csproj`: these are csproj files for the two LANDIS-II extensions made by Clement Hardy. Since they have a format very different from the rest, it's easier to just use these files instead of editing the csproj files.
- `BFOLDS_v2.3_nocode`: A folder containing the pre-compiled .dll files for the BFOLDS fire extension. At the date of release of this Dockerfile, the code of BFOLDS is still not open-source, although it will come in the future; in the meantime, it is integrated to this docker image thanks to these precompiled libraries.

