# Tillicum Containers Tutorial

## Overview

**Containers** are lightweight, isolated software environments that encapsulate an application along with its dependencies and runtime settings. They provide a consistent and reproducible way to package, distribute, and run software across different computing environments.

Tillicum offers a shared computing environment with a baseline software stack and commonly used tools pre-installed. For security, users do not have root or sudo access and are responsible for managing any additional software required for their research. Guidance and support are available through documentation and the [Research Computing help desk](https://uwconnect.uw.edu/sp?id=sc_cat_item&sys_id=9e0fe8b58718fa906f1997dd3fbb35f3). Containers enable researchers to build and run customized software stacks on Tillicum in a secure, portable, and fully reproducible way—without requiring elevated system access.

🎯 **By completing this tutorial, you’ll learn how to:**
* Work with GPU-ready Apptainer containers on Tillicum, including pulling, inspecting, and running containers.
* Create sandbox environments and build customized container images.
* Access and use shared datasets from the Tillicum Data Commons.
* Run GPU-accelerated deep learning inference inside a container.
* Submit and monitor batch jobs on Tillicum using Slurm.

## Repository Structure

Each topic in this tutorial is contained in its own Markdown file for easy navigation:

| Section | Description |
| :- | :- |
| [00-preparation.md](./00-preparation.md) | Logging in via SSH and setting up your working directory |
| [01-apptainer-basics.md](./01-apptainer-basics.md) | Introducing Apptainer and commonly commands when working with containers on Tillicum |
| [02-sandbox.md](./02-sandbox.md) | Practice building a custom container interactively |
| [03-def-file.md](./03-def-file.md) | Practice building custom containers from definition files |
| [04-task.md](./04-task.md) | Hands-on exercise:  |

## Sources for pre-built Containers
   - **HIGHLY RECOMMENDED** - [DockerHub](https://hub.docker.com/)
   - **HIGHLY RECOMMENDED** - [NVIDIA NGC](https://catalog.ngc.nvidia.com/containers?filters=&orderBy=weightPopularDESC&query=&page=&pageSize=)
      and [For NVIDIA Containers for AI specifically](https://catalog.ngc.nvidia.com/?filters=&orderBy=weightPopularDESC&query=&page=&pageSize=)
   - [BioContainers](https://biocontainers.pro/registry)
   - Google: "your-software-name Dockerfile"

## Introduction Video

A link to the recording of the Novemeber 13, 2025 Tillicum Containers workshop will be added here when available.

## Feedback

We’d love your feedback to help improve this tutorial and future Tillicum trainings. After completing the tutorial or attending the workshop, please take a moment to fill out our [feedback form](https://forms.office.com/r/wvKwLnemmb).

## Additional Resources

- [Tillicum Documentation](https://hyak.uw.edu/docs/tillicum/)
- [Apptainer User Guide](https://apptainer.org/docs/user/main/)
- [Containers tutorial for Hyak Klone](https://hyak.uw.edu/docs/hyak101/containers/syllabus)

### Containers Reading
   - [What are Containers? from Google Cloud](https://cloud.google.com/learn/what-are-containers)
   - [Understanding Containers from RedHat](https://www.redhat.com/en/topics/containers)

### Containers Videos
   - **HIGHLY RECOMMENDED** - [Apptainer: Deep Dive, Use Cases, and Examples from CiQ](https://www.youtube.com/watch?v=Hj5eTZGUsDM&list=PLcQDboeIE0XhKKczoGK-EvINuwAnm-jsI&index=3)
   - [you need to learn Docker RIGHT NOW!! // Docker Containers 101 from NetworkChuck](https://www.youtube.com/watch?v=eGz9DS-aIeY)
   - [Containerization Explained from IBM Technologies](https://www.youtube.com/watch?v=0qotVMX-J5s)
   - [Containers for Absolute Beginners from Tiny Technical Tutorials](https://www.youtube.com/watch?v=NI34uF7VVP8)


