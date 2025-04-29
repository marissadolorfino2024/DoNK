#!/bin/bash
#SBATCH --job-name=sphgen5
#SBATCH --account=maom0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=20GB
#SBATCH --time=24:00:00
#SBATCH --output=sphgen5.out
#SBATCH --error=sphgen5.err

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
	
	# directory of alphafold structures
	af_dir=/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/AF_fold_designs/10angstrom_0.3temp_AF_rank1_files
	
	pdb_name="${dir%%_results*}"

	af_pdb=${af_dir}/${pdb_name}.pdb

	# copy alphafold file from af structure folders
	cp $af_pdb .
	
	# 5 angstrom radius around ref lig, 7 clusters --> 7 diffdock probes within ~5 angstrom radius	
	python /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/diffdockalign_designs_andDock_originalset/diffdock_sphgen.py $af_pdb 7 7

	cd ../
done
mkdir pdbs_ready_forDOCK_5ang
cp *_results/*dd_sphgen.pdb pdbs_ready_forDOCK_5ang
}
