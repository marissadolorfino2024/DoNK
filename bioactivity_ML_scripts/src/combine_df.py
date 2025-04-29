#!/bin/python

# script to view df (from parquet files)

import pandas as pd
import numpy as np
import sys
import pyarrow

bio_data = sys.argv[1]

zincdata = sys.argv[2]

bio = pd.read_parquet(bio_data)
zinc = pd.read_csv(zincdata, names=['zincid', 'smiles'])

bio.reset_index(inplace=True)

print(bio.head())
print(bio.shape)
bio_cols = list(bio.columns)

print(zinc.head())
print(zinc.shape)

for col in bio_cols:
    if col != 'zincid':
        bio[col] = bio[col].astype(int)
        bio[col] = bio[col].astype(str)
    
    else:
        continue
    
bio['biofing'] = bio.iloc[:, 1:].agg(''.join, axis=1) 

bio = bio[['zincid', 'biofing']]

combined = pd.merge(bio, zinc, on='zincid', how='inner')

combined.to_parquet('pymol_donk_formatted4ML.parquet')




