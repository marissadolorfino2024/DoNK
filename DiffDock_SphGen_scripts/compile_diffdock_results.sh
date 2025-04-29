#!/bin/bash

## script to 
## fill in sbatch lines

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

diffdock_dir="" ## fill in directory that contains all of the diffdock results (full path)

time {
cd $diffdock_dir
for dir in *
do
	cd $dir || continue
	for dir2 in *
	do
		cd $dir2 || continue
		cd complex_0 || continue
		subs="${dir2#*seed_000_}"
		probe="${subs%_preds}"
		
		rm rank1.sdf
		if compgen -G "rank*" > /dev/null; then
			for file in rank*
			do
				mv $file ${probe}_${file}
			done
		fi
		cd ../../
	done
	
	mv */complex_0/*.sdf .
	
	rmdir */complex_0
	rmdir *_preds

	cd $diffdock_dir
done
}

