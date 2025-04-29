#!/bin/python

import sys
import pandas as pd
import itertools
import numpy as np
import matplotlib.pyplot as plt
import copy

# script to get hit information from a file containing the docked energies of ligands at one receptor
# hits chosen as the lowest 10% of docked energies

energies = sys.argv[1] # file that contains energy as the first column and ligand name as the second column 
out_name = sys.argv[2]

e_dict = {}
name_dict = {}

es = []
names = []

with open(energies, 'r') as in_file:
    for line in in_file:
        items = line.split()
        e = float(items[0])
        name = items[1]
        es.append(e)
        names.append(name)

sorted_es = copy.deepcopy(es)

sorted_es.sort()

top_10perc = []

non_hits = []

total_num = len(sorted_es)

top_num = round((total_num * 0.1))

for i in range(top_num):
    top_10perc.append(sorted_es[i])

for i in range(total_num):
    if i in range(top_num):
        continue
    else:
        non_hits.append(sorted_es[i])
    
for i in range(len(es)):
    index = 'line'+str(i)
    e_dict[index] = es[i]
    name_dict[index] = names[i]

top_dict = {}
for energy in top_10perc:
    for key in name_dict:
        if e_dict[key] == energy:
            name_key = key
            zinc_name = name_dict[name_key]
        else:
            continue
    top_dict[zinc_name] = energy

nonhit_dict = {}
for energy in non_hits:
    for key in name_dict:
        if e_dict[key] == energy:
            name_key = key
            zinc_name = name_dict[name_key]
        else:
            continue
    nonhit_dict[zinc_name] = energy

with open(out_name, 'w') as out:
    for key in top_dict:
        key = key
        val = top_dict[key]
        out.write(str(key)+'\t'+str(val)+'\t'+'1'+'\n')
    
    for key in nonhit_dict:
        key = key
        val = nonhit_dict[key]
        out.write(str(key)+'\t'+str(val)+'\t'+'0'+'\n')

