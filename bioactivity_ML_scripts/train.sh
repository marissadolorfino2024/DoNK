#!/bin/bash
#SBATCH --job-name=train
#SBATCH --account=tsztain_owned1
#SBATCH --partition=spgpu2
#SBATCH --gres=gpu:8
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=60
#SBATCH --mem=256GB
#SBATCH --time=24:00:00
#SBATCH --error=train.err
#SBATCH --output=train.out

time python data_serial_train.py

