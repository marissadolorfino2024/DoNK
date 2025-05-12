#!/bin/bash

## fill in SBATCH 
  
#SBATCH --job-name=
#SBATCH --account=
#SBATCH --partition=standard
#SBATCH --cpus-per-task=5
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=20GB
#SBATCH --time=
#SBATCH --output=
#SBATCH --error=
#SBATCH --array=

# script to design binding pockets of protein receptors. pdb files are specified in tasks.txt and residues to design are specified in mpnn_contigs.txt
# designs specifically hydrophobic pockets

# activate conda env prior to running: source activate mlfold

source activate mlfold

pdb=$(cat tasks.txt | sed -n "$SLURM_ARRAY_TASK_ID p")
seq_contig=$(cat mpnn_contigs.txt | sed -n "$SLURM_ARRAY_TASK_ID p")
echo $seq_contig

name="${pdb#*noised_receptors/}"
if [ ! -d ${name::-4}_input ]
then
	mkdir ${name::-4}_input
	cp $pdb ${name::-4}_input
fi

output_dir=${name::-4}_hydro_results
if [ ! -d $output_dir ]
then
	mkdir -p $output_dir
fi

folder_with_pdbs=${name::-4}_input

path_for_parsed_chains=$output_dir"/parsed_pdbs.jsonl"
design_only_positions="$seq_contig"
path_for_fixed_positions=$output_dir"/fixed_pos.jsonl"
chains_to_design="A"

python /home/mdolo/turbo/mdolo/opt/ProteinMPNN/helper_scripts/parse_multiple_chains.py --input_path=$folder_with_pdbs --output_path=$path_for_parsed_chains

python /home/mdolo/turbo/mdolo/opt/ProteinMPNN/helper_scripts/make_fixed_positions_dict.py --input_path=$path_for_parsed_chains --output_path=$path_for_fixed_positions --chain_list "$chains_to_design" --position_list "$design_only_positions" --specify_non_fixed

python /home/mdolo/turbo/mdolo/opt/ProteinMPNN/protein_mpnn_run.py \
	--jsonl_path $path_for_parsed_chains \
	--out_folder $output_dir \
	--fixed_positions_jsonl $path_for_fixed_positions \
	--num_seq_per_target 5 \
	--omit_AAs "RHKDESTNQC" \
	--sampling_temp "0.3" \
	--seed 37 \
	--batch_size 1

