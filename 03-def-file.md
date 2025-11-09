# Building a Container from a Definition File

A definition file (`.def`) is a recipe that documents the container build process, including the base OS, packages to install, and commands to run. In this section we will build another Ubuntu container, but this time from a definition file and we will use the definition file to install Git and Curl into the container. 

Take a look at the definition file we made called `container-build.def`:
```bash 
cat container-build.def
```

Let's break down what these sections do when Apptainer builds the container:

* All definition files start with `Bootstrap` followed by the bootstrap agent which specifies the base operating system the container image will use. In this tutorial, we will be using the Docker bootstrap agent. Other agents you may come across are localimage, oras, and scratch.
* `From: ubuntu` indicates what image you want to use or the specific publisher in Docker Hub you are pulling from. In this case, we are using the Ubuntu repository and without further specifications, the starting OS will be the latest version of Ubuntu available on Docker Hub.
* The `%post` section is where new software and files can be downloaded and new directories can be made. Here we are updating package information, and this time we will install Git and Curl into the container.
* The `%runscript` section can be used to test your container; the commands under the `%runscript` section will be executed when the command `apptainer run` is used.  

## Build the Container

We will call our completed container `custom-container.sif` to differentiate it from the containers we built in the last section.

```bash
apptainer build custom-container.sif container-build.def
```
Let's test the container by using `apptainer run` to execute the runscripts we defined. 
```bash
apptainer run custom-container.sif
```

Output should show Curl and Git versions.

You can use `container-build.def` as a template to build your own custom containers. 

## Building a Container from a Local Image

You can also build on a container that is already on Tillicum. This is useful for layering additional software without downloading a new base. This can be useful as you develop more complex containers that take longer to build from scratch. 

For example, earlier in the workshop we pulled `python_latest.sif`. Now we will create a new image based on it and install common packages for data science. Then we'll use the container to execute a script that requires the package and outputs a simple plot. 

Take a look at the definition file we made called `fromlocal-build.def`:
```bash 
cat fromlocal-build.def
```
Notice that this time we are using `localimage` as the Bootstrap agent, which means that Apptainer will find the named image defined in the `From:` directive and use it as the base operating system image. The installation instructions for the packages then follow in the `%post` section, and the `%runscript` section contains instructions to print a greeting and the version of the packages installed when `apptainer run` is executed.

Like before, build the container using the definition file. `custom-python.sif` will be the name of the new container.

```bash
apptainer build custom-python.sif fromlocal-build.def
```
Let's test the container by using `apptainer run` to execute the runscripts we defined. 
```bash
apptainer run custom-python.sif
```
Let's test the container with `apptainer exec` and `plot_example.py`.

```bash
apptainer exec custom-python.sif python plot_example.py
```
Listing the container with `ls` will show that the output `example_plot.png` was generated successfully. 
