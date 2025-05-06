# Docking to Novel Pockets (DoNK)

<img width="870" alt="image" src="https://github.com/user-attachments/assets/f89eae18-6f2f-4aef-bdd7-713373aed5bb" />


This repository contains scripts for protein generation, docking, and analysis relating to the generation, analysis, and use of DoNK data.

## Overview
Large-scale synthetic datasets can be used as a source of evidence to complement complex experimental data to train foundation models. The Docking to Novel pocKets project aims to develop representations of small molecules based on their in-silico activity profiles across binding sites in designed receptors. These representations can be used to efficiently develop structure-activity relationships, navigate ultra-large scale make-on-demand chemical spaces, and facilitate training large-scale chemical foundation models. The development of DoNK involves three stages 1) Simulate diverse, native-like binding sites using state-of-the-art protein structure generation, 2) use physics based docking to simulate the binding mode and binding affinity of small molecules into the generated binding sites, and 3) use deep-learning based variational transcoder models to predict docking-based activity profiles across designed receptors with a meaningful latent space. To use the DoNK model, the trained encoder can be used to embed small molecules into a latent space where similar embeddings represent similar predicted docking-based bioactivity profiles, or the DoNK dataset can be used directly as a foundation model training task.

## Protein Design workflow: 

Steps for DoNK protein design: 
  - RFDiffusion for protein backbone diversity: `RFDiffusion_scripts/`
  - ProteinMPNN for sequence design: `MPNN_sequence_design_scripts`
  - AlphaFold2 for sequence --> structure: `AlphaFold2_scripts`
  - Sphere generation via DiffDock: `DiffDock_SphGen_scripts`

## Docking via DOCK3.8 workflow:

A general DOCK38 tutorial can be found here: [DOCK38 tutorial](https://docs.google.com/document/d/1ZIgTsOP2wmaPRvEQ0r4Q2FTC_R4RNvx7j5CiS3m8rXQ/edit?usp=sharing).
Steps for DoNK docking:
  - Setup the docking environment by editing and running the following script: `DOCK38_scripts/setup_dock_environment.sh`
  - Make the structures (generate rec.pdb and xtal-lig.pdb): `DOCK38_scripts/batch_make_struct.sh`
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
The directory corresponding to this repo on greatlakes is: `/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/DoNK_scripts`.

The DoNK_v1 data can be found on greatlakes here: `/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1` and will be released open source soon.


