#!/bin/python

# script to extract the total energies from the extract_all.sort.uniq.txt file generated as part of DOCK38 analysis

import sys

extract_all_file = sys.argv[1]
tenergy_ofile = sys.argv[2]

with open(extract_all_file, 'r') as efile:
    docklines = efile.readlines()

to_write = [['zincid', 'totalE']]
for line in docklines:
    zincid = line.split()[2]
    energy = line.split()[21]
    to_write.append([zincid, energy])

with open(tenergy_ofile, 'w') as ofile:
    for e in to_write:
        ofile.write(f'{e[0]}    {e[1]}\n')

