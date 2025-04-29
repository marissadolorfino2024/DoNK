#!/bin/bash

## fill in sbatch
## this script calls the get_hits.py script, which uses lowest 1% total docking energies to choose hits (1) from ligands docked. The nonhits are 0
 
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
 
# tasks.txt should contain a list of directories (one on each line) which contains the *_totalE.txt file 
# the output will be $dir_hits.txt

dir=$(cat tasks.txt | sed -n "$SLURM_ARRAY_TASK_ID p")

arg1=$dir'_totalE.txt'
arg2=$dir'_hits.txt'

cd $dir

python /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/DoNK_scripts/get_hits.py $arg1 $arg2

