#!/bin/python

import sys
import numpy as np

# script that relates the AlphaFold2 pLDDT and RMSD to the scores from MPNN sequence designs
# takes as input the RMSD vs pLDDT csv file generated from analysis of alphafold scripts

with open(sys.argv[1], 'r') as data:
    lines = data.readlines()

to_write = ['pdb\trmsd\tplddt\tlocal_score\tlocal_prob\tglobal_score\tglobal_prob\tseq_recovery\n']
for line in lines:
    items = line.split('\t')
    pdb = items[0]
    rmsd = items[1]
    plddt = items[2][:-1]

    mpnn_score = (pdb.split('__score_')[1]).split('__')[0]
    local_prob = str(np.exp(-float(mpnn_score)))

    global_score = (pdb.split('global_score_')[1]).split('__')[0]
    global_prob = str(np.exp(-float(global_score)))

    seq_recovery = (pdb.split('seq_recovery_')[1]).split('_')[0]

    to_write.append(f'{pdb}\t{rmsd}\t{plddt}\t{mpnn_score}\t{local_prob}\t{global_score}\t{global_prob}\t{seq_recovery}\n')

with open(sys.argv[2], 'w') as out:
    out.writelines(to_write)
