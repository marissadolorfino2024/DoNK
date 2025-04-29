#!/bin/python

import sys
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
import math
import glob
import csv

# script to compute the volume of a binding site given a pose of a ligand binding to receptor
# the volume is calculated by computing the convex hull of residues within the binding pocket of the ligand receptor pose

# set the heavy atom distance between res and lig to be considered binding pocket residue
if len(sys.argv) > 1:
    max_dist = float(sys.argv[2])
else:
    max_dist = 4 # if argument is not given, radius of 4 around ligand is considered to be binding pocket

print('max distance: ', max_dist)

# function to compute distance
# inputs should be length 3 lists with [x,y,z]
def dist3d(atom1, atom2):
    x1 = atom1[0]
    y1 = atom1[1]
    z1 = atom1[2]
    x2 = atom2[0]
    y2 = atom2[1]
    z2 = atom2[2]

    dist = math.sqrt(((x1-x2)**2) + ((y1 - y2)**2) + ((z1 - z2)**2))
    return dist

# function takes pdb file as input and max_dist

def bp_volume(pdbfile, max_dist):
    # from the HETATM lines in pdb, get the 3D coordinates 
    het_coords = []
    atom_lines = []
    with open(pdbfile, 'r') as pdb:
        lines = pdb.readlines()
    
        for line in lines:
            items = line.split()
            if items[0] == 'HETATM':
                threed = [float(items[5]), float(items[6]), float(items[7])]
                het_coords.append(threed)
            elif items[0] == 'ATOM':
                atom_lines.append(items)
    
    # definition of binding pocket residues -- all residues with at least 1 heavy atom within 4 ang (unless diff distance specified) of at least one ligand heavy atom
    
    bp_residues = set()
    # for each atom, compute distance between all the 3d coordinates in het_coords
    for atom in atom_lines:
        # chain id of atom
        try:
            int(atom[3])
            chain = atom[3]
        except:
            chain = atom[4]
    
        # res num of atom
        if '.' in atom[5]:
            res = atom[4]
        else:
            res = atom[5]
        
        res_id = [chain,res]
        res_id = tuple(res_id)
    
        # for each res_id, if already in bp_residues, then skip
        if res_id in bp_residues:
            continue
        else:
            if len(atom) == 12 or len(atom) == 13:
                atom_coords = [float(atom[6]), float(atom[7]), float(atom[8])]
            else:
                atom_coords = [float(atom[5]), float(atom[6]), float(atom[7])]
            
            for hetatom in het_coords:
                if res_id in bp_residues:
                    continue
                else:
                    distance = dist3d(hetatom, atom_coords)
                    if distance <= max_dist:
                        bp_residues.add(res_id)
                    else:
                        continue
    
    # with each chain id and res num in bp_residues set, get all the atoms of those residues
    atoms_in_bp = []
    for res in list(bp_residues):
        resn = list(res)[1]
        chain = list(res)[0]
        for atom in atom_lines:
            if atom[3] == chain or atom[4] == chain:
                if atom[4] == resn or atom[5] == resn:
                    if len(atom) == 12 or len(atom) == 13:
                        atom_coords = [float(atom[6]), float(atom[7]), float(atom[8])]
                        atoms_in_bp.append(atom_coords)
                    elif len(atom) == 11:
                        atom_coords = [float(atom[5]), float(atom[6]), float(atom[7])]
                        atoms_in_bp.append(atom_coords)
                    else:
                        continue
                else:
                    continue
            else:
                continue
    
    # now compute volume of convex hull containing the binding pocket atoms:
    try:
        hull = ConvexHull(atoms_in_bp)
        volume = hull.volume
        return volume
    except:
        print(pdbfile, ': error with calculating convex hull')
        return 0

# volumes to dict, dict to csv
vol_dict = {}
for pdb in glob.glob("*.pdb"):
    try:
        pdbfile = pdb
        volume = bp_volume(pdbfile,max_dist)
        vol_dict[pdbfile] = volume

    except:
        pdb_file = pdb
        volume = 'pdb error'
        vol_dict[pdbfile] = volume

with open('BP_volumes.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    for key in vol_dict:
        row = [key, vol_dict[key]]
        writer.writerow(row)


