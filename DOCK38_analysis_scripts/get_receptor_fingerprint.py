#!/bin/python

import sys
import glob
import pandas as pd
import numpy as np
import csv

# script that extracts the hits from the data file containing hits as the 7th column for the specified receptor
# the output file will effectively contain the receptor binary bioactivity fingerprint formatted as a one column csv file

data = sys.argv[1]
out = str(data)[:-3]+'csv'

row_names = []
hit_data = []

with open(data, 'r') as data:
    lines = data.readlines()

for i in range(len(lines)):
    line = lines[i]
    if i == 0:
        continue
    else:
        items = line.split(',')
        row_name = items[2]
        hit = items[6][:-1]

        row_names.append(row_name)
        hit_data.append(hit)

labs = lines[1]
labs = labs.split(',')
rec_name = labs[4]

df = pd.DataFrame(data=hit_data, columns=[rec_name], index=row_names)
df.to_csv(out)


