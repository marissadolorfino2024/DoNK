#!/bin/bash

# this script takes as input (arg1) a directory containing pdb files of receptors to dock to and prepares the rec.pdb and xtal-lig.pdb files for docking. it creates a subdirectory in the docking directory (arg2) that includes the original pdb, rec.pdb, and xtal-lig.pdb 
# requirements: need directory with inputs names dock_inputs

## fill in SBATCH lines

#SBATCH --job-name=
#SBATCH --account=
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=20GB
#SBATCH --time=48:00:00
#SBATCH --error=
#SBATCH --output=

shopt -s nullglob

# check for the existence of the necessary directories
input_dir=$1
docking_dir=$2

echo $input_dir
echo $docking_dir

if [ ! -d ${input_dir} ]; then
	echo "no directory named $input_dir containing pdbs"
	return
fi

if [ ! -d ${docking_dir} ]; then
	echo "no directory named $docking_dir for docking"
	return
fi

# loop to make rec and xtal-lig structures for all the input pdbs in dock_inputs

for file in $input_dir/*.pdb
	do
		file_name=${file##*/}
		
		pdb=$file_name

		pdb_id=${pdb::-4}

		dir_name="${pdb_id}_dock_$(date +%Y%m%d)"
		
		echo $dir_name

		mkdir "$docking_dir/$dir_name"

		cd "$docking_dir/$dir_name"
		
		pwd

		cp "../../$input_dir/"$pdb .
		
		# creating rec.pdb and xtal-lig.pdb for docking
		# assumes that all of the pdblines starting with ATOM are receptor atoms and that
		# all pdblines starting with HETATM are ligand atoms (like w output from diffdock)

		grep "^ATOM................." $pdb > rec.pdb 
		grep "^HETATM..........." $pdb > xtal-lig.pdb

		rec_atoms=$(wc -l < rec.pdb)
		lig_atoms=$(wc -l < xtal-lig.pdb)

		echo "atoms in "${pdb_id}"_rec.pdb: $(wc -l < rec.pdb)"
		echo "atoms in "${pdb_id}"_xtal-lig.pdb: $(wc -l < xtal-lig.pdb)"

		if ((rec_atoms == 0))
		then
			cd ../
			rm -r $dir_name
			mv ../$input_dir/$pdb ../$input_dir/rerun 
			cd ../

		else
			if ((lig_atoms == 0))
			then
				cd ../
				rm -r $dir_name
				mv ../$input_dir/$pdb ../$input_dir/rerun
				cd ../
			else
				cd ../../
			fi
		fi
		
	done
