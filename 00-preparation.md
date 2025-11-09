# Preparation

Before beginning the tutorial, let’s log in to Tillicum and set up a working directory where you’ll clone the training repository and store outputs for this tutorial.

## Log in to `tillicum`

Connect to Tillicum via SSH from your terminal/Windows Powershell:

```bash
# Replace "UWNetID" with your actual UW NetID.
ssh UWNetid@tillicum.hyak.uw.edu
```

If successful, you should see a prompt like:

```bash
[UWNetID@tillicum-login01 ~]$
```

## Create Your Working Directory

All tutorial exercises will be done in your own working directory.
We recommend starting your working directory in a filesystem location where you have a large storage quota, rather than starting in your Home directory (limited to 10 GB; [Click here to learn more about storage limits on Tillicum](https://hyak.uw.edu/docs/tillicum/storage#user-storage)). 

For this tutorial, we will use Tillicum's free community storage under `/gpfs/scrubbed` for the working directory.

**1. Navigate to `/gpfs/scrubbed`**

```bash
cd /gpfs/scrubbed/
```

**2. Create and enter your own directory under `/gpfs/scrubbed`**

```bash
mkdir $USER
cd $USER
```

> 📝 **NOTE:** The `$USER` variable automatically expands to your username.

**3. Clone the training repository**

Clone the Tillicum Slurm training materials into your working directory:

```bash
git clone https://github.com/UWrc/tillicum-containers.git
```

Once cloned, you’ll have a directory named `tillicum-containers` containing all tutorial scripts and examples.

Navigate into it to get started:

```bash
cd tillicum-containers
```

List the contents in the directory:

```bash
ls
```