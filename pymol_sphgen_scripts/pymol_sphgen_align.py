#!/bin/usr/python

import pymol.cmd as cmd
import sys
import glob
import numpy as np
import math

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

name = af_pdb.split('_formatted_')[0]
name = name + '_formatted.pdb'
scaffold = '/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/scaffolds/prepped_formatted_scaffolds/' + name 

# get ligand name of scaffold (ref) ligand
ref_lig = get_lig(scaffold)

# load objects
cmd.load(af_pdb, object='af_struct')

cmd.save('af22.pdb')

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

# compute the rmsd and store dictionary, load 3 closest with alphafold structure, save as one pdb. this will be input to ucsf dock
def dif_ligs(lig, ref):
    with open(lig, 'r') as ligfile:
        lig_lines = ligfile.readlines()

    with open(ref, 'r') as reffile:
        ref_lines = reffile.readlines()

    lig_atoms = []
    for line in lig_lines: 
        if line[0:6] == 'HETATM':
            lig_atoms.append(np.array([float(line[32:38]), float(line[40:46]), float(line[48:54])]))

        else:
            continue

    ref_atoms = []
    for line in ref_lines:
        if line[0:6] == 'HETATM':
            ref_atoms.append(np.array([float(line[32:38]), float(line[40:46]), float(line[48:54])]))

        else:
            continue

    sum_dist = 0
    for ref_atom in ref_atoms:
        for lig_atom in lig_atoms:
            sum_sq = 0
            for i in range(3):
                sum_sq += ((ref_atom[i] - lig_atom[i])**2)

            sum_dist += math.sqrt(sum_sq)

    avg_dist = sum_dist / len(ref_atoms)

    return avg_dist

# choose three closest ligands
dist_dict = {}
for lig_pred in glob.glob("rank*"):
    dist_dict[lig_pred] = dif_ligs(lig_pred, 'ref_lig.pdb')

# sort dist_dict by increasing average distance to reflig
sort_dict = dict(sorted(dist_dict.items(), key=lambda item: item[1]))

spheres = list(sort_dict.keys())[:3]

cmd.select("everything", "all")
cmd.remove("everything")

cmd.reinitialize()

# combine three closest ligands with alphafold structure
cmd.load(af_pdb, object='af_struct')
cmd.save('af2_2.pdb')
for i, pred in enumerate(spheres):
    cmd.load(pred, object=f'pred_{i}')

sphgen_pdb = af_pdb[:-4] + '_dd_sphgen.pdb'

cmd.save(sphgen_pdb)


