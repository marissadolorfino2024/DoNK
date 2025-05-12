# Docking to Novel Pockets (DoNK)

<img width="870" alt="image" src="https://github.com/user-attachments/assets/f89eae18-6f2f-4aef-bdd7-713373aed5bb" />


This repository contains scripts for protein generation, docking, and analysis relating to the generation, analysis, and use of DoNK data.

## Overview
Large-scale synthetic datasets can be used as a source of evidence to complement complex experimental data to train foundation models. The Docking to Novel pocKets project aims to develop representations of small molecules based on their in-silico activity profiles across binding sites in designed receptors. These representations can be used to efficiently develop structure-activity relationships, navigate ultra-large scale make-on-demand chemical spaces, and facilitate training large-scale chemical foundation models. The development of DoNK involves three stages 1) Simulate diverse, native-like binding sites using state-of-the-art protein structure generation, 2) use physics based docking to simulate the binding mode and binding affinity of small molecules into the generated binding sites, and 3) use deep-learning based variational transcoder models to predict docking-based activity profiles across designed receptors with a meaningful latent space. To use the DoNK model, the trained encoder can be used to embed small molecules into a latent space where similar embeddings represent similar predicted docking-based bioactivity profiles, or the DoNK dataset can be used directly as a foundation model training task.

## Protein Design workflow: 

Steps for DoNK protein design: 
  - clone the RFDiffusion git repo and follow steps to set up conda env 
  - RFDiffusion for protein backbone diversity: `RFDiffusion_scripts/`
    - to prepare PDB files for RFDiffusion, run the `reformat_pdbs.py` for each PDB file
    - for each reformatted PDB file, run the `pdb2fasta.py` script to generate a fasta file corresponding to each PDB file
    - run the `sequence_contigs.py` script to prepare RFDiffusion contigs
    - run the `partialdiffusion.sh` script to submit a SLURM array job that runs RFDiffusion partial diffusion on each PDB file
  - clone the ProteinMPNN git repo and follow steps to set up conda env
  - ProteinMPNN for sequence design: `MPNN_sequence_design_scripts`
    - run the `sequence_design_contigs.py` script to generate contigs that determine which residues in a PDB file are designable. The radius around the binding pocket that defines designable residues is specified as an argument to the script
    - `hydro_pocket_design.sh` and `polar_pocket_design.sh` run sequence designing allowing only hydrophobic or polar residues. Either of these scripts can be modified for more relaxed or stringent design by changing what amino acids are omitted from design (via the flag `--omit_AAs`)
  - clone the colabfold git repository and follow steps to set up conda env
  - AlphaFold2 for sequence --> structure: `AlphaFold2_scripts`
    - run the `sep_fastas.sh` script, which calls `get_designed_fastas.py`, to separate outputs from ProteinMPNN into individual fasta files
    - run the `batch_colab.sh` script to submit a SLURM array job to fold the sequences
    - the `relax_AF_folds.sh` script can be run to relax structures via Rosetta (this step was not done for donk_v1)
  - Sphere generation via DiffDock: `DiffDock_SphGen_scripts`
    - run the `submit_dockruns.sh` script to run DiffDock on each protein, with 8 probes
    - run the `compile_diffdock_results.sh` script
    - run `sphgen_10ang.sh` or `sphgen_5ang.sh`, which call `diffdock_sphgen.py`
    - make the spheres via `batch_make_struct.sh`

## Docking via DOCK3.8 workflow:

A general DOCK38 tutorial can be found here: [DOCK38 tutorial](https://docs.google.com/document/d/1ZIgTsOP2wmaPRvEQ0r4Q2FTC_R4RNvx7j5CiS3m8rXQ/edit?usp=sharing).
Steps for DoNK docking:
  - Setup the docking environment by editing and running the following script: `DOCK38_scripts/setup_dock_environment.sh`
  - Make the structures (generate rec.pdb and xtal-lig.pdb): `DOCK38_scripts/batch_make_struct.sh`. This step should be done above if using DiffDock for sphere generation
  - Prepare the structures via blastermaster: `DOCK38_scripts/batch_prepare_structure.sh`
  - Modify docking parameters via the INDOCK file: `DOCK38_scripts/modify_indock.sh`
  - Dock a dataset of small molecule ligands to each receptor: `DOCK38_scripts/batchdock_tranch.sh`
  - Analyze docking data: `DOCK38_analysis_scripts`

## ML on bioactivity fingerprints workflow:

Steps for DoNK fingerprint generation and ML:
  - Generate ECFP4 chemical fingerprints for ligands: `bioactivity_ML_scripts/ECFP4.py`
  - Generate receptor by ligand bioactivity matrix: `mjo_build_analyze_bindmatrix`
  - Obtain ligand and receptor bioactivity fingerprints from the bioactivity matrix: `mjo_build_analyze_bindmatrix`
  - Perform analysis on fingerprints
    - Dimensionality reduction of fingerprints
    - Clustering of embedding space
  - Train models (graph encoder-decoders) to transform graph representations of small molecules into bioactivity fingerprints: `bioactivity_ML_scripts/ml_utils.py` and `bioactivity_ML_scripts/data_serial_train.py`
  - Use latent space of trained models to predict molecular properties, bioactivity, etc

## Data Availability:
The directory corresponding to this repo on greatlakes is: `/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/DoNK`.

The DoNK_v1 data can be found on greatlakes here: `/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1` and will be released open source soon.


