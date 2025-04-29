#!/bin/sh

## this script calls get_designed_fastas.py on the fa files specified in tasks.txt
## fill in SBATCH scripts

#SBATCH --job-name=
#SBATCH --account=
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
##SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=20GB
#SBATCH --time=70:00:00
#SBATCH --output=array_%A-%a.out
#SBATCH --error=array_%A-%a.err
#SBATCH --array=             

# the tasks.txt file should contain a list of fa files generated from ProteinMPNN (one fa file per line) to be separated into single design fastas (one sequence per fasta)
file=$(cat tasks.txt | sed -n "$SLURM_ARRAY_TASK_ID p")

python get_designed_fastas.py $file 

