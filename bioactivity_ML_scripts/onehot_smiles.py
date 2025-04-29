#!/bin/python

## script to generate one hot encodings of the SMILES strings

import sys
import pandas as pd
import numpy as np
import pyarrow

def onehot(smiles_string,max_len,smiles_chars):
    smi_list = list(smiles_string)
    onehot_vec = ''
    for i in range(max_len): 
        if i < len(smi_list): # if the smiles string is shorter than max string length, pad with 0s to ensure vectors all of same length
            schar = smi_list[i]
            for possible_char in smiles_chars:
                if schar == possible_char:
                    onehot_vec = onehot_vec + '1'
                else:
                    onehot_vec = onehot_vec + '0'
        else:
            for possible_char in smiles_chars:
                onehot_vec = onehot_vec + '0'

    return onehot_vec

possible_chars = [' ',
                '#', '%', '(', ')', '+', '-', '.', '/',
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '=', '@',
                'A', 'B', 'C', 'F', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P',
                'R', 'S', 'T', 'V', 'X', 'Z',
                '[', '\\', ']',
                'a', 'b', 'c', 'e', 'g', 'i', 'l', 'n', 'o', 'p', 'r', 's',
                't', 'u'] 

smiles = []
zincids = []
chunk_size = 1000
chunks = pd.read_csv('zinc_ids_smiles.csv', names=['zincid', 'smiles'], chunksize=chunk_size)

# remove any smiles characters that aren't actually present in the smiles of this dataset
smiles_count = {schar: 0 for schar in possible_chars}
# determine max length of smiles strings to determine lenght of one-hot encoding vectors
max_len = 0
for i, chunk in enumerate(chunks):

    print(f'chunk {i} of {int(635431157/chunk_size)} chunks')

    smiles.append(list(chunk['smiles']))
    zincids.append(list(chunk['zincid']))
    
    chunk_max = max([len(smile) for smile in list(chunk['smiles'])])
    if chunk_max > max_len:
        max_len = chunk_max
    
    for smile in list(chunk['smiles']):
        for char in smile:
            smiles_count[char] += 1

# remove any smiles characters that are not seen in the molecules in the train or test set
smiles_chars_keep = [schar for schar in smiles_count.keys() if smiles_count[schar] != 0]

print(f'maximum length of smiles string: {max_len}')
print(f'smiles chars present in this dataset: {smiles_chars_keep}')

rows = [] # tuples: (zincid, smiles, onehot) 

for i in range(len(smiles)):
    hot_smi = onehot(smiles[i],max_len,smiles_chars_keep)
    rows.append((zincids[i], smiles[i], hot_smi))

smi_df = pd.DataFrame(rows, columns=['zincid', 'smiles', 'onehot_smiles'])

smi_df.to_parquet('onehot_smiles.parquet', engine='pyarrow')

smi_df.head()
smi_df.shape
