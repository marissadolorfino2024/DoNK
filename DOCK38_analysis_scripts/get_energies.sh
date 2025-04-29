#!/bin/bash

## fill in sbatch
## this script extracts the total docking energies from poses.mol2 files  

#SBATCH --job-name=
#SBATCH --account=
#SBATCH --partition=
#SBATCH --cpus-per-task=
#SBATCH --nodes=
#SBATCH --ntasks-per-node=
#SBATCH --mem-per-cpu=
#SBATCH --time=
#SBATCH --mail-type=BEGIN,END
#SBATCH --error=
#SBATCH --out=
#SBATCH --mail-user=
#SBATCH --array= ## range (1-n) where n is the number of array jobs you have (# of lines in task.txt)

# tasks.txt should contain a list of directories (one on each line) which contain the poses.mol2 files obtained from the DOCK38 analysis scripts
dir=$(cat tasks.txt | sed -n "$SLURM_ARRAY_TASK_ID p")

cd $dir

python /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/DoNK_scripts/get_total_E.py poses.mol2 $dir
