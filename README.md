# DoNK Scripts: this repository contains scripts for protein generation, docking, and analysis relating to the generation, analysis, and use of DoNK data.

The directory corresponding to this repo on greatlakes is: `/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/DoNK_scripts`.

The DoNK_v1 data can be found on greatlakes here: `/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1`.

## Protein Design workflow: 

Steps for DoNK protein design: 
  - RFDiffusion for protein backbone diversity:
  - ProteinMPNN for sequence design
  - AlphaFold2 for sequence --> structure
  - Sphere generation via DiffDock

## Docking via DOCK3.8 workflow:

A general DOCK38 tutorial can be found here: [DOCK38 tutorial](https://docs.google.com/document/d/1ZIgTsOP2wmaPRvEQ0r4Q2FTC_R4RNvx7j5CiS3m8rXQ/edit?usp=sharing).
Steps for DoNK docking:
  - Make the structures (generate rec.pdb and xtal-lig.pdb)
  - Prepare the structures via blastermaster
  - Modify docking parameters via the INDOCK file
  - Dock a dataset of small molecule ligands to each receptor
  - Analyze docking data

## ML on bioactivity fingerprints workflow:

Steps for DoNK fingerprint generation and ML:
  - Generate ECFP4 chemical fingerprints for ligands
  - Generate receptor by ligand bioactivity matrix
  - Obtain ligand and receptor bioactivity fingerprints from the bioactivity matrix
  - Perform analysis on fingerprints
    - Dimensionality reduction of fingerprints
    - Clustering of embedding space
  - Train models (graph encoder-decoders) to transform graph representations of small molecules into bioactivity fingerprints
  - Use latent space of trained models to predict molecular properties, bioactivity, etc
