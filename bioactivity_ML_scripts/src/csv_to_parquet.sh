#!/bin/bash
#SBATCH --job-name=csv_to_parquet
#SBATCH --account=tromeara0
#SBATCH --partition=largemem
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=250GB
#SBATCH --time=24:00:00
#SBATCH --output=csv_to_parquet.out
#SBATCH --error=csv_to_parquet.err

time python csv_to_parquet.py

