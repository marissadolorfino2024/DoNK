#!/bin/bash

## fill in SBATCH

#SBATCH --job-name=
#SBATCH --account=
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=20GB
#SBATCH --time=24:00:00
#SBATCH --output=
#SBATCH --error=

time{
for dir in *_results
do	
	cd $dir

	# convert sdf prdiction files to pdb
	for file in *.sdf
	do
		obabel $file -O ${file::-3}pdb
	done

	mkdir sdf_dir
	mv *.sdf sdf_dir
	
	# directory of rank1 alphafold structures
	af_dir=
	
	pdb_name="${dir%%_results*}"

	af_pdb=${af_dir}/${pdb_name}.pdb

	# copy alphafold file from af structure folders
	cp $af_pdb .
	
	# 5 angstrom radius around ref lig, 7 clusters --> 7 diffdock probes within ~5 angstrom radius	
	python diffdock_sphgen.py $af_pdb 7 7

	cd ../
done
mkdir pdbs_ready_forDOCK_5ang
cp *_results/*dd_sphgen.pdb pdbs_ready_forDOCK_5ang
}
