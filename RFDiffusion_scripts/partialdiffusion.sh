#!/bin/bash

## script to partially diffuse input backbones 

## fill in SBATCH lines

#SBATCH --job-name=
#SBATCH --account=
#SBATCH --partition=spgpu,gpu
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=20GB
#SBATCH --time=70:00:00
#SBATCH --output=array_%A-%a.out
#SBATCH --error=array_%A-%a.err
#SBATCH --array=

# partial diffusion of scaffold structures to diversify backbone. The entire structure is allowed to change and 20 timesteps are used. 10 backbones will be generated per scaffold

# tasks.txt should contain a list of pdb files of backbones to be perturbed
pdb=$(cat test_tasks.txt | sed -n "$SLURM_ARRAY_TASK_ID p")
# seq_contigs.txt should contain a list of contigs. each line should correspond to the pdb file in tasks.txt
seq_contig=$(cat seq_contigs.txt | sed -n "$SLURM_ARRAY_TASK_ID p")

name=${pdb::-4}
result_dir=${name::-4}_results/${name::-4}

/nfs/turbo/umms-maom/mdolo/opt/RFdiffusion/scripts/run_inference.py inference.output_prefix=$result_dir inference.input_pdb=$pdb "contigmap.contigs=[$seq_contig-$seq_contig]" inference.num_designs=10 diffuser.partial_T=20

