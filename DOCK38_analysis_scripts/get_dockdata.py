#!/bin/python

import sys
import csv
import pandas as pd
import os

# extracts dock data from the extract_all.sort.txt file

in_file = "extract_all.sort.txt"

pwd = str(os.getcwd())

dir_name = os.path.basename(os.getcwd())

receptor_name = str(dir_name.split("2")[0])

tranch = "tranch" # this should be changed to 

out_file = receptor_name + tranch + "_dockdata.txt"

with open(in_file, 'r') as poses:
    lines = poses.readlines()

dirs = []
zincs = []
es = []
rec_name = []
tranch_name = []

col_names = ['result_dir', 'zinc_id', 'tranch', 'rec_name', 'total_energy']

for line in lines:
    items = line.split()

    dir_num = items[0][8:]
    zinc_id = items[2]
    tot_e = items[21]
    
    dirs.append(dir_num)
    zincs.append(zinc_id)
    es.append(tot_e)
    rec_name.append(receptor_name)
    tranch_name.append(tranch)

indices = list(range(len(dirs)))

df = pd.DataFrame(list(zip(dirs, zincs, tranch_name, rec_name, es)), index=indices, columns=col_names)
df.to_csv(out_file)

