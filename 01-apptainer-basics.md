# Apptainer Containers on Tillicum

A container packages software together with the libraries and configuration it needs. Instead of installing software directly onto Tillicum (which can require administrator privileges or conflict with the host operating system), you run software inside a container that provides its own user-space environment.

On Tillicum , we use Apptainer, which is designed for shared HPC systems. Apptainer containers use the host system's kernel (the core of the operating system) but provide their own user space (applications, libraries, runtime settings). This is what allows containers to be lightweight and portable.

Because software package, libraries, and research pipelines carry their own dependencies, using a container can help with:
* Reproducibility: the environment is consistent across systems.
* Version control: multiple versions of the same tool can be used easily.
* Storage efficiency: containers are single files rather than thousands of separate package files.

## Container Image

Apptainer stores containers in a SIF file (Singularity Image Format). A SIF file is a compressed, read-only filesystem containing the environment. By default, you cannot modify files inside a SIF image. To make changes, the container must be rebuilt or converted to a writable format, which we will use later.

Apptainer commands you will see repeatedly:

```bash
apptainer pull   # download and convert container images
apptainer shell  # open an interactive shell inside the container
apptainer exec   # run a command in the container without a shell
```

## Pulling a Pre-built Container

We will pull a Python container from [DockerHub](https://hub.docker.com/), a public container repository. Although Docker is a different container system, Apptainer can convert Docker images automatically using `apptainer pull docker://....`

Multiple versions of python are available from DockerHub, and you can specify the version by providing a tag. For not we will pull the container without specifying a tag to pull the container tagged as the "latest" released version on DockerHub. 

```bash
apptainer pull docker://python
```
When the build finishes, list your directory:
```bash
ls
# python_latest.sif
```

### Disk Quota Notes
By default, Apptainer caches downloads in your home directory, which has a strict quota (10GB). If you get a “Disk quota exceeded” error, clear the cache:
```bash
apptainer cache clean
```
And then reset the destination of the apptainer cache for this session. 
```bash
export APPTAINER_CACHEDIR=$PWD
```

## Running Commands Inside the Container
Commands can be run inside the container interactively with `apptainer shell`. Open a shell into the python container we just pulled: 
```bash
apptainer shell python_latest.sif
```

The command prompt will change and now start with `Apptainer>`. This is how you know that you are now inside the Apptainer container. Input python into the terminal to open the container's Python shell:
```bash
Apptainer> python
```

Exit Python with Ctrl+D and exit the container with:
```bash
exit
```

You can compare host vs container Python versions:
```bash
python
# -bash: python: command not found
```
There is no native version of python installed for all users. But you can execute python commands with your container: 
```bash
apptainer exec python_latest.sif python --version
```
`apptainer exec` rather than `apptainer shell` sends a command to be executed inside the container, rather than first opening a shell into the container.

## Accessing Your Files (Tillicum Default Behavior)
On Tillicum, Apptainer is configured to automatically bind user-accessible storage (including GPFS workspaces i.e., `/gpfs`). That means your files are visible inside the container without any extra options.

We have provided a simple script for your to confirm your files are accessible. 
```bash 
cat pi.py
```
We can execute this script with our container: 
```bash
apptainer exec python_latest.sif python pi.py
```

## About Binding (Concept Only)
Although Tillicum binds core filesystems automatically, it is important to understand the idea of binding.

* Containers are isolated environments
* Binding “mounts” directories from the host into the container
* Other clusters, including Hyak Klone, require explicit binds

The general pattern looks like:
```bash
apptainer exec --bind /gpfs python_latest.sif python pi.py
```

On Hyak Klone: 
```bash
# An example of the same command adapted for Hyak Klone
apptainer exec --bind /gscratch python_latest.sif python pi.py
```

You will need this when:
* Running containers on some HPC/cloud environments
* Binding large datasets outside standard paths
