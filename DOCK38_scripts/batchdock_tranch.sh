#!/bin/bash
#SBATCH --job-name=batch_dock
#SBATCH --account=maom0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=10:00:00
#SBATCH --error=dock_10ang.err
#SBATCH --output=dock_10ang.out

# change to bash script not slurm script, change db2 batchsize in dock_submit.sh based on n_recs and n_batches, n_recs * n_batches must be less than 4900.
# to prepare many pdbs at once, create tasks.txt file where each line is a directory where diffdock predictions and the rec pdb live

# batch docking of database to set of receptors
for i in $(seq 1 4999)
do
	dir=$(cat tasks.txt | sed -n "$i p")
	script="dock_struct_${i}.sh"

	cat <<EOF  > $script
#!/bin/bash
#SBATCH --job-name=dock_${i}
#SBATCH --account=maom0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=5:00:00
#SBATCH --error=dock_${i}.err
#SBATCH --output=dock_${i}.out

# usage: run ucsf dock to dock instock ligands (or specified database) to a set of prepared receptors specified in tasks.txt

cd $dir

prepare_dir=${dir}_prepared_struct

#echo "structure folder: \$prepare_dir"

# structure folder with INDOCK file
PREPARED_STRUCTURE="\$PWD/\$prepare_dir"

# directory where database.sdi is located
DATABASE=/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/databases/ZINC_instock

database_name=ZINC_instock

dock_dir="${dir},,_\${database_name}"

#echo "docking dir: \$dock_dir"

mkdir \${dock_dir}

cd \${dock_dir}

source ${DOCK_TEMPLATE}/scripts/dock_clean.sh

#echo "Running dock ..."
bash /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/dock_submit.sh \
\${DATABASE}/database.sdi \
\${PREPARED_STRUCTURE}/dockfiles \
results

cd ../../
EOF

	sbatch $script
	rm $script
done
