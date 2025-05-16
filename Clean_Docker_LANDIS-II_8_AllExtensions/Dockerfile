FROM ubuntu:22.04

################################################################
# PREPARATIONS
################################################################

# Set the DEBIAN_FRONTEND environment variable to noninteractive
# Avoid prompts when installing packages
ENV DEBIAN_FRONTEND=noninteractive

# PREPARING PACKAGES AND UPGRADING, AND INSTALLING DEPENDENCIES OF LANDIS-II
# apt-get clean and rm -rf /var/lib/apt/lists/* are used to clear the packages folder caches
# to avoid putting them in the docker layerin system, freeing space
RUN apt-get update -y && apt-get upgrade -y \
&& apt-get update && apt-get -y upgrade \
&& apt-get install -y wget vim pip nano git python3 python-is-python3 \
&& apt-get install -y libjpeg62 \
&& apt-get install -y libpng16-16 \
&& apt-get install -y gdal-bin \
&& apt-get install -y libgdal-dev \
# Installing libssl1 sometimes needed for Dotnet
&& wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb \
&& dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb \
&& apt-get clean && rm -rf /var/lib/apt/lists/*
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal

# INSTALLING DOTNET SDK AND RUNTIME 8.0
RUN mkdir /bin/.dotnet/ && cd /bin/.dotnet/ \
&& wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh \
&& chmod +x ./dotnet-install.sh \
&& ./dotnet-install.sh --channel 8.0 -InstallDir /bin/.dotnet/  \
&& ./dotnet-install.sh --channel 8.0 --runtime aspnetcore -InstallDir /bin/.dotnet/ \
&& apt-get clean && rm -rf /var/lib/apt/lists/*
ENV DOTNET_ROOT=/bin/.dotnet
ENV PATH=$PATH:$DOTNET_ROOT:$DOTNET_ROOT/tools

# PREPARING VARIABLES FOR DOWNLOADS
# WARNING : With a bad internet connection, git clone can sometimes fail to.
# These commands should help git on bad internet connections
RUN git config --global http.version HTTP/1.1 \
&& git config --global http.postBuffer 524288000 \
&& git config --global http.lowSpeedLimit 0 \
&& git config --global http.lowSpeedTime 999999

# PREPARING VARIABLE FOR MORE EASY COMMANDS 
ENV LANDIS_EXTENSIONS_TOOL="/bin/LANDIS_Linux/Core-Model-v8-LINUX/build/Release/Landis.Extensions.dll"
ENV LANDIS_CONSOLE="/bin/LANDIS_Linux/Core-Model-v8-LINUX/build/Release/Landis.Console.dll"
ENV LANDIS_FOLDER="/bin/LANDIS_Linux/Core-Model-v8-LINUX/"

################################################################
# COMPILING LANDIS-II
################################################################

###### COMPILING THE CORE 

RUN mkdir /bin/LANDIS_Linux \
&& cd /bin/LANDIS_Linux && git clone https://github.com/LANDIS-II-Foundation/Core-Model-v8-LINUX.git \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Tool-Console/src && dotnet build -c Release 

# Downloading support libraries and installing them
# We fix the commit that is used to avoid breaking the build of the Docker image
# because of updates to the repository
RUN cd /bin/LANDIS_Linux && git clone https://github.com/LANDIS-II-Foundation/Support-Library-Dlls-v8.git \
&& cd /bin/LANDIS_Linux/Support-Library-Dlls-v8/ && git checkout f8178b2a8f8d39bf8c4f1884cc446e4e34fee1ff \
&& mv /bin/LANDIS_Linux/Support-Library-Dlls-v8/* /bin/LANDIS_Linux/Core-Model-v8-LINUX/build/extensions \
&& rm -r /bin/LANDIS_Linux/Support-Library-Dlls-v8

# Transfering the python script that helps the compilation of the extensions
COPY ./files_to_help_compilation/editing_csproj_LANDIS-II_files.py /bin/LANDIS_Linux/Core-Model-v8-LINUX

# Transfering the sh script that allows us to only download one folder from one commit from github
COPY ./files_to_help_compilation/downloadSpecificGitCommitAndFolder.sh /bin/LANDIS_Linux/Core-Model-v8-LINUX
RUN chmod +x /bin/LANDIS_Linux/Core-Model-v8-LINUX/downloadSpecificGitCommitAndFolder.sh

###### COMPILING AND REGISTERING EXTENSIONS 
# INFO: The files necessary for the compilation are downloaded through the script downloadSpecificGitCommitAndFolder.sh
# It is used to avoid downloading the entire repository as it's not needed.
#
# It takes three arguments :
# The URL of the repo
# The commit hash for the commit from which we want to download files
# The folder we want to download files from (excludes all of the others)
#
# The folder we want is almost always /src which contains the source code.
#
# We also always end up deleting the files downloaded for the build to avoid saving them in docker layering system (saves space).
#
# For the .txt file necessary to register the extension in the extension.xml file, I've decided to download them through
# their unique Github URL (corresponding to the commit). This is again to avoid downloading a lot of files for nothing.

#### SUCCESSION EXTENSIONS

# Biomass Succession
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 58ad3673e02abe82f437a6b68c44220c51351091 is latest at time of writing.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Biomass-Succession.git 58ad3673e02abe82f437a6b68c44220c51351091 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Biomass-Succession/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./biomass-succession.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Biomass-Succession/9d13943847328e6fc8968120bc46802c8581541b/deploy/installer/Biomass%20Succession%207.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Biomass Succession 7.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Biomass-Succession 

# NECN Succession
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit dd5838ab2b5c8eef874d48b16e9e52480c5671b6 is latest at time of writing.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-NECN-Succession.git dd5838ab2b5c8eef874d48b16e9e52480c5671b6 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-NECN-Succession/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./NECN-succession.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-NECN-Succession/dd5838ab2b5c8eef874d48b16e9e52480c5671b6/deploy/installer/NECN_Succession8.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "NECN_Succession8.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-NECN-Succession

# PnET Succession
# As of time of writing, seems to work, but is not released officially.
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 8cd34cd223e5cfbf9b63e2582ff863e2c2d37d07 is the most recent at date of writing.
# Testing an update from Austen !
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/aruzicka555/Extension-PnET-Succession.git 8cd34cd223e5cfbf9b63e2582ff863e2c2d37d07 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-PnET-Succession/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./PnET-Succession.csproj \
# We need to remove the .sln file; it's not useful to build, and is full of bad/missing references to other projects.
&& rm /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-PnET-Succession/src/PnET-Succession.sln \
# We make the build
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-PnET-Succession/src \
&& dotnet build -c Release \
# We remove the files
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-PnET-Succession \
# To finish, we have to transfer some "Default files" of PnET in the extension folder
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/aruzicka555/Extension-PnET-Succession.git 8cd34cd223e5cfbf9b63e2582ff863e2c2d37d07 /deploy \ 
&& cp -r /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-PnET-Succession/deploy/Defaults /bin/LANDIS_Linux/Core-Model-v8-LINUX/build/extensions \
# We also have to register the extension properly
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-PnET-Succession && wget https://raw.githubusercontent.com/aruzicka555/Extension-PnET-Succession/8cd34cd223e5cfbf9b63e2582ff863e2c2d37d07/deploy/installer/PnET-Succession.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "PnET-Succession.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-PnET-Succession

# # # Forest Carbon Succession (ForCS)
# As of time of writing, seems to work, but is not released officially and the ForCS extension has not been tested in the Docker container --MGarcia, 20250505
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Austen's commit a00be551c53b1da5cf3b5578b05601cad3d7c8da is the most recent at date of writing.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/aruzicka555/Extension-ForCS-Succession.git a00be551c53b1da5cf3b5578b05601cad3d7c8da /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-ForCS-Succession/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./CForCS.csproj \
# We make the build
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-ForCS-Succession/src \
&& dotnet build -c Release \
# We remove the files
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-ForCS-Succession \
# To finish, we have to transfer some ForCS deployment files in the extension folder
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/aruzicka555/Extension-ForCS-Succession.git a00be551c53b1da5cf3b5578b05601cad3d7c8da /deploy \
# We also have to register the extension properly
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-ForCS-Succession && wget https://raw.githubusercontent.com/aruzicka555/Extension-ForCS-Succession/a00be551c53b1da5cf3b5578b05601cad3d7c8da/deploy/installer/ForCS%204.0.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "ForCS 4.0.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-ForCS-Succession

# # DGS Succession extension : Not yet ready for v8.

# We finish by moving the defaults from /extension to /Release; since apparently, the v8 core wants things to be there.
# See section on recompiling the core at the end of the file.
RUN cp -a /bin/LANDIS_Linux/Core-Model-v8-LINUX/build/extensions/Defaults /bin/LANDIS_Linux/Core-Model-v8-LINUX/build/Release/Defaults


#### DISTURBANCE EXTENSIONS

## FIRE

# Base Fire
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 59a3f9a128cf474ca2971e4b485aed1f2e1025d8 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Base-Fire.git 59a3f9a128cf474ca2971e4b485aed1f2e1025d8 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Base-Fire/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./original-fire.csproj \
# We remove the .sln as it's not useful for the build
&& rm original-fire.sln \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Base-Fire/59a3f9a128cf474ca2971e4b485aed1f2e1025d8/deploy/installer/Original%20Fire%205.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Original Fire 5.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Base-Fire

# # BFOLDS Fire - Not ready yet for v8, to check with Marc Ouelette.

# Climate-social Fire
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 0a9bb3de83a601804e825d41afcbb17fcaedbe76 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Social-Climate-Fire.git 0a9bb3de83a601804e825d41afcbb17fcaedbe76 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Social-Climate-Fire/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./SocialClimateFire.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Social-Climate-Fire/0a9bb3de83a601804e825d41afcbb17fcaedbe76/deploy/installer/Scrapple%204.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Scrapple 4.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Social-Climate-Fire

# # Dynamic Fuel system - Not referenced anymore in the LANDIS-II extension, but is only refered as "Dynamic Fuels & Fire System" with a link to 	http://landis-ii-foundation.github.io/Extension-Dynamic-Fire-System/. Will let this one be. Seems to have been replaced by dynamic biomass fuels ?

# # Dynamic Biomass Fuels
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 06dd67482b20a74a0e075782e66b09b4fe42c248 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Dynamic-Biomass-Fuels.git 06dd67482b20a74a0e075782e66b09b4fe42c248 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Dynamic-Biomass-Fuels/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./dynamic-fuels.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Dynamic-Biomass-Fuels/06dd67482b20a74a0e075782e66b09b4fe42c248/deploy/installer/Dynamic%20Fuels%204.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Dynamic Fuels 4.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Dynamic-Biomass-Fuels

# Dynamic Fire System
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 999b479f503cfd4b4eb9cf0bf1f1a7af21b96eb6 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Dynamic-Fire-System.git 999b479f503cfd4b4eb9cf0bf1f1a7af21b96eb6 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Dynamic-Fire-System/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./dynamic-fire.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Dynamic-Fire-System/999b479f503cfd4b4eb9cf0bf1f1a7af21b96eb6/deploy/installer/Dynamic%20Fire%20Component%204.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Dynamic Fire Component 4.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Dynamic-Fire-System

# ## HARVEST

# Biomass Harvest
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 24b01fea5a90b05b2732c3e52e09a02fdb47db59 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Biomass-Harvest.git 24b01fea5a90b05b2732c3e52e09a02fdb47db59 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Biomass-Harvest/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./biomass-harvest-ext.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Biomass-Harvest/24b01fea5a90b05b2732c3e52e09a02fdb47db59/deploy/installer/Biomass%20Harvest%206.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Biomass Harvest 6.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Biomass-Harvest

# # SOSIEL Harvest - Not ready for v8 as time of writing

# FRS Module
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit b2f1345f33bf0d089dabba75f8a1afe5de2d9d26 is latest as of writing this.
# Not using the download script here as the repo is organized differently (source code is in the root)
&& git clone https://github.com/Klemet/LANDIS-II-Forest-Roads-Simulation-extension.git \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/LANDIS-II-Forest-Roads-Simulation-extension && git checkout b2f1345f33bf0d089dabba75f8a1afe5de2d9d26 \
&& rm /bin/LANDIS_Linux/Core-Model-v8-LINUX/LANDIS-II-Forest-Roads-Simulation-extension/Forest-Roads-Extension.sln
# Sadly, the csproj file here is completly wrong for compiling on Linux. 
# I got to replace it entirely by something that is more in line with the other extensions.
COPY files_to_help_compilation/Forest-Roads-Extension.csproj /bin/LANDIS_Linux/Core-Model-v8-LINUX/LANDIS-II-Forest-Roads-Simulation-extension
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/LANDIS-II-Forest-Roads-Simulation-extension && dotnet build -c Release \
&& wget https://raw.githubusercontent.com/Klemet/LANDIS-II-Forest-Roads-Simulation-extension/b2f1345f33bf0d089dabba75f8a1afe5de2d9d26/Deploy/Installation%20Files/plug-ins-installer-files/Forest%20Roads%20Simulation%202.0.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Forest Roads Simulation 2.0.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r LANDIS-II-Forest-Roads-Simulation-extension

# # Magic harvest
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 4def8fc98e3d816367f8ba2ec6d2b8ea76d279f6 is latest as of writing this.
# Not using the download script here as the repo is organized differently (source code is in the root)
&& git clone https://github.com/Klemet/LANDIS-II-Magic-Harvest.git \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/LANDIS-II-Magic-Harvest/ && git checkout 4def8fc98e3d816367f8ba2ec6d2b8ea76d279f6 \
&& rm /bin/LANDIS_Linux/Core-Model-v8-LINUX/LANDIS-II-Magic-Harvest/"Magic Harvest.sln"
# Sadly, the csproj file here is completly wrong for compiling on Linux. 
# I got to replace it entirely by something that is more in line with the other extensions.
COPY ["./files_to_help_compilation/Magic Harvest.csproj", "/bin/LANDIS_Linux/Core-Model-v8-LINUX/LANDIS-II-Magic-Harvest"]  
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/LANDIS-II-Magic-Harvest && dotnet build -c Release \
&& wget https://raw.githubusercontent.com/Klemet/LANDIS-II-Magic-Harvest/4def8fc98e3d816367f8ba2ec6d2b8ea76d279f6/Deploy/Installation%20Files/plug-ins-installer-files/Magic%20harvest%20v2.1.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Magic harvest v2.1.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r LANDIS-II-Magic-Harvest

## WIND

# Base Wind - Now called Original wind
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 84ab06131a007e78569e778d722a786986f2f8a9 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Base-Wind.git 84ab06131a007e78569e778d722a786986f2f8a9 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Base-Wind/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./original-wind.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Base-Wind/84ab06131a007e78569e778d722a786986f2f8a9/deploy/installer/Original%20Wind%204.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Original Wind 4.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Base-Wind

# Linear Wind
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit fde29473f773c9f995f3a702ca919f7f30a6bcd1 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-LinearWind.git fde29473f773c9f995f3a702ca919f7f30a6bcd1 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-LinearWind/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./linear-wind.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-LinearWind/fde29473f773c9f995f3a702ca919f7f30a6bcd1/deploy/installer/Linear%20Wind%203.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Linear Wind 3.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-LinearWind

# # Hurricane
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit a6afe3f3d2c8664023e32a9ca66544aa14d24449 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Biomass-Hurricane.git a6afe3f3d2c8664023e32a9ca66544aa14d24449 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Biomass-Hurricane/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./hurricane-extension.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Biomass-Hurricane/a6afe3f3d2c8664023e32a9ca66544aa14d24449/deploy/current/Hurricane%203.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Hurricane 3.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Biomass-Hurricane

## DISEASES, INSECTS AND OTHERS

# Base BDA (now named Climate biological Disturbance agent)
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 1aaa2e28627ba21949fd9053b9aae18f099032d5 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Base-BDA.git 1aaa2e28627ba21949fd9053b9aae18f099032d5 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Base-BDA/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./BDA-Climate.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Base-BDA/1aaa2e28627ba21949fd9053b9aae18f099032d5/deploy/installer/Climate%20BDA%205.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Climate BDA 5.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Base-BDA

# Root rot - Not yet available for v8

# # Biomass Browse - Not yet available for v8

# # Land-use plus
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 574940aa6382ed9e5840b78b0544300bf5a40cd2 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Land-Use-Plus.git 574940aa6382ed9e5840b78b0544300bf5a40cd2 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Land-Use-Plus/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./land-use.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Land-Use-Plus/574940aa6382ed9e5840b78b0544300bf5a40cd2/deploy/installer/Land%20Use%204.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Land Use 4.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Land-Use-Plus

### OUTPUT EXTENSIONS

# Max species Age
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 5c9ae5394be1c897ed775cc446d800c34c3d5fec is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Output-Max-Species-Age.git 5c9ae5394be1c897ed775cc446d800c34c3d5fec /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Output-Max-Species-Age/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./max-species-age.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Output-Max-Species-Age/5c9ae5394be1c897ed775cc446d800c34c3d5fec/deploy/installer/Output%20MaxSpeciesAge%204.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Output MaxSpeciesAge 4.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Output-Max-Species-Age

# Biomass-by-age
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 0419cc64634f57ad3660590408ded3aef88ecf9d is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Output-Biomass-By-Age.git 0419cc64634f57ad3660590408ded3aef88ecf9d /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Output-Biomass-By-Age/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./output-biomass-by-age.csproj \
# We need to add a line to the csproj.
&& sed -i '37i    <HintPath>..\\..\\build\\extensions\\Landis.Library.UniversalCohorts-v1.dll</HintPath>' output-biomass-by-age.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Output-Biomass-By-Age/0419cc64634f57ad3660590408ded3aef88ecf9d/deploy/installer/Output%20Biomass-by-Age%204.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Output Biomass-by-Age 4.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Output-Biomass-By-Age

# Biomass Community
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 5942e9bebafb0a618e8f46195aac0b118de4ae31 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Output-Biomass-Community.git 5942e9bebafb0a618e8f46195aac0b118de4ae31 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Output-Biomass-Community/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./output-biomass-community.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Output-Biomass-Community/5942e9bebafb0a618e8f46195aac0b118de4ae31/deploy/installer/Output%20Biomass%20Community%203.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Output Biomass Community 3.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Output-Biomass-Community

# Biomass Output
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit d5cb256f7669df36a76d9337c779cdc7f1cdbd0b is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Output-Biomass.git d5cb256f7669df36a76d9337c779cdc7f1cdbd0b /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Output-Biomass/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./output-biomass.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Output-Biomass/d5cb256f7669df36a76d9337c779cdc7f1cdbd0b/deploy/installer/Output%20Biomass%204.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Output Biomass 4.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Output-Biomass

# Biomass reclassification
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit fad7e9f7e39b9cf72e1e55210cb0e8cd09082671 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Output-Biomass-Reclass.git fad7e9f7e39b9cf72e1e55210cb0e8cd09082671 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Output-Biomass-Reclass/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./output-biomass.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Output-Biomass-Reclass/fad7e9f7e39b9cf72e1e55210cb0e8cd09082671/deploy/installer/Output%20Biomass%20Reclass%204.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Output Biomass Reclass 4.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Output-Biomass-Reclass

# # Cohort statistics outputs
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 0b5cb4ba929bb2f0f87db14fc013e660a79da903 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Output-Cohort-Statistics.git 0b5cb4ba929bb2f0f87db14fc013e660a79da903 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Output-Cohort-Statistics/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./output-cohort-stats.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Output-Cohort-Statistics/0b5cb4ba929bb2f0f87db14fc013e660a79da903/deploy/installer/Output%20Cohort%20Statistics%204.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Output Cohort Statistics 4.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Output-Cohort-Statistics

# # Landscape habitat Output - Not yet available for v8

# Local habitat suitability
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 1366a092625e0a26fff870e16529c1fe3e071c14 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Local-Habitat-Suitability-Output.git 1366a092625e0a26fff870e16529c1fe3e071c14 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Local-Habitat-Suitability-Output/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./local-habitat-output.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Local-Habitat-Suitability-Output/1366a092625e0a26fff870e16529c1fe3e071c14/deploy/installer/Local%20Habitat%20Output.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Local Habitat Output.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Local-Habitat-Suitability-Output

# # PnET Output
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 3924c35120958be9319838ad37e4f67774ac194b is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Output-Biomass-PnET.git 3924c35120958be9319838ad37e4f67774ac194b /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Output-Biomass-PnET/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./output-biomass-pnet.csproj \
# Looks like a wrong variable type definition causes an error. We change it.
&& sed -i 's/ISiteCohorts/SiteCohorts/g' PlugIn.cs \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Output-Biomass-PnET/3924c35120958be9319838ad37e4f67774ac194b/deploy/installer/PnET-Output.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "PnET-Output.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Output-Biomass-PnET

# Wildlife habitat Output
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 695a03ba11a21d8a12eb714a6c8759a8284290f2 is latest as of writing this.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Extension-Output-Wildlife-Habitat.git 695a03ba11a21d8a12eb714a6c8759a8284290f2 /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Extension-Output-Wildlife-Habitat/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./wildlife-habitat.csproj \
&& dotnet build -c Release \
&& wget https://raw.githubusercontent.com/LANDIS-II-Foundation/Extension-Output-Wildlife-Habitat/695a03ba11a21d8a12eb714a6c8759a8284290f2/deploy/installer/Wildlife%20Habitat%20Output%203.txt \
&& dotnet $LANDIS_EXTENSIONS_TOOL add "Wildlife Habitat Output 3.txt" \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Extension-Output-Wildlife-Habitat

# ################################################################
# # RECOMPILING SOME SUPPORT LIBRARIES TO SOLVE LIBRARY ERRORS
#
# Some library errors seem to come from the fact that the
# support libraries in the support library repository are built in
# an environment with references to libraries that are not yet available,
# or other issues. By re-compiling, we avoid these issues.
# ################################################################

# # Metadata library recompilation
# Necessary to avoid an error with ForCS.
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
# Commit 72b8caa14cdd6af81c6e1e4541c4c3e18bc63eca is latest at time of writing.
&& ./downloadSpecificGitCommitAndFolder.sh https://github.com/LANDIS-II-Foundation/Library-Metadata.git 72b8caa14cdd6af81c6e1e4541c4c3e18bc63eca /src \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Library-Metadata/src \
&& python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./Metadata.csproj \
&& dotnet build -c Release \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Library-Metadata

# Universal Initial community library
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX \
&& rm /bin/LANDIS_Linux/Core-Model-v8-LINUX/build/extensions/Landis.Library.InitialCommunity.Universal.dll \
# Commit 5dc6dd299eef88ded1c88871470d58c26c1a4093 is latest at time of writing.
&& mkdir /bin/LANDIS_Linux/Core-Model-v8-LINUX/Library-Initial-Community/ && cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Library-Initial-Community/ \
&& git clone https://github.com/LANDIS-II-Foundation/Library-Initial-Community.git \ 
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Library-Initial-Community/Library-Initial-Community/ && git checkout 5dc6dd299eef88ded1c88871470d58c26c1a4093 \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Library-Initial-Community/Library-Initial-Community/ && python /bin/LANDIS_Linux/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./initial-community.csproj \
&& dotnet build -c Release \
&& cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ && rm -r Library-Initial-Community


# ################################################################
# # RECOMPILING THE CORE TO REFERENCE LIBRARIES
#
# Recompiling the core as per https://github.com/CU-ESIIL/ExtremeWildfire/blob/main/docker/landis2/Dockerfile
# This part seems absolutly essential. Basically, it seems like the core of LANDIS-II v8 needs to have all 
# librairies of all extensions clearly indicated as dependancies so that it can find them when running.
# All of the dll indicated here will be copied from /build/extensions to /build/Release during this re-build process.
# Simply copying the dlls into /build/Release is not enough; you have to indicate them here for the re-build.
#
# WARNING : If you added a new extension in the previous sections, you have to indicate
# its .dll here, or it will not work !
# ################################################################

# To recompile the core properly, we need to add references to all of the libraries that are used
# in the Console.csproj file of Tool-Console. Instead of doing it by hand, I made a python script
# that will detect all of the libraries in /build/extensions, and add them in Console.csproj with the
# right format. Open the script for more info.

COPY ./files_to_help_compilation/adding_xml_dll_references.py /bin/LANDIS_Linux/Core-Model-v8-LINUX/
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/ \
&& python adding_xml_dll_references.py /bin/LANDIS_Linux/Core-Model-v8-LINUX/build/extensions /bin/LANDIS_Linux/Core-Model-v8-LINUX/Tool-Console/src/Console.csproj
RUN cd /bin/LANDIS_Linux/Core-Model-v8-LINUX/Tool-Console/src && dotnet build -c Release

# ################################################################
# # FINISHING
# ################################################################

# # Re-configure git for latest version of HTTP protocol
RUN git config --global --unset http.version
