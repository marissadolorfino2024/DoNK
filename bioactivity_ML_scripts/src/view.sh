#!/bin/bash
#SBATCH --job-name=view
#SBATCH --account=tromeara0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=100GB
#SBATCH --time=1:00:00
#SBATCH --output=view.out
#SBATCH --error=view.err

time python view.py pymol_donk_sample4ML.parquet
