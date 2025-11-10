# Hands-on Exercise: Pytorch Container Customization 

This hands-on exercise allows you to practice using the common Apptainer commands to customize a container pulled from the [NVIDIA NGC](https://catalog.ngc.nvidia.com/containers?filters=&orderBy=weightPopularDESC&query=&page=&pageSize=) and run an image classification inference using one of Tillicum's common datasets, [ImageNet](https://hyak.uw.edu/docs/data-commons/imagenet). Additionally, you will submit the inference as a job to be executed without supervision to Tillicum's Job Scheduler, Slurm. 

> 🎯 **GOAL:** Learn how to customize a GPU-enabled PyTorch container, run image classification on a shared dataset, monitor GPU activity, and submit the workflow as a batch job using Slurm on Tillicum.

### Overview
* [0. Preparation](#0-preparation)
* [1. Start an Interactive Job](#1-start-an-interactive-job)
* [2. Prepare the Dataset](#2-prepare-the-dataset)
* [3. Prepare the Container](#3-prepare-the-container)
* [4. Image Classification](#4-image-classification)
* [5. Batch inference - submit the job with Slurm](#5-batch-inference---submit-the-job-with-slurm)
* [6. Challenge: Convert the Inference Workflow into a Slurm Array Job](#6-challenge-convert-the-inference-workflow-into-a-slurm-array-job)

## 0. Preparation

If you haven't already, follow the instructions in [00-preparation](./00-preparation.md) to log in to Tillicum and set up your working directory for the following exercise.

## 1. Start an Interactive Job

> ⚠️ **WARNING: All compute work must be done on compute nodes.**

Request an interactive session with 1 GPU for 1 hour:

```bash
salloc --account=traincontainer2025 --qos=interactive --gpus=1 --time=01:00:00
```
> ⚠️ **WARNING**: If you are completing this workshop independently and asynchronousl from the November 2025 workshop, you will not be able to use the account `traincontainer2025`. Remove this Slurm directive and Slurm will use your default account.
```bash
salloc --qos=interactive --gpus=1 --time=01:00:00
```

Once resources are allocated, confirm you’re on a compute node:

```bash
hostname
```

Then verify your GPU is visible:

```bash
nvidia-smi
# output should resemble a table with driver, CUDA, and hardware details
```

You should see GPU details (e.g., NVIDIA H200 with driver and CUDA versions)

## 2. Prepare the Dataset

Tillicum has cluster-wide, shared dataset storage referred to as Data Commons under `/gpfs/datasets/`.

The purpose of the Data Commons is to provide a central location for datasets being used by multiple groups, to avoid hosting the same dataset multiple times in separate group directories. The Tillicum support team is taking requires to host additional datasets. [Please review the requirements](https://hyak.uw.edu/docs/data-commons/requirements) to nominate datasets for hosting if that is of interest fo your research group. 

We'll use images from the [ImageNet](https://hyak.uw.edu/docs/data-commons/imagenet) dataset for this exercise. 

> 📝 Note: Pytorch has specific functions to use ImageNet for various tasks, but we won't be reviewing those today. You can read [instructions on the ImageNet function within PyTorch here](https://pytorch.org/vision/stable/generated/torchvision.datasets.ImageNet.html). 

Make a directory for a subset of images from the ImageNet dataset. 
```bash
mkdir sample-images
```
For now, we'll select 5 images at random can copy them from `/gpfs/datasets/imagenet/ILSVRC/Data/CLS-LOC/val/` or the set of validated images.
```bash
cd sample-images
find /gpfs/datasets/imagenet/ILSVRC/Data/CLS-LOC/val/ -name "*.JPEG" | shuf -n 5 | xargs -I {} cp {} .
cd ../
```
Next we'll download the standard ImageNet labels list. Our model will predict the index of the image label (a number) which is not as helpful as the label describing the image. 

```bash
wget https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt
head imagenet_classes.txt
```

## 3. Prepare the Container

We'll use the latest [Pytorch container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch?version=25.10-py3)from the [NVIDIA NGC](https://catalog.ngc.nvidia.com/containers?filters=&orderBy=weightPopularDESC&query=&page=&pageSize=) to use as our baseline environment. 

To save some time, we have pulled the Pytorch container version 25.10-py3 and stored it on Tillicum. Copy it into your working directory: 
```bash
cp /gpfs/containers/nvidia/pytorch_25.10-py3.sif .
```

If you want to try pulling it yourself instead of copying it, run (takes 7-8 minutes to complete): 
```bash
time apptainer pull docker://nvcr.io/nvidia/pytorch:25.10-py3
```
This container is preloaded with a lot of what we need for GPU acceleration (e.g., CUDA) and image inference (e.g., torchvision), but to practice customizing containers, we will install [`timm`](https://timm.fast.ai/) a deep-learning library that is: 
* widely used by deep learning users
* maintained by NVIDIA and the broader PyTorch community
* allows users to test dozens of Imagenet-trained architectures with one line
* relevant to real GPU workflows on Tillicum

We'll install `timm` into the Pytorch container with a definition file and building from `pytorch_25.10-py3.sif` defined as our local image. 

```bash
cat pytorch_timm.def
```
The definition file installs `timm` into the container with `pip install`, adds labels, and a runscript. 

Build the custom Pytorch container + `timm` with (takes 4-5 minutes to complete):
```bash
time apptainer build pytorch_timm_25.10.sif pytorch_timm.def
```

Confirm `timm` is available. 
```bash 
apptainer exec pytorch_timm_25.10.sif python -c "import timm; print('timm version:', timm.__version__)"
```

## 4. Image Classification

Let's use our container to classify the 5 images we selected by random draw. For this, we have prepared `infer_timm.py`. 

```bash 
cat infer_timm.py
```

> 📝 **About this script:** 
> 
> The script runs a few extra operations as well because Tillicum is a GPU system: 
> * takes a directory of images as input
> * imports python modules including `timm`, `torch`, and image utilities
> * loads the [ResNet-50](https://docs.pytorch.org/vision/main/models/generated/torchvision.models.resnet50.html) pretrained image classification model
> * loads the standard ImageNet labels list (`imagenet_classes.txt`)
> * classifies each image and writes the filename + predicted label to an output file
> * reports which GPUs are visible and which GPU the model is using
> * prints GPU memory usage after each image is processed

Inference command: 
```bash
apptainer exec --nv pytorch_timm_25.10.sif python infer_timm.py sample-images/ output_labels.txt
```
The `--nv` flag tells Apptainer to enable NVIDIA GPU support inside the container, allowing CUDA and GPU-accelerated libraries to run.

> ⚠️ **Ignore this warning** - you may see an error `Read-only file system`. When you use `--nv`, Apptainer bind-mounts NVIDIA driver libraries into the container. As part of that process, the runtime tries to clean up old symlinks in `/usr/local/cuda/compat/lib` but since your `.sif` is read-only, it cannot remove anything there so `rm` prints that warning. Just ignore it. It does not affect inference or performance.

Check out the results:
```bash
cat output_labels.txt
```
Output should resemble: 
```bash
ILSVRC2012_val_00040920.JPEG, gas pump
ILSVRC2012_val_00038837.JPEG, rain barrel
ILSVRC2012_val_00019209.JPEG, Rhodesian ridgeback
ILSVRC2012_val_00040044.JPEG, rhinoceros beetle
ILSVRC2012_val_00017487.JPEG, rain barrel
```

> **OPTIONAL SIDE QUEST: Check Images with Globus** 
> 
> [Check out these instructions](https://github.com/UWrc/tillicum-onboarding/blob/main/04-file-transfer.md#getting-started)to: 
> * go to [globus.org](https://www.globus.org/) and log in
> * find "Uw Hyak Tillicum"
> * use the graphical interface to navigate to your working directory and the sample-images directory at `/gpfs/scrubbed/$USER/tillicum-containers/sample-images`
> * select one of the images
> * download the image with the download icon in the right tool bar
> * compare the image to its inferred label
> 
> Was the image classification correct? 


## 5. Batch inference - submit the job with Slurm

If you haven't used Slurm on Tillicum before, please consider completing our [Slurm tutorial](https://github.com/UWrc/tillicum-slurm/blob/2856a9bcc3eeda15ce1549d0e932f8f5bf335f9c/05-task.md?plain=1) for additional practice. 

Since it is pretty quick, let's classify more images, but instead of waiting, let's use Slurm to schedule the job for execution. Slurm is ideal for jobs that take longer to complete. You can schedule the job as a batch and rather than dedicating your computer to running tasks interactively, avoiding disruptions due to a faulting internet connection. 

This time, let's copy 200 images at random to our `sample-images` directory for classification. 

```bash
cd sample-images
find /gpfs/datasets/imagenet/ILSVRC/Data/CLS-LOC/val/ -name "*.JPEG" | shuf -n 200 | xargs -I {} cp {} .
ls
cd ../
```
We've prepared `run_inference.slurm` for your to submit with `sbatch` to classify these images. 
```bash
cat run_inference.slurm
```

> ⚠️ **WARNING**: If you are completing this workshop independently and asynchronousl from the November 2025 workshop, you will not be able to use the account `traincontainer2025`. Edit `run_inference.slurm` to remove this `#SBATCH --account=traincontainer2025` and Slurm will use your default account.

> 📝 **About this script:** 
> 
> This Slurm script: 
> * requests 1 GPU and sets a 10-minute time limit
> * loads the container image (pytorch_timm_25.10.sif)
> * sets the input image directory and output file paths
> * runs the inference script inside the container with GPU access (--nv)
> * writes job output and logs to infer_<jobid>.out

Submit the Slurm script with: 
```bash
sbatch run_inference.slurm
```

While the task of classifying 200 images is still wicked fast, you can monitor any job in real time with: 
```bash
watch squeue -u $USER
# Ctrl + C to quit the watch command
```

View the results: 
```bash
more output_labels.txt
```

View the output messages: 
```bash
more infer_<jobID>.out
# replace <jobID> above with the jobID assigned to your job
```

## 6. Challenge: Convert the Inference Workflow into a Slurm Array Job

So far, we have run image classification on a single directory of images using a standard Slurm job. This works well when we only have one dataset to process. However, in real research workflows, we often need to run the same analysis many times over different input sets. Slurm **array jobs** provide a scalable way to launch multiple, independent tasks in parallel with a single submission.

Your challenge is to:
* Prepare three small image “batches” (e.g., sample-images-1/, sample-images-2/, sample-images-3/).
* Convert the inference job into a Slurm array job so that each array task processes one directory.
    * *Hint: Use the [Slurm variable](https://slurm.schedmd.com/sbatch.html#SECTION_OUTPUT-ENVIRONMENT-VARIABLES) `SLURM_ARRAY_TASK_ID` so each task processes a different input directory and writes its own output.
* Ensure that each task writes its output to a distinct results file.

[**This skills page may be helpful.**](https://github.com/UWrc/tillicum-slurm/blob/2856a9bcc3eeda15ce1549d0e932f8f5bf335f9c/04-job-arrays.md)

Try to complete this with minimal guidance. Afterward, compare your solution to 




