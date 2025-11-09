# Building a Container Interactively (Sandbox)

The sandbox method creates a writable version of a container that you can modify interactively. This is useful for exploring container development, but it does not keep a record of the changes made, unlike definition files, which will be demonstrated in the next section. 

## Pull an Ubuntu Container

We’ll pull the latest Ubuntu container from Docker Hub:

```bash
apptainer pull docker://ubuntu
```
Check the file:
```bash
ls
# ubuntu_latest.sif
```
Inspect the container:
```bash
apptainer inspect ubuntu_latest.sif
```
Execute a command inside the container to see that `git` is missing:
```bash
apptainer exec ubuntu_latest.sif git --version
# FATAL:   "git": executable file not found in $PATH
```

## Convert to Sandbox
Create a writable sandbox directory:
```bash
apptainer build --sandbox ubuntu_latest ubuntu_latest.sif
```
View the directory:
```bash
ls
ls ubuntu_latest
```
The `ubuntu_latest` directory is a full Ubuntu root filesystem unpacked into a writable form. Viewing it with `ls` shows the same directory structure as a standard Ubuntu installation.

You should see directories similar to:
```bash
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  
proc  root  run  sbin  srv  sys  tmp  usr  var
```

These are the standard components of a typical Ubuntu operating system environment.

Enter the sandbox interactively:

```bash
apptainer shell --writable --fakeroot ubuntu_latest
```
* `--writable`: allows changes inside the container.
* `--fakeroot`: simulates root access for users without root privileges.

Note: When entering a sandbox container, your working directory inside the container may default to `/root` if the directory you were in on the host doesn’t exist in the container. This does not affect where software is installed. Software installed with apt always goes into the container’s filesystem, not the host system.

## Install Software

Update the package list and install Git:

```bash
apt -y update
apt -y install git
git --version
# git version 2.43.0
```
Inside the container, the apt package manager is operating on the container’s own root filesystem.

Exit the container:
```bash
exit
```

## Rebuild Container with Changes

Convert the sandbox back into a `.sif` container image:
```bash
apptainer build ubuntu_latest_git.sif ubuntu_latest
```
We'll call this container `ubuntu_latest_git.sif` to differentiate it from the original `ubuntu_latest.sif`. 

Test Git:
```bash
apptainer exec ubuntu_latest_git.sif git --version
```
And compare that with the native version of Git for Tillicum users. 
```bash
git --version
# git version 2.47.3
```
