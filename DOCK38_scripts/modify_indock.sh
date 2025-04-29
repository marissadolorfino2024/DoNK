#!/bin/bash
#SBATCH --job-name=mod_indock
#SBATCH --account=maom0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=24:00:00
#SBATCH --error=mod_indock.err
#SBATCH --output=mod_indock.out

# script to change all indock files in batch 

# fill in to edit INDOCK files
bump_max=100
bump_rigid=100
score_max=100
atom_max=100

for dir in dockdir*/*dock_2025*/*prepared_struct/dockfiles
do 
	cd $dir

	sed -i "s/bump_maximum                  10.0/bump_maximum                  $bump_max/" INDOCK

	sed -i "s/bump_rigid                    10.0/bump_rigid                    $bump_rigid/" INDOCK

	sed -i "s/mol2_score_maximum            -10.0/mol2_score_maximum            $score_max/" INDOCK

	sed -i "s/atom_maximum                  25/atom_maximum                  $atom_max/" INDOCK

	cd ../../../../
done
