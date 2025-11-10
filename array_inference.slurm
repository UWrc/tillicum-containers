#!/bin/bash
#SBATCH --job-name=imagenet-test
#SBATCH --account=traincontainer2025 # change account
#SBATCH --qos=normal
#SBATCH --gpus=1
#SBATCH --time=00:10:00
#SBATCH -o infer_%j.out
#SBATCH --array=1-3   # or however many directories there are

IMAGE=pytorch_timm_25.10.sif
INPUT=sample-images-${SLURM_ARRAY_TASK_ID}/
OUT=output_labels_${SLURM_ARRAY_TASK_ID}.txt

time apptainer exec --nv $IMAGE python infer_timm.py $INPUT $OUT