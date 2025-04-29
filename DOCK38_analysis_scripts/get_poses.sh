#!/bin/sh

## fill in sbatch
## this script calls the getposes_blazing_faster_py3.py DOCK38 script, which extracts docked poses from the DOCK outputs

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

# tasks.txt should contain a list of directories (one on each line), each of which contains the extract_all.sort.txt files (obtained from extract_all.sh script)
# the output will be a poses.mol2 file, which contains the poses of the docked ligands. This file can be viewed in pymol or chimera

dir=$(cat tasks.txt | sed -n "$SLURM_ARRAY_TASK_ID p")

cd $dir

python /home/mdolo/turbo/MPProjects/chemical_space/dock_dev/docking_runs/getposes_blazing_faster_py3.py ./ extract_all.sort.txt 2000000 poses.mol2 test.mol2.gz.0 # 2000000 arg should be larger than the number of ligands docked so as to obtain poses from all ligands 
