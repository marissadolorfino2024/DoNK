#!/bin/python

import sys
import csv

# this script extracts energies from the extract all files

extract = sys.argv[1] # path to extract_all txt file 
receptor = sys.argv[2] # name of receprot
tranch = sys.argv[3] # name of tranch of ligands docked

outfile = receptor + '_' + tranch + '_docking.csv'

with open(extract, 'r') as efile:
    lines = efile.readlines()

to_write = []
for line in lines:
    items = line.split()
    lig = items[2]
    energy = items[21]
    row = [receptor, lig, energy]

    to_write.append(row)

with open(outfile, 'w') as out:
    writer = csv.writer(out)

    for row in to_write:
        writer.writerow(row)

