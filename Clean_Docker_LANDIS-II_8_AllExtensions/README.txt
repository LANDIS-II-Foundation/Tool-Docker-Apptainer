This folder contains the Dockerfile necessary to create the Docker image that will contain LANDIS-II v8 and all of its available extensions in their latest version, at the date of January 2025.

Some extensions are still yet not available for LANDIS-II v8 (e.g. PnET), and will be updated when possible.

⚠ WARNING : You might encounter some bugs during the build process, which are due to the fact that downloads from github often fail for an unknown reason. Just re-launch the build process if this happens, and it will eventually succeed.

The other files are here to help the build process of the Dockerfile, especially to prepare the files of the extensions before compiling them. Here is a quick summary :

- buildDockerImage.sh : shell script to launch the docker command to build the dockerfile with the name "landis-ii_v7_linux" given to the resulting docker image. Launch it in a terminal to quickly build the image.
- downloadSpecificGitCommitAndFolder.sh : a script used by the Dockerfile to retrieve files from the different Github repositories containing the LANDIS-II code and the code of its extensions. It's made to download as few files as possible instead of clonign the entire repository every time.
- editing_csproj_LANDIS-II_files.py : A python script use to edit the .csproj files used to compile LANDIS-II and its extensions. These edits are made to allow the compilation in a linux environment. See the informations in the readme of https://github.com/LANDIS-II-Foundation/Core-Model-v7-LINUX to know more.
- "Magic Harvest.csproj" and "Forest-Roads-Extension.csproj" : these are csproj files for the two LANDIS-II extensions made by Clement Hardy. Since they have a format very different from the rest, it's easier to just use these files instead of editing the csproj files.