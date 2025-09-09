<p align="center"><img src="logo_Landis_Docker_Apptainer.svg" width="500"></p>

<h1 align="center">LANDIS-II Docker and Apptainer</h1>

Resources to create and use a Docker Image and an Apptainer containing the [LANDIS-II model](https://www.landis-ii.org/) and its extensions, for use on almost any environment, including supercomputing clusters.

## 🐋 What is Docker ?

Docker is an open-source platform designed for creating, deploying, and managing applications using what are called "containers".

Containers can be seen as a kind of special file that contain an entire computer environment, including an OS (like Linux or Windows) and as many programs, packages or libraries as you want to install in it.

Docker containers are created, managed and run on your computer using the Docker Engine (which you have to install), and can be interacted with easily. But when run, what's happening in the container is separated from what goes on in the rest of your computer. However, you can make some files from your computer available in the container (like LANDIS-II scenario files), as we'll see later in this readme.

Using a Docker container to run LANDIS-II has many advantages :

- It's easy to install (see below; one program to install in your computer + one command in a terminal)
- You will be able to run LANDIS-II on any platform (Mac OS, Windows, Linux, etc.) with no compatibility issue.
    - The only exception is for High Performance Computing (HPC) environment, like supercomputing clusters. In that case, use Apptainer (see below)
- Your LANDIS-II simulations will be highly replicable, since they will not depend on the environment of your own work computer (e.g. R and Python packages you have, etc.); but only on what you define in the Dockerfile (the file that will generate your Docker container)
- You can easily deploy different LANDIS-II environments (sets of extensions + R or Python packages) on your computer without having conflicts or problems between them.
- **You ensure that LANDIS-II will always have the right dependencies to function**. 

To learn more about Docker, you can check [one of the many videos explaining the concept](https://youtu.be/_dfLOzuIg2o).

## 📦 What's an Apptainer ?

[Apptainer](https://apptainer.org/) (formerly called "Singularity") is a program that creates "containers" similar to Docker. These containers contain an entire operating system (OS) like Ubuntu, along with every program or dependencies you might want to install in it. As for Docker containers, and Apptainer can still edit and modify files that are "outside" of the Apptainer if they are made available inside of the Apptainer through a special command. See below for more.

The differences between Docker containers and Apptainer are very technical; for example, Docker has a "layering" system that allows different Docker containers running on the same machine to use the same files that they share with each other. But the only thing that will certainly matter to you as a LANDIS-II user is that Apptainers are made to be run on a High Performance Computing environment, where the security standards are much greater, and where Docker containers are often forbidden from use for different reasons.

The biggest advantage of Apptainers is that just like Docker Containers, they will ensure that LANDIS-II always have all of the necessary dependencies to run anywhere, especially on supercomputing clusters. This is crucial, as supercomputing clusters tend to restrain the programs/modules/packages/dependencies one can load inside your session. This can create hair-pulling scenarios where any update of the global environment in the clusters breaks your LANDIS-II installation, as it cannot access the right dependencies anymore. 

> 💡 While Docker containers are often forbiden on High Performance Computing environments, they are generaly safe to use on your computer. They can be used, like almost any program, to hurt your computer; especially if they contain older version of packages or programs that contain known vulnerabilities, and if they are run in ways that make them accessible to attakers. In case of doubt, use Docker Scout to analyze a container before running a container. You can find more information about the security of Docker Containers [here](https://www.docker.com/blog/container-security-and-why-it-matters/). **While several vulnerabilities exist in the Docker containers that you can create with this repository, they should not cause problems to your computer as long as you run the containers for LANDIS-II simulations and with LANDIS-II scenario files that you trust.**

## ⚙ How to use

We provide several "flavours" of images, contributed by users with different use cases and needs.
Simply select an image that best suits your needs - you can use "as is" or simply as a starting point for further customizations.

> 💡 If you want to use LANDIS-II on a HPC environment (e.g. supercomputing clusters),
> then you can simply download one of the Apptainer files available in the
> [Releases](https://github.com/LANDIS-II-Foundation/Tool-Docker-Apptainer/releases) section
> of this repository and follow the instruction below to run it with the right command.
> However, we recommend that you familiarize yourself with the rest of the instructions to learn
> how to edit and customize them for your own research purposes.

### Generic images

These images provide a minimal LANDIS-II installation, including GDAL, plus a python installation.

> 💡 The `Clean_Docker_*` images hardcode the extensions and their specific commits directly in the Dockerfile,
> whereas the others refer to a `.yaml` file (e.g., [`extensions-v8-release.yaml`](extensions-v8-release.yaml)) to define the versions used.
> When customizing multiple images, it is easier to use these shared sets of extensions,
> especially when important updates (like bug fixes) are made to the extensions and images need to be updated and rebuilt.

**LANDIS-II v7 images**

| Image name             | Subdirectory                               | Description                                         |
| ---------------------- | ------------------------------------------ | --------------------------------------------------- |
| `landis-ii-v7-linux`   | `Clean_Docker_LANDIS-II_7_AllExtensions/`  | LANDIS-II v7 (Ubuntu 22.04); fixed versions of v7-compatible extensions; **superseded by `landis-ii-v7-release`** |
| `landis-ii-v7-release` | `Docker-LANDIS-II-v7-release/`             | LANDIS-II v7 (Ubuntu 22.04); [fixed versions of v7-compatible extensions](extensions-v7-release.yaml) |

**LANDIS-II v8 images**

| Image name             | Subdirectory                               | Description                                         |
| ---------------------- | ------------------------------------------ | --------------------------------------------------- |
| `landis-ii-v8-linux`   | `Clean_Docker_LANDIS-II_8_AllExtensions/`  | LANDIS-II v8 (Ubuntu 22.04); fixed versions of v8 extensions; **superseded by `landis-ii-v8-release`** |
| `landis-ii-v8-release` | `Docker-LANDIS-II-v8-release/`             | LANDIS-II v8 (Ubuntu 24.04); [fixed versions of v8 extensions](extensions-v8-release.yaml) |

### R/Rstudio images

These images are based on the generic images and add R and/or a running Rstudio Server instance.

**LANDIS-II v8 images**

| Image name             | Subdirectory                               | Description                                         |
| ---------------------- | ------------------------------------------ | --------------------------------------------------- |
| `landis-ii-v8-r`       | `Docker-LANDIS-II-v8-release-R/`           | LANDIS-II v8 (Ubuntu 24.04); [fixed versions of v8 extensions](extensions-v8-release.yaml); |
| `landis-ii-v8-rstudio` | `Docker-LANDIS-II-v8-release-Rstudio/`     | LANDIS-II v8 (Ubuntu 24.04); [fixed versions of v8 extensions](extensions-v8-release.yaml); Rstudio Server |

### Other custom images

**LANDIS-II v8 images**

| Image name             | Subdirectory                               | Description                                         |
| ---------------------- | ------------------------------------------ | --------------------------------------------------- |
| `landis-ii-v8-latest`  | `Clean_Docker_LANDIS-II_8_Latest_Commits/` | LANDIS-II v8 (Ubuntu 22.04); latest versions of v8 extensions; `miniconda` and [iRods](https://irods.org/) |

### 📥 Get a prebuilt image

**Authenticate with the GitHub Container Registry:**

1. Setup a personal access token following [these instructions](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic);

2. Login with Docker:

    ```shell
    export GHCR_PAT=YOUR_TOKEN
    echo $GHCR_PAT | docker login ghcr.io -u USERNAME --password-stdin
    ```

**Download the image:**

```shell
## replace <imagename> with one from above
docker pull ghcr.io/landis-ii-foundation/<imagename>:main
```

### 📦 Building the docker image containing LANDIS-II

> 💡 A Docker image is simply a "template" to initialize a Docker container.
> You can initialize and run many Docker Containers from one Docker image.
> Imagine that the Docker image is a blueprint for a house or a "demo" house,
> while Docker containers are houses where people actually live.
> You first need to make the Docker image before creating a Docker container. 

- Download [Docker Desktop](https://www.docker.com/) on your computer.
  You can also install Docker through a command prompt if you are on Linux.
    - On Windows, Docker Desktop will ask you by default to be integrated with what is called "WSL",
      the Windows Subsystem for Linux. The WSL can be seen as a "Linux emulator" for Windows,
      and it can help for a lot of things. It's recommended that you use the WSL integration;
      however, you might need to enable the WSL before starting Docker Desktop, or you'll get an error at launch.
      To enable the WSL, simply open a Powershell command prompt and use `wsl --install` as a command.
      Then restart your computer.
- Launch Docker Desktop. This will start the Docker Engine on your computer.
- Download the entire contents of this repository (several files needed to build are shared among multiple images);
- Open a terminal on your computer (e.g., a Powershell command prompt if you're on Windows)
  and change your working directory to that of your local copy of this repository.
- Select an image flavour to build / use, and follow the specific build instructions
  found in the `README.md` in that flavour's subdirectory.

	> 💡 Generally, the build command will look like the following:
	> 
	> ```shell
	> docker build <directory> -f <path/to/Dockerfile> -t <my_image_name>
	> ```
	> 
	> - `<directory>` specifies the Docker 'build context', which determines the set of local files
	>   the bulid process has access to. If `<directory>` is specified as the root directory of the repository,
	>   then shared files or directories (e.g., `extension_files/`, `scripts/`, and any `*.yaml` files
	>   can be passed to the build process. Whereas, if `<directory>` is specified as one of the repository
	>   subdirectories (e.g., `Clean_Docker_LANDIS-II_8_AllExtensions`), then the build will only use
	>   the files contained in that subdirectory.
	> - `<path/to/Dockerfile>` specifies the *relative* path to the `Dockerfile` used to build the image.
	>   A `Dockerfile` is simply a text file, so you can view it with any text editor.
  >   It contains a set of Linux commands to set up the container environment
  >   (e.g., install software dependencies) and download the code to build and run LANDIS-II.
	> - `<my_image_name>` is simply a name to give to your image (e.g., `landis-ii` or whatever works best for you).


> [!WARNING]
> You may get the occaisional error during the build that are due to internet connection issues.
> For example, when the build is downloading files from GitHub it may error with messages similar to:
> 
> ```shell
> HTTP request sent, awaiting response... 429 Too Many Requests`
> ```
> 
> We are working on ways to fix this; but because these errors are typically transient,
> you can simply restart the build process by rerunning the `docker build` command.
> The build should continue where it left off (due to caching).
> 
> NOTE: Using a VPN may create additional issues with some commands.
> If you encounter errors with a VPN enabled, you can try disabling your VPN and retrying the build.

### 📝 (Optional) Customizing the Docker image image with R packages, Python packages, or anything else

The Docker images we have created contain the minimal set of the components necessary to run
LANDIS-II in the container, and cover several important use cases (but not all!).
If the images provided don't meet all of your needs, feel free to customize with additional components as needed for your study.
**Everything you put in your Docker image can be made available to other research groups looking to replicate, improve or update your methodology if you share the `Dockerfile` you used to create it.**
As such, we recommend that you take full advantage of it. The sky is the limit!

1. Make a copy of one of the 'flavour' subdirectories and give it a custom name;
2. Edit the `Dockerfile` with any text editor to add additional build steps using the Docker `RUN` command
   (see the [Dockerfile syntax](https://docs.docker.com/reference/dockerfile/) documentation);
   
  > 💡 Example: install additonal Python packages
  > 
  > Add the following build step to your Dockerfile:
  > 
  > ```shell
  > RUN pip install numpy rasterio pandas
  > ```

3. Edit the `README.md` file to update the `docker build` command for your image,
   by editing the paths used for build context and/or the Dockerfile, and the name of your image;
4. Build your image;
5. (Optional) Push your newly build image to a container registry to share with others
   (e.g., [Docker Hub](https://hub.docker.com/) or [GitHub](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry));

  > 💡 You can also share the `Dockerfile` you created (and any additional files needed to build the image),
  > rather than needing to share the built image.
  > The `Dockerfile` is very light as it is only a text file, and can be shared in any way you like.

6. Start a container instance based on your new image following the documentation in the `README.md`;

### ⚡ Running a Docker container based on the image

#### Containers based on generic images

There are several ways to run a Docker container:

- You can run it "interactively" via the `-it` argument, which will allow you to interact with your container in your command prompt.
  From there, you can look at the files that are inside the container, run a LANDIS-II scenario, etc.
- Or, you can run it in a non-interactive way and specify a couple of commands to execute.
  When the commands are done (or if they fail), the container will simply shut down.
  This approach is useful for running a single LANDIS-II simulation (or other workflow).
  Multiple isolated and independent runs can be run concurrently using this approach
  (depending on the computational resources available on the local host machine).

In both cases, you can create a "bind", which will allow your container to access and edit files that are on your computer, outside of the container. This is most likely what you will want to do to run a LANDIS-II simulation on your computer; the container will then be able to read the scenario files, run LANDIS-II, and create the output files in the same folder.

To run an interactive Docker container with a bind, use the following command :

```shell
docker run -it \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="<SCENARIO_FOLDER_FULL_PATH_ON_COMPUTER>",dst=/scenarioFolder \
  --name <MY_LANDIS_CONTAINER_NAME> \
  <LANDIS_DOCKER_IMAGE_NAME>
```

- `-it` will run the container interactively
- `--mount type=bind,src="<SCENARIO_FOLDER_FULL_PATH_ON_COMPUTER>",dst=/scenarioFolder` will bind make the folder containing LANDIS-II scenario files on your computer available inside the container, at the path `/scenarioFolder`. Simply replace `<SCENARIO_FOLDER_FULL_PATH_ON_COMPUTER>` with the full path to the folder on your compute (for example, `C:\Users\JohnDoe\LANDIS-II_Simulation`).
- limit system resources available to the container by passing e.g., `--memory=64g` and `--cpus=8`;
- `<MY_LANDIS_CONTAINER_NAME>` is simply a name to give the *container* (useful to distinguish among several containers initialized from the same image);
- `<LANDIS_DOCKER_IMAGE_NAME>` is simply the name of the Docker image we have built earlier (for example, `landis_ii`).

To run a non-interactive Docker container with a bind mount, use:

```shell
docker run \
  --cpus=4 \
  --memory=64g \
  --mount type=bind,src="<SCENARIO_FOLDER_FULL_PATH_ON_COMPUTER>",dst=/scenarioFolder \
  --name <MY_LANDIS_CONTAINER_NAME> \
  <LANDIS_DOCKER_IMAGE_NAME> /bin/sh -c "<COMMAND1> && <COMMAND2>"
```

- Here, `/bin/sh -c "<COMMAND1> && <COMMAND2>` allow use to define the commands we want to run once the container is running.
  You can add more commands with the `&&` symbol.

#### Rstudio containers

These containers are intended for interactive workflows, via Rstudio.

When launching an instance of the container:

- specify the local port to use to connect to the container by passing `-p` with appropriate arguments
  (e.g., `-p 127.0.0.1:8080:8787` allows connections on local port 8080; 8787 is the port used by Rstudio on the container);
- a custom `PASSWORD` can be specified (if not specified, a random one will be used and displayed *once* at container launch);
- local directories can be mounted as above;
- `USERID` and `GROUPID` specify the user and group ids, respectively, and can be specified
  to ensure user file permissions of the container match those of the mounted volume (defaults: `1000`)
  (see <https://rocker-project.org/images/versioned/rstudio.html#userid-and-groupid>);
- limit system resources available to the container by passing e.g., `--memory=64g` and `--cpus=8`;

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
  landis-ii-rstudio:release
```

To access the running container's Rstudio instance:

Open your web browser and connect to `localhost:8080`.
Log in using username `rstudio` and the password set above.

**See also:** <https://rocker-project.org/images/versioned/rstudio.html#how-to-use>

### 🌳 Launching a LANDIS-II simulation through the container

The Docker containers created with the Dockerfiles present in this repository will be running in an Ubuntu (Linux) environment.
As such, the command to launch LANDIS-II in the container will be a bit different.
To launch a LANDIS-II simulation from inside the container, you will need to change the working directory to the folder containing your scenario files, and then run :

```shell
cd path/to/scenarioFolder/
dotnet $LANDIS_CONSOLE scenario.txt
```

- `dotnet` is the Linux program that allows us to run LANDIS-II on Linux, since it's coded in `C#` (a programming language made by Microsoft);
- `$LANDIS_CONSOLE` is an environment variable that contains the location of the LANDIS-II program
  in the container (in `/bin/LANDIS_Linux/build/Release/Landis.Console.dll`);
- `scenario.txt` is the name of your scenario fiMY_LANDIS_CONTAINER_NAMEle;

As such, if you want to run LANDIS-II through an interactive container :

- Run the following command:

  ```shell
  docker run -it \
    --cpus=4 \
    --memory=64g \
    --mount type=bind,src="<SCENARIO_FOLDER_FULL_PATH_ON_COMPUTER>",dst=/scenarioFolder \
    --name <MY_LANDIS_CONTAINER_NAME> \
    <LANDIS_DOCKER_IMAGE_NAME>
  ```
  
- In the interactive mode, use `cd` to change your working directory to go into `/scenarioFolder` (or where you can access your scenario files through the bind)
- Once you are in the right folder, run `dotnet $LANDIS_CONSOLE scenario.txt`, and the scenario should run.

If you want to run the LANDIS-II scenario in an non-interactive container (useful to automatize your simulations), here is the full command :

```shell
docker run \
--cpus=4 \
  --memory=64g \
  --mount type=bind,src="<SCENARIO_FOLDER_FULL_PATH_ON_COMPUTER>",dst=/scenarioFolder \
  --name <MY_LANDIS_CONTAINER_NAME> \
  <LANDIS_DOCKER_IMAGE_NAME> /bin/sh -c "cd /scenarioFolder && dotnet $LANDIS_CONSOLE scenario.txt"
```

Simply make sure that the command `cd /scenarioFolder` goes where your `scenario.txt` file is located. If it's in a subfolder, change it to `cd /scenarioFolder/subFolder`.

### 📦 (Optional) Building an apptainer file to use LANDIS-II on HPC environments (e.g. supercomputing clusters)

You can easily create an Apptainer file (in `.sif` format) from a Docker image to deploy on HPC environments.

- First, you need to install Apptainer (the program) on your computer. This can only be done in Linux.
  If you are on Windows, you can use the WSL that we installed with Docker Desktop (see above)
  to run an Ubuntu console on your Windows computer. Simply run `wsl -d Ubuntu` in a Powershell terminal.
  You can also create a Docker container that contains Apptainer.
  See [this repository](https://github.com/kaczmarj/apptainer-in-docker) for one.
- Next, you need to export your Docker image as an archive file.
  Use `docker save <NAME OF DOCKER IMAGE> -o <DOCKER ARCHIVE FILE NAME>.tar` in the terminal.
- Then, you need to use a Linux terminal with Apptainer installed, and change your working directory
  to go the folder containing your `.tar` docker archive file.
- Finally, use this command to build the Apptainer image:
  
  ```shell
  apptainer build --fakeroot <NAME OF YOUR APPTAINER FILE>.sif docker-archive://<DOCKER ARCHIVE FILE NAME>.tar
  ```

  > ⚠ This compilation often takes a lot of RAM, and will fail if you do not have enough of it available!
  > If that's the case, you can download and use one of the `.sif` files available from the
  > [Releases](https://github.com/LANDIS-II-Foundation/Tool-Docker-Apptainer/releases) section of this repository.

To use the Apptainer on a HPC environment :

- Upload your LANDIS-II scenario files and your `.sif` Apptainer file on your HPC environment.
- In the terminal you use to interact with your HPC environment, load the package `apptainer` (which should be available).
- Go to where your `.sif` files are located, and use the following command:

  ```shell
  apptainer exec -C -B <FULL_PATH_TO_FOLDER_WITH_SCENARIO_FILE> <NAME OF YOUR APPTAINER FILE>.sif /bin/sh -c "cd <FULL_PATH_TO_FOLDER_WITH_SCENARIO_FILE> && dotnet $LANDIS_CONSOLE scenario.txt"
  ```

As you can see, the command is very similar to the one used with Docker:

- `apptainer` calls the `apptainer` package, which knows how to use your `.sif` file;
- `exec` tells the `apptainer` package that we are going to run commands inside the Apptainer;
- `-C` tells `apptainer` remove all of the folder binding that gets done automatically by Apptainer.
  It will only bind the folders to the Apptainer that we tell him to.
  The folder binding is essential: it's the process through which your Apptainer will become able to access files from outside the Apptainer file.
- `-B <FULL_PATH_TO_FOLDER_WITH_SCENARIO_FILE>` binds the folder containing your scenario files.
  Replace `<FULL_PATH_TO_FOLDER_WITH_SCENARIO_FILE>` with the **full, absolute path** to your scenario folder on your HPC environment (e.g. `/home/Klemet/LANDIS-II_Simulations/Simulation1`).
  These files will become accessible inside the Apptainer at the same path.
- `<NAME OF YOUR APPTAINER FILE>.sif` is simply the name of the Apptainer file.
-  `/bin/sh -c "... && ..."` is used to give several commands at once to do inside the Apptainer.
  These two commands (`cd` and `donet`) are described just below.
-  `cd <FULL_PATH_TO_FOLDER_WITH_SCENARIO_FILE>` is a the first command we launch while inside the Apptainer:
  we simply use it to go inside the folder containing your LANDIS-II scenario files,
  which are accessible inside the Apptainer thanks to `-B <FULL_PATH_TO_FOLDER_WITH_SCENARIO_FILE>` that we used before, which "binded" them inside it.
-  `dotnet $LANDIS_CONSOLE scenario.txt` is the final command we launch to launch the simulation.


## 🐛 Problem, issue or bug ?

- **I'm encountering an error when compiling the Docker image where it says that it fails to download from GitHub (something like `error unexpected disconnect while reading sideband packet`). What should I do ?**

You're most likely using Windows; this error seems to be due to an outdated SSH library that deal with the encryption of connections. See [here](https://github.com/orgs/community/discussions/48568#discussioncomment-8510498) for more information. It seems like it can be solved by downloading the latest beta version of the SSH library of Microsoft, by using the following command in a Powershell prompt :

```powershell
 winget install Microsoft.OpenSSH.Beta
```

- **I'm encountering an error when compiling the Docker image at the beginning of the process, where commands like `apt update` and `apt upgrade` are used. What should I do ?**
 
Most likely, this error is due the fact that the command returned an interactive prompt (e.g., `Do you want to continue? [Y/n]Abort`).
Because Docker cannot answer this prompt, the command is aborted and returns an error.
Simply change the command to something like `apt-get update -y` in your Dockerfile; the `-y` flag will confirm the prompt automatically for you.

- **I've got another error that is not indicated here ?**

Please head to the [LANDIS-II users group](https://www.landis-ii.org/users) if you have questions or issues !
