#!/bin/sh

# script to submit a batch of alphafold2 jobs (via colabfold). using default configs for alphafold2 unless otherwise stated. 3 recycles performed
## fill in SBATCH

#SBATCH --job-name=
#SBATCH --account=
#SBATCH --partition=spgpu,gpu
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=20GB
#SBATCH --time=
#SBATCH --output=array_%A-%a.out
#SBATCH --error=array_%A-%a.err
#SBATCH --array=             

# tasks.txt should list paths to fasta files (one on each line) containing the designed protein sequences (from proteinMPNN) to be folded via AlphaFold2

file=$(cat tasks.txt | sed -n "$SLURM_ARRAY_TASK_ID p")

/nfs/turbo/umms-maom/mdolo/opt/ColabFold/localcolabfold/colabfold-conda/bin/colabfold_batch --num-recycle 3 $file ${file::-6}_folds
