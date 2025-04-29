#!/bin/python

# this script generates spheres (chooses HETATMs) which will be used as spheres during DOCK38 pipeline
# clusters possible HETATM coordinates to generate diverse HETATMs for sphgen

import pymol.cmd as cmd
import sys
import glob
import numpy as np
import math
import sklearn
from sklearn import cluster
import math

# ensure somewhere that the number of clusters is <= the number of predictions in the specified radius
# function get the name of the ligand from the reference pdb file
def get_lig(file):
    with open(file, 'r') as pdbf:
        lines = pdbf.readlines()

    ligs = set()
    for line in lines:
        if line[0:6] == 'HETATM':
            lig = line[17:20]
            if lig in ['SEP', 'TPO', 'SCS', 'CAS']:
                continue
            else:
                ligs.add(lig)


    lig = list(ligs)[0]
    if lig[0] == ' ':
        lig = lig[1:]
    elif lig[2] == ' ':
        lig = lig[:2]
    else:
        lig = lig

    return str(lig)

af_pdb = sys.argv[1] 
accept_radius = sys.argv[2]
clusters = sys.argv[3]

base_name = af_pdb.split('rank1_files/')[1]

name = af_pdb.split('_formatted_')[0]
name = name.split('rank1_files/')[1]
name = name + '_formatted.pdb'
scaffold = '/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/scaffolds/prepped_formatted_scaffolds/' + name 

# get ligand name of scaffold (ref) ligand
ref_lig = get_lig(scaffold)

# load objects
cmd.load(af_pdb, object='af_struct')

#cmd.save('af22.pdb')

cmd.load(scaffold, object='scaffold')

# align scaffold (mobile) to alphafold structure (fixed) 
cmd.align('scaffold', 'af_struct')

# remove everything except the reference ligand
cmd.remove('af_struct')

selection_string = f'scaffold and (not resn {ref_lig})'

cmd.select('to_remove', selection_string)
cmd.remove('to_remove')

# save the reference ligands as a pdb file
cmd.save('ref_lig.pdb')

ref_atoms = []
with open('ref_lig.pdb', 'r') as reffile:
    ref_lines = reffile.readlines()

for line in ref_lines:
    if line[0:6] == 'HETATM':
        ref_atoms.append(np.array([float(line[32:38]), float(line[40:46]), float(line[48:54])]))

reflig_center = [float(np.mean([atom[0] for atom in ref_atoms])), float(np.mean([atom[1] for atom in ref_atoms])), float(np.mean([atom[2] for atom in ref_atoms]))]

# compute the rmsd and store dictionary
def accept_lig(lig, ref_center, radius):
    radius = float(radius)

    with open(lig, 'r') as ligfile:
        lig_lines = ligfile.readlines()

    lig_atoms = []
    for line in lig_lines: 
        if line[0:6] == 'HETATM':
            lig_atoms.append(np.array([float(line[32:38]), float(line[40:46]), float(line[48:54])]))

        else:
            continue

    lig_center = [float(np.mean([atom[0] for atom in lig_atoms])), float(np.mean([atom[1] for atom in lig_atoms])), float(np.mean([atom[2] for atom in lig_atoms]))]
    
    atom_dists = []
    for lig_atom in lig_atoms:
        sum_sq = 0
        for i in range(3):
            sum_sq += ((ref_center[i] - lig_atom[i])**2)

        atom_dists.append(math.sqrt(sum_sq))

    in_radius = 0
    for atom in atom_dists:
        in_radius += (atom <= radius)
    
    return (int(in_radius) == len(atom_dists)), lig_center

print(f'reference center: {reflig_center}')

valid_preds = [] # as determined by distance to center of reference molecule
valid_pred_coords = [] # contains coordinates of center of valid diffdock predictions
# filter ligands by distance to center of reference molecule
for lig_pred in glob.glob('*rank*'):
    accept, pred_center = accept_lig(lig_pred, reflig_center, accept_radius)
    if (accept == True) and (np.isnan(pred_center).any() == False):
        valid_preds.append(lig_pred)
        valid_pred_coords.append(pred_center)
    else:
        continue

print(f'valid prediction coordinates: {valid_pred_coords}')
print(f'number of valid coordinates: {len(valid_pred_coords)}')

if int(len(valid_pred_coords)) > int(clusters):
    # perform clustering
    clust = sklearn.cluster.AgglomerativeClustering(n_clusters=int(clusters))
    
    labels = list(clust.fit_predict(np.array(valid_pred_coords)))
    labels = [int(label) for label in labels]
    
    clust_dict = {}
    for i in range(len(labels)):
        cluster = labels[i]
        if cluster in list(clust_dict.keys()):
            clust_dict[cluster].append(valid_preds[i])
        else:
            clust_dict[cluster] = [valid_preds[i]]
    
    print(f'cluster dictionary: {clust_dict}')
    
    # choose the highest ranking diffdock prediction from each cluster to include in the final structure
    spheres = []

    for clust, pdbs in clust_dict.items():
        sph_pdb = pdbs[0]
        rank0 = int(str(pdbs[0]).split('rank')[1].split('_')[0])
        for i in range(1,len(pdbs)):
            if int(str(pdbs[i]).split('rank')[1].split('_')[0]) < rank0:
                sph_pdb = pdbs[i]
            else:
                continue

        spheres.append(sph_pdb)

    print(f'predictions to be kept: {spheres}')
    cmd.select("everything", "all")
    cmd.remove("everything")
    
    cmd.reinitialize()
    
    # combine three closest ligands with alphafold structure
    cmd.load(af_pdb, object='af_struct')
    #cmd.save('af2_2.pdb')
    for i, pred in enumerate(spheres):
        cmd.load(pred, object=f'pred_{i}')

    sphgen_pdb = base_name[:-4] + '_dd_sphgen.pdb'
    
    cmd.save(sphgen_pdb)

else:
    print(f'failed for: {af_pdb}')    


