FROM ubuntu:22.04

USER root

# Set non-interactive status for builds
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies including sudo, ca-certificates, and gnupg for key management
RUN apt-get update && \
    apt-get install -y sudo apt-transport-https \
    ca-certificates gnupg curl software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add GitHub CLI GPG key and repository
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/etc/apt/trusted.gpg.d/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/trusted.gpg.d/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && \
    apt-get install -y gh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install additional dependencies
RUN apt-get update && \
    apt-get install -y git \
    libjpeg62 \
    libpng16-16 \
    wget \
    unzip && \
    add-apt-repository universe && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python 3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    numpy \
    pandas \
    rasterio \
    geopandas \
    scipy \ 
    numpy

# Set the working directory
WORKDIR /opt

#RUN wget -q https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb && \
#    dpkg -i packages-microsoft-prod.deb && \
#    apt-get update && \
#    apt-get install -y dotnet-sdk-8.0 && \
#    apt-get clean && \
#    rm packages-microsoft-prod.deb && \
#    rm -rf /var/lib/apt/lists/*

RUN mkdir /bin/.dotnet/ && cd /bin/.dotnet/ \
&& wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh \
&& chmod +x ./dotnet-install.sh \
&& ./dotnet-install.sh --channel 8.0 -InstallDir /bin/.dotnet/  \
&& ./dotnet-install.sh --channel 8.0 --runtime aspnetcore -InstallDir /bin/.dotnet/ \
&& apt-get clean && rm -rf /var/lib/apt/lists/*
ENV DOTNET_ROOT=/bin/.dotnet
ENV PATH=$PATH:$DOTNET_ROOT:$DOTNET_ROOT/tools

# Install LANDIS
WORKDIR /opt

RUN git clone https://github.com/LANDIS-II-Foundation/Core-Model-v8-LINUX.git && \
    cd Core-Model-v8-LINUX/Tool-Console/src && dotnet build -c Release

RUN cd /opt/Core-Model-v8-LINUX/ && \
    git clone https://github.com/LANDIS-II-Foundation/Support-Library-Dlls-v8.git && \
    mv Support-Library-Dlls-v8/* /opt/Core-Model-v8-LINUX/build/extensions

# Thanks to Clement Hardy https://github.com/Klemet
COPY ./editing_csproj_LANDIS-II_files.py /opt/Core-Model-v8-LINUX

#SCRPPLE test DGS compliant (this is the version within ML's personal repo- WORKS)
RUN cd /opt/Core-Model-v8-LINUX && \
    git clone https://github.com/LANDIS-II-Foundation/Extension-Social-Climate-Fire.git && \
    cd Extension-Social-Climate-Fire && \
    #git checkout b463ea378f1bcde4369907a408dfe64b9cc52c7a && \
    cd /opt/Core-Model-v8-LINUX/Extension-Social-Climate-Fire/src && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./SocialClimateFire.csproj && \
    dotnet build -c Release && \
    dotnet /opt/Core-Model-v8-LINUX/build/Release/Landis.Extensions.dll add "/opt/Core-Model-v8-LINUX/Extension-Social-Climate-Fire/deploy/installer/Scrapple 4.txt"

# Output Biomass (WORKS)
RUN wget -O master.zip https://github.com/LANDIS-II-Foundation/Extension-Output-Biomass/archive/refs/heads/master.zip && \
    unzip master.zip -d /opt/Core-Model-v8-LINUX/ && \
    rm master.zip && \
    cd /opt/Core-Model-v8-LINUX/Extension-Output-Biomass-master/src && \
    #cp /opt/Core-Model-v8-LINUX-main/build/extensions/Support-Library-Dlls-v8-main/*.dll /opt/Core-Model-v8-LINUX-main/build/extensions/Extension-Output-Biomass-master/src/lib/ && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./output-biomass.csproj && \
    dotnet build -c Release && \
    dotnet /opt/Core-Model-v8-LINUX/build/Release/Landis.Extensions.dll add "/opt/Core-Model-v8-LINUX/Extension-Output-Biomass-master/deploy/installer/Output Biomass 4.txt"

# Output Biomass Community
RUN wget -O master.zip https://github.com/LANDIS-II-Foundation/Extension-Output-Biomass-Community/archive/refs/heads/master.zip && \
    unzip master.zip -d /opt/Core-Model-v8-LINUX/ && \
    rm master.zip && \
    cd /opt/Core-Model-v8-LINUX/Extension-Output-Biomass-Community-master/src && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./output-biomass-community.csproj && \
    dotnet build -c Release && \
    dotnet /opt/Core-Model-v8-LINUX/build/Release/Landis.Extensions.dll add "/opt/Core-Model-v8-LINUX/Extension-Output-Biomass-Community-master/deploy/installer/Output Biomass Community 3.txt"

# Output Biomass Reclass
RUN wget -O master.zip https://github.com/LANDIS-II-Foundation/Extension-Output-Biomass-Reclass/archive/refs/heads/master.zip && \
    unzip master.zip -d /opt/Core-Model-v8-LINUX/ && \
    rm master.zip && \
    cd /opt/Core-Model-v8-LINUX/Extension-Output-Biomass-Reclass-master/src && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./output-biomass.csproj && \
    dotnet build -c Release && \
    dotnet /opt/Core-Model-v8-LINUX/build/Release/Landis.Extensions.dll add "/opt/Core-Model-v8-LINUX/Extension-Output-Biomass-Reclass-master/deploy/installer/Output Biomass Reclass 4.txt"

# Output Max Spp Age
RUN wget -O master.zip https://github.com/LANDIS-II-Foundation/Extension-Output-Max-Species-Age/archive/refs/heads/master.zip && \
    unzip master.zip -d /opt/Core-Model-v8-LINUX/ && \
    rm master.zip && \
    cd /opt/Core-Model-v8-LINUX/Extension-Output-Max-Species-Age-master/src && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./max-species-age.csproj && \
    dotnet build -c Release && \
    dotnet /opt/Core-Model-v8-LINUX/build/Release/Landis.Extensions.dll add "/opt/Core-Model-v8-LINUX/Extension-Output-Max-Species-Age-master/deploy/installer/Output MaxSpeciesAge 4.txt"

# GIPL (WORKS)
RUN wget https://github.com/LANDIS-II-Foundation/Library-GIPL/archive/master.zip && \
    unzip master.zip -d /opt/Core-Model-v8-LINUX/ && \
    rm master.zip && \
    mv /opt/Core-Model-v8-LINUX/Library-GIPL-master/ /opt/Core-Model-v8-LINUX/Library-GIPL/ && \
    cd /opt/Core-Model-v8-LINUX/Library-GIPL/src && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./GiplDamm.csproj && \
    dotnet build -c Release && \
    cp /opt/Core-Model-v8-LINUX/Library-GIPL/src/bin/Debug/netstandard2.0/Landis.Extension.GiplDamm.dll /opt/Core-Model-v8-LINUX/build/extensions/.

# SHAW (WORKS)
RUN wget https://github.com/LANDIS-II-Foundation/Library-Shaw/archive/refs/heads/master.zip && \
    unzip master.zip -d /opt/Core-Model-v8-LINUX && \
    rm master.zip && \
    mv /opt/Core-Model-v8-LINUX/Library-Shaw-master/ /opt/Core-Model-v8-LINUX/Library-Shaw/ && \
    cd /opt/Core-Model-v8-LINUX/Library-Shaw/src && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./ShawDammNewInputs.csproj && \
    dotnet build -c Release && \
    cp /opt/Core-Model-v8-LINUX/Library-Shaw/src/bin/Debug/netstandard2.0/Landis.Extension.ShawDamm.dll /opt/Core-Model-v8-LINUX/build/extensions/.

# Biomass Succession
    RUN cd /opt/Core-Model-v8-LINUX/ && \
    git clone https://github.com/LANDIS-II-Foundation/Extension-Biomass-Succession.git && \
    cd /opt/Core-Model-v8-LINUX/Extension-Biomass-Succession && \
    #git checkout 58ad3673e02abe82f437a6b68c44220c51351091 && \
    cd /opt/Core-Model-v8-LINUX/Extension-Biomass-Succession/src && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./biomass-succession.csproj && \
    dotnet build -c Release && \
    dotnet /opt/Core-Model-v8-LINUX/build/Release/Landis.Extensions.dll add "/opt/Core-Model-v8-LINUX/Extension-Biomass-Succession/deploy/installer/Biomass Succession 7.txt"

# NECN (WORKS)
RUN cd /opt/Core-Model-v8-LINUX/ && \
    git clone https://github.com/LANDIS-II-Foundation/Extension-NECN-Succession.git && \
    #cd /opt/Core-Model-v8-LINUX/Extension-NECN-Succession && \
    #git checkout 37ce246c37bab3448e3db134373deb56063e14ac && \
    cd /opt/Core-Model-v8-LINUX/Extension-NECN-Succession/src && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./NECN-succession.csproj && \
    dotnet build -c Release && \
    dotnet /opt/Core-Model-v8-LINUX/build/Release/Landis.Extensions.dll add "/opt/Core-Model-v8-LINUX/Extension-NECN-Succession/deploy/installer/NECN_Succession8.txt"

# DGS (WORKS)
RUN wget https://github.com/LANDIS-II-Foundation/Extension-DGS-Succession/archive/refs/heads/v8.zip && \
    unzip v8.zip -d /opt/Core-Model-v8-LINUX/ && \
    rm v8.zip && \
    mv /opt/Core-Model-v8-LINUX/Extension-DGS-Succession-8/ /opt/Core-Model-v8-LINUX/Extension-DGS-Succession/ && \
    #best bet is to remove the main support dlls from DGS repo then push latest
    rm /opt/Core-Model-v8-LINUX/Extension-DGS-Succession/src/lib/*.dll && \
    #cp /opt/Core-Model-v8-LINUX/Extension-NECN-Succession/src/lib/*.dll /opt/Core-Model-v8-LINUX/Extension-DGS-Succession/src/lib/ && \
    cd /opt/Core-Model-v8-LINUX/Extension-DGS-Succession/src && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./DGS-succession.csproj && \
    dotnet build -c Release && \
    dotnet /opt/Core-Model-v8-LINUX/build/Release/Landis.Extensions.dll add "/opt/Core-Model-v8-LINUX/Extension-DGS-Succession/deploy/installer/DGS_Succession 1.102.txt"

RUN cd /opt/Core-Model-v8-LINUX && \
    rm /opt/Core-Model-v8-LINUX/build/extensions/Landis.Library.InitialCommunity.Universal.dll && \
    wget https://github.com/LANDIS-II-Foundation/Library-Initial-Community/archive/refs/heads/master.zip && \
    mkdir /opt/Core-Model-v8-LINUX/Initial-Community-main/ && \
    unzip master.zip -d /opt/Core-Model-v8-LINUX/Initial-Community-main/ && \
    rm master.zip && \
    cd /opt/Core-Model-v8-LINUX/Initial-Community-main/Library-Initial-Community-master/ && \
    python3 /opt/Core-Model-v8-LINUX/editing_csproj_LANDIS-II_files.py ./initial-community.csproj && \
    dotnet build -c Release

# Add a hint path for all of the extensions to the Tool-Console csproj file and then rebuild it
# need to add max species age just not sure on syntax
RUN sed -i '/<\/Project>/i \
<ItemGroup>\n\
    <Reference Include="Landis.Extension.Succession.Biomass-v7.dll">\n\
        <HintPath>../../build/extensions/Landis.Extension.Succession.Biomass-v7.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Library.Metadata-v2">\n\
        <HintPath>../../build/extensions/Landis.Library.Metadata-v2.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Library.Succession-v9.dll">\n\
        <HintPath>../../build/extensions/Landis.Library.Succession-v9.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Extension.Succession.NECN-v8.dll">\n\
        <HintPath>../../build/extensions/Landis.Extension.Succession.NECN-v8.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Extension.SocialClimateFire-v4.dll">\n\
        <HintPath>../../build/extensions/Landis.Extension.SocialClimateFire-v4.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Extension.GiplDamm.dll">\n\
        <HintPath>../../build/extensions/Landis.Extension.GiplDamm.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Extension.Output.Biomass-v4.dll">\n\
        <HintPath>../../build/extensions/Landis.Extension.Output.Biomass-v4.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Extension.Output.BiomassCommunity-v3.dll">\n\
        <HintPath>../../build/extensions/Landis.Extension.Output.BiomassCommunity-v3.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Library.UniversalCohorts-v2.dll">\n\
        <HintPath>../../build/extensions/Landis.Library.UniversalCohorts-v2.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Extension.Output.BiomassReclass-v4.dll">\n\
        <HintPath>../../build/extensions/Landis.Extension.Output.BiomassReclass-v4.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Extension.ShawDamm.dll">\n\
        <HintPath>../../build/extensions/Landis.Extension.ShawDamm.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Extension.Succession.DGS.dll">\n\
        <HintPath>../../build/extensions/Landis.Extension.Succession.DGS.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Library.BiomassHarvest-v3.dll">\n\
        <HintPath>../../build/extensions/Landis.Library.BiomassHarvest-v3.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Library.Climate-v5.dll">\n\
        <HintPath>../../build/extensions/Landis.Library.Climate-v5.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Library.HarvestManagement-v4.dll">\n\
        <HintPath>../../build/extensions/Landis.Library.HarvestManagement-v4.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="Landis.Library.HarvestManagement-v4.dll">\n\
        <HintPath>../../build/extensions/Landis.Library.HarvestManagement-v4.dll</HintPath>\n\
    </Reference>\n\
    <Reference Include="log4net.dll">\n\
        <HintPath>../../build/extensions/log4net.dll</HintPath>\n\
    </Reference>\n\
</ItemGroup>' /opt/Core-Model-v8-LINUX/Tool-Console/src/Console.csproj

# Move Support Libraries to the correct place
#RUN mv /opt/Core-Model-v8-LINUX-main/build/extensions/Support-Library-Dlls-v8-main/*.dll /opt/Core-Model-v8-LINUX-main/build/extensions/

RUN chown -R 1000:1000 /opt/Core-Model-v8-LINUX

ARG LOCAL_USER=user
ARG PRIV_CMDS='/bin/ch*,/bin/cat,/bin/gunzip,/bin/tar,/bin/mkdir,/bin/ps,/bin/mv,/bin/cp,/usr/bin/apt*,/usr/bin/pip*,/bin/yum'

RUN adduser --disabled-password --gecos "VICE_User" --uid 1000 user  && \
    usermod -aG sudo user && \
    echo "$LOCAL_USER ALL=NOPASSWD: $PRIV_CMDS" >> /etc/sudoers

RUN apt-get update && \
    apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    gettext-base git mercurial subversion \
    tmux && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> /home/user/.bashrc && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> /home/user/.zshrc && \
    chown -R user:user /opt/conda

# install ttyd
RUN curl -L "https://github.com/tsl0922/ttyd/releases/download/1.6.3/ttyd.x86_64" > ttyd && \
    chmod a+x ttyd && \
    mv ttyd /usr/local/bin/ttyd

RUN apt-get update && \
    apt-get install -y curl grep sed dpkg && \
    curl -L "https://github.com/krallin/tini/releases/download/v0.19.0/tini_0.19.0-amd64.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install a few dependencies for iCommands, text editing, and monitoring instances
RUN apt-get update && \
    apt-get install -y lsb-release apt-transport-https curl gnupg2 libfuse2 gcc less nodejs software-properties-common apt-utils glances htop nano  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y vim-nox && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y emacs-nox && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget -qO - https://packages.irods.org/irods-signing-key.asc | apt-key add - && \
    echo "deb [arch=amd64] https://packages.irods.org/apt/ $(lsb_release -sc) main" >> /etc/apt/sources.list.d/renci-irods.list && \
    apt-get update && \
    apt install -y irods-icommands

USER user

# set shell as bash and terminal as linux
ENV SHELL=bash
ENV TERM=xterm

# open port 7681 for ttyd
EXPOSE 7681

# changes tmux layout while running
COPY entry.sh /bin
RUN echo 'set-option -g status off' >> ~/.tmux.conf

# add iRODS iCommands to user profile as JSON
RUN mkdir /home/user/.irods

#RUN cd /opt/Core-Model-v8-LINUX-main/Tool-Extension-Admin/src && dotnet build -c Release
RUN echo "alias console='dotnet /opt/Core-Model-v8-LINUX/build/Release/Landis.Console.dll'" >> ~/.bashrc
#RUN echo "cd /opt/Core-Model-v8-LINUX-main/Tool-Console/src && dotnet build -c Release && cd" >> ~/.bashrc
RUN cd /opt/Core-Model-v8-LINUX/Tool-Console/src && dotnet build -c Release
ENTRYPOINT ["bash", "/bin/entry.sh"]

CMD ["ttyd", "bash"]

WORKDIR /home/user
