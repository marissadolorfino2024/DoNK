#!/bin/python

# script to calculate the center of the binding pocket (by calculating the center of ligand in binding pocket)

import sys
import numpy as np

pdbfile = sys.argv[1] # script takes one argument, which is the pdb file of the ligand docked to the protein

with open(pdbfile, 'r') as pdb:
    lines = pdb.readlines()

xs = []
ys = []
zs = []

for line in lines:
    cols = line.split()
    
    # check if line is ligand line
    if cols[0] == 'HETATM':
        xs.append(float(cols[5])) # append x,y,z coordinates of ligand atom to corresponding list
        ys.append(float(cols[6]))
        zs.append(float(cols[7]))

    else:
        continue

center_x = (max(xs) - min(xs))/2
center_y = (max(ys) - min(ys))/2
center_z = (max(zs) - min(zs))/2

pocket_center = [center_x, center_y, center_z]

print(pocket_center)


    
