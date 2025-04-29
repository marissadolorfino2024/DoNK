#!/bin/python

import sys

# script to get separate fasta files from proteinmpnn outputs, which are files containing all the designed sequences generated from a single backbone input

fafile = sys.argv[1] # .fa file generated from proteinMPNN

fa_name = fafile[:-3] # fill in prefix of name for the indiviudal fasta files to be generated 

output_dir = fafile + '_separated_fastas' # fill in the output directory name for which the indiviudal fasta files should be moved to

with open(fafile, 'r') as fa:
    if 'polar' in fafile:
        lines = fa.readlines()
        for i in range(len(lines)):
            if i % 2:
                pass
            else:
                if i == 0:
                    pass
                else:
                    fa_index = i/2 - 1
                    fasta_name = fa_name + '_polar_'+str(int(fa_index))+'.fasta'
                    output_file = output_dir + '/' + fasta_name
                    with open(output_file, 'w') as new:
                        new.write(lines[i])
                        new.write(lines[i+1])
    else:
        lines = fa.readlines()
        for i in range(len(lines)):
            if i % 2:
                continue
            else:
                if i == 0:
                    pass
                else:
                    fa_index = i/2 - 1
                    fasta_name = fa_name + '_hydro_'+str(int(fa_index))+'.fasta'
                    output_file = output_dir + '/' + fasta_name
                    with open(output_file, 'w') as new:
                        new.write(lines[i])
                        new.write(lines[i+1])

