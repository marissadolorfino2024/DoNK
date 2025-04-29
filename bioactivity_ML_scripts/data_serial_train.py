#!/bin/python

from ml_utils import * # import ml functions from ml_utils.py
import torch
from torch import optim
from torch.nn import MSELoss
from datetime import date
import os
import shutil
import pyarrow
import pandas as pd

# script to train/val/test actual model

loss = torch.nn.MSELoss
batchsize = 64 
lr = 0.01
epochs = 100
name = f'graphtransform_{date.today()}_{lr}_{batchsize}_{epochs}'
data = 'pymol_donk_sample4ML.parquet'

sample_graph = gen_molegraph("O=O", [1,0]) 
num_node_features = sample_graph.x.size(1) # get number of node features for the molecular graphs

print(f'number of node features for molecular graphs: {num_node_features}')

hidden_channels = 20000
bioprint_size = 18162
model = GCN(num_node_features, hidden_channels, bioprint_size)

if os.path.isdir(f'models/{name}'):
    shutil.rmtree(f'models/{name}')
    os.mkdir(f'models/{name}')
    
else:
    os.mkdir(f'models/{name}')
    
# ensure GPU is utilized
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'using {device} device')

# load dataframe
df = pd.read_parquet(data)

# generate train, test, validation dataframes
traindf, testdf, valdf = split_data(df)

print(traindf.shape)
print(traindf.columns)
print(traindf.head())
print(testdf.shape)
print(testdf.head())
print(valdf.shape)
print(valdf.head())

# graphs are stored. if the process directory already exists, it will not be regenerated
traindata, testdata, valdata = molegraph_dataset(traindf, df_type='train'), molegraph_dataset(testdf, df_type='test'), molegraph_dataset(valdf, df_type='validation')

train(model, traindata, valdata, testdata)
