#!/bin/usr/python

# script to calculate RMSD between alphafold proteinmpnn design and original scaffolds

import sys
import glob
import subprocess
import os, itertools
import csv
import numpy as np

# script to calculate the RMSD and TM align scores between soluble and transmembrane input sets

#design = sys.argv[1]
output_file = sys.argv[1]

to_write = ['design,scaffold,rmsd\n']

for design in glob.glob('*.pdb'):
    scaf_name = design.split('prepped_formatted')[0] + 'prepped_formatted.pdb'
    scaffold = '/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/scaffolds/prepped_formatted_scaffolds/'+scaf_name
    
    cmd = "/nfs/turbo/umms-maom/mdolo/opt/TMalign " + design + " " + scaffold
    
    output = subprocess.check_output(["/nfs/turbo/umms-maom/mdolo/opt/TMalign", design, scaffold])
    
    output_lines = output.decode().split("\n")
    
    for line in output_lines:
        if "RMSD" in line:
            RMSD = float(line.split(',')[1].replace("RMSD=","").lstrip())
            to_write.append(design+','+scaf_name+','+str(RMSD)+'\n')
        else:
            pass
    
with open(output_file, 'w') as ofile:
    for oline in to_write:
        ofile.write(oline)


