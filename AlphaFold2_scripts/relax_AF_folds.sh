#!/bin/sh

# this script performs Rosetta relaxation of PDBs 
# fill in SBATCH lines

#SBATCH --job-name=
#SBATCH --account=
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --nodes=14
#SBATCH --ntasks-per-node=14
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=70:00:00
#SBATCH --error=
#SBATCH --output=
#SBATCH --array=

# the tasks.txt file should contain pdbs (one on each line) to be relaxed
file=$(cat tasks.txt | sed -n "$SLURM_ARRAY_TASK_ID p")

# the Bioinformatics and Rosetta modules from greatlakes will need to be loaded prior to running this script via module load 'module_name'

$ROSETTA3/bin/relax.linuxgccrelease -ignore_unrecognized_res -ignore_zero_occupancy false -use_input_sc -flip_HNQ -no_optH false -relax:constrain_relax_to_start_coords -relax:coord_constrain_sidechains -relax:ramp_constraints false -s $file

