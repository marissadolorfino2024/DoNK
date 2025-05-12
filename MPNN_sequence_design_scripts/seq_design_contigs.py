#!/bin/python

import sys
import numpy as np
import math
import glob

# script to get designable residues (based on proximity to ligand) if center of residue is within x angstroms of  

# path to directory containing scaffold pdbs
path_to_pdbs = sys.argv[1]

# path to directory containing RFdiffusion backbones
path_to_designs = sys.argv[2]

# distance threshold
x = float(sys.argv[3])

regex = path_to_pdbs + '*.pdb'
regex2 = path_to_designs + '*_0001.pdb'

contig_dict = {}

for pdbfile in glob.glob(regex): 
    atom_dict = {}
    hetatm_coords = []
    res_to_design = []
    
    with open(pdbfile, 'r') as pdb:
        lines = pdb.readlines()
    
    for line in lines:
        if line[0:4] == 'ATOM':
            x_coord = float(line[30:38])
            y_coord = float(line[38:46])
            z_coord = float(line[46:54])
    
            res_id = int(line[22:26])
            if res_id in atom_dict.keys():
                atom_dict[res_id].append([x_coord, y_coord, z_coord])
            else:
                atom_dict[res_id] = [[x_coord, y_coord, z_coord]]
            
        elif line [0:6] == 'HETATM':
            x_coord = float(line[30:38]) 
            y_coord = float(line[38:46]) 
            z_coord = float(line[46:54])
    
            hetatm_coords.append([x_coord, y_coord, z_coord])
    
        else:
            continue
    
    for res in atom_dict.keys():
        x_mean = np.mean([atom_dict[res][i][0] for i in range(len(atom_dict[res]))])
        y_mean = np.mean([atom_dict[res][i][1] for i in range(len(atom_dict[res]))])
        z_mean = np.mean([atom_dict[res][i][2] for i in range(len(atom_dict[res]))])
    
        res_center = [x_mean, y_mean, z_mean]
        for hetatm in hetatm_coords:
            dist = 0
            for i in range(len(res_center)):
                diffsq = (res_center[i] - hetatm[i])**2
                dist += diffsq
    
            dist = math.sqrt(dist)
    
            if dist < x:
                res_to_design.append(res)
            else:
                continue
        
    res_to_design = list(set(res_to_design))
    res_to_design = [str(res) for res in res_to_design]
    res_to_design = ' '.join(res_to_design)
    
    pdbfile = pdbfile.split("prepped_formatted_scaffolds/")[1]
    scaffold = pdbfile.split("_prepped_formatted")[0]

    contig_dict[scaffold] = res_to_design

# iterate through the rfdiff backbones to create contig text file with allowed residues to design (rf backbone will share same contigs as scaffold backbone)
for rf_bb in glob.glob(regex2):
    rf_file = rf_bb.split("noised_receptors/")[1]
    rf_scaffold = rf_file.split("_prepped_formatted")[0]

    rf_contigs = contig_dict[rf_scaffold]

    with open('tasks.txt', 'a+') as tasks:
        tasks.write(rf_bb)
        tasks.write("\n")

    with open('mpnn_contigs.txt', 'a+') as contigs:
        contigs.write(rf_contigs)
        contigs.write("\n")
