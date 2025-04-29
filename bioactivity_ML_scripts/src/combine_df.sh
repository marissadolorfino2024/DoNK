#!/bin/bash
#SBATCH --job-name=combine_sample
#SBATCH --account=tromeara0
#SBATCH --partition=largemem
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=250GB
#SBATCH --time=24:00:00
#SBATCH --output=combine_sample.out
#SBATCH --error=combine_sample.err

time python combine_df_sample.py /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/pymol_dock_binding_analysis_originalset/product/donkv1_binds_wide_rm_allzero_ligands.parquet zinc_ids_smiles.parquet

