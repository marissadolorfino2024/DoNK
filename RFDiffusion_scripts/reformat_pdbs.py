#!/bin/python

import sys

# script to reformat a pdb file to be a single chain, with res count starting at 1
# the resulting formatted pdb will contain only chain A except for the HETATM records, which will be chain X
# this is to format the pdbs for RFDiffusion and for downstream binding pocket design

pdbfile = sys.argv[1]

formatted_pdb = pdbfile[:-4] + '_formatted.pdb'

with open(pdbfile, 'r') as pdb:
    lines = pdb.readlines()

previous_resids = [0]

res_count = 1
for i in range(len(lines)):
    line = lines[i]
    if line[0:4] == 'ATOM':
        line = line[:21] + 'A' + line[22:]
        try:
            res_id = int(line[21:26])
        except:
            res_id = int(line[22:26])
        if res_id == previous_resids[-1] or previous_resids[-1] == 0:
            new_id = res_count
            res_num = ' '*(4-len(str(new_id)))
            res_num = (res_num + str(new_id))
            line = line[:22] + res_num + line[26:]
            
            previous_resids.append(res_id)

        else:
            res_count += 1
            new_id = res_count
            res_num = ' '*(4-len(str(new_id)))
            res_num = res_num + str(new_id)
            line = line[:22] + res_num + line[26:]
            
            previous_resids.append(res_id)

        with open(formatted_pdb, 'a+') as new_pdb:
            new_pdb.write(str(line))
        
    elif line[0:6] == 'HETATM':
        line = line[:21] + 'X' + line[22:]
        
        with open(formatted_pdb, 'a+') as new_pdb:
            new_pdb.write(str(line))
    
    elif line[0:3] == 'TER':
        if lines[i-1][0:4] == 'ATOM' and lines[i+1][0:4] == 'ATOM':
            continue
        else:
            with open(formatted_pdb, 'a+') as new_pdb:
                new_pdb.write(str(line))

    elif line[0:6] == 'ANISOU':
        pass

    else:
        with open(formatted_pdb, 'a+') as new_pdb:
            new_pdb.write(str(line))

