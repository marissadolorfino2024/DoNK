#!/bin/python

# utils for ML on DoNK data

import numpy as np
from rdkit import Chem
from rdkit.Chem.rdmolops import GetAdjacencyMatrix
from rdkit.Chem import Draw
import glob
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import random
from scipy.stats import spearmanr
from torch.autograd import Variable
import time

import torch
from torch_geometric.data import Data
import pandas as pd
import scipy
import autograd
import random

import os

import networkx as nx
import matplotlib.pyplot as plt

from matplotlib import font_manager
import matplotlib.pylab as pylab

from typing import Callable
import os.path as osp
import sys
from torch.nn import Linear
import torch.nn.functional as F
from torch.nn.functional import relu
from torch.nn.functional import softmax
from torch_geometric.nn import GCNConv
from torch_geometric.nn import global_mean_pool
import torch.nn as nn
from torch import optim

from torch.nn.modules.module import Module
from torch.nn.parameter import Parameter
from torch.nn import Linear
from torch_geometric.nn import GCNConv
from torch_geometric.nn import global_mean_pool
from torch_geometric.loader import DataLoader

import os.path as osp
from torch_geometric.data import Dataset

# function for saving model weights at each epoch
def save(name, epoch, model, batchsize, lr, result_dir):
    """ 
    function to save current state of model
    """
    if epoch==0:
        torch.save(model.state_dict(),'models/{}/{}_initial_{}.pth'.format(result_dir, name, epoch))
    else:
        torch.save({'epoch' : epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'batchsize': batchsize,
            'learning_rate' : lr,
            },'models/{}/{}_epoch_{}.pth'.format(result_dir, name, epoch))
    print("Saved {} at epoch {}\n".format(name, epoch+1))


# function to split dataset into train/val/test
def split_data(dataframe, trainsize=0.8):
    """
    given pandas dataframe, generate train, test, and validation sets (as dataframes). will then need to generate dataset and load with dataloader
    """
    # shuffle dataframe
    dataframe = dataframe.sample(frac=1)
    
    # split into train, test, validation sets
    train_set, test_set = train_test_split(dataframe,train_size=trainsize)
    test_set, val_set = train_test_split(test_set, train_size=0.5)
    
    return train_set, test_set, val_set


# function to compute one-hot encoding for input
def one_hot_encoding(x, permitted_list):
    """
    generate one hot encoding given permitted list
    """
    # if not permitted, x is last permitted item in permitted_list
    if x not in permitted_list:
        x = permitted_list[-1]

    # onehot encode
    binary_encoding = [int(boolean_value) for boolean_value in list(map(lambda s: x == s, permitted_list))]

    return binary_encoding


# function to get atom featurization. takes RDKIT input, returns 1d array of atom features
def get_atom_features(atom, use_chirality=True, hydrogens_implicit=True): # might try to use hydrogens as explicit and chirality as false for a comparison
    """
    generates the atom features of a singular atom as a one hot encoding
    """
    permitted_list_of_atoms = ['C','N','O','S','F','Si','P','Cl','Br','Mg','Na','Ca','Fe','As','Al','I', 'B','V','K','Tl','Yb','Sb','Sn','Ag','Pd','Co','Se','Ti','Zn', 'Li','Ge','Cu','Au','Ni','Cd','In','Mn','Zr','Cr','Pt','Hg','Pb','Dy'] # add Dy for DNA

    if hydrogens_implicit == False:
        permitted_list_of_atoms = ['H'] + permitted_list_of_atoms

    # compute atom features as onehot encodings
    atom_type_enc = one_hot_encoding(str(atom.GetSymbol()), permitted_list_of_atoms)

    n_heavy_neighbors_enc = one_hot_encoding(int(atom.GetDegree()), [0,1,2,3,4,"MoreThanFour"])

    formal_charge_enc = one_hot_encoding(int(atom.GetFormalCharge()), [-3,-2,-1,0,1,2,3,"Extreme"])

    hybridization_type_enc = one_hot_encoding(str(atom.GetHybridization()), ["S", "SP", "SP2", "SP3", "SP3D", "SP3D2", "OTHER"])

    is_in_a_ring_enc = [int(atom.IsInRing())]

    is_aromatic_enc = [int(atom.GetIsAromatic())]

    atomic_mass_scaled = [float((atom.GetMass() - 10.812)/116.092)]

    vdw_radius_scaled = [float((Chem.GetPeriodicTable().GetRvdw(atom.GetAtomicNum()) - 1.5)/0.6)]

    covalent_radius_scaled = [float((Chem.GetPeriodicTable().GetRcovalent(atom.GetAtomicNum()) - 0.64)/0.76)]

    # atom feature vector (concatenate all encodings from above)
    atom_feature_vector = atom_type_enc + n_heavy_neighbors_enc + formal_charge_enc + hybridization_type_enc + is_in_a_ring_enc + is_aromatic_enc + atomic_mass_scaled + vdw_radius_scaled + covalent_radius_scaled

    if use_chirality == True:
        chirality_type_enc = one_hot_encoding(str(atom.GetChiralTag()), ["CHI_UNSPECIFIED", "CHI_TETRAHEDRAL_CW", "CHI_TETRAHEDRAL_CCW", "CHI_OTHER"])
        atom_feature_vector += chirality_type_enc

    if hydrogens_implicit == True:
        n_hydrogens_enc = one_hot_encoding(int(atom.GetTotalNumHs()), [0,1,2,3,4,"MoreThanFour"])
        atom_feature_vector += n_hydrogens_enc

    return np.array(atom_feature_vector)


# function to get bond featurization
def get_bond_features(bond, use_stereochemistry = True):
    """
    generates the bond features of a single bond as one hot encoding
    """
    permitted_list_of_bond_types = [Chem.rdchem.BondType.SINGLE, Chem.rdchem.BondType.DOUBLE, Chem.rdchem.BondType.TRIPLE, Chem.rdchem.BondType.AROMATIC]

    bond_type_enc = one_hot_encoding(bond.GetBondType(), permitted_list_of_bond_types)

    bond_is_conj_enc = [int(bond.GetIsConjugated())]

    bond_is_in_ring_enc = [int(bond.IsInRing())]

    bond_feature_vector = bond_type_enc + bond_is_conj_enc + bond_is_in_ring_enc

    if use_stereochemistry == True:
        stereo_type_enc = one_hot_encoding(str(bond.GetStereo()), ["STEREOZ", "STEREOE", "STEREOANY", "STEREONONE"])
        bond_feature_vector += stereo_type_enc

    return np.array(bond_feature_vector)

# function to generate molecular graph from a SMILES string
def gen_molegraph(smiles, label): # in this case, the label will be the bioactivity fingerprint, but it could be any other label (like molecular property vector)
    """
    generate a molecular graph given the smiles string of the molecule (as a series of one hot encodings)
    """
    mol = Chem.MolFromSmiles(smiles)

    # get feature dimensions
    n_nodes = mol.GetNumAtoms() # number of atoms in molecule
    n_edges = 2*mol.GetNumBonds() # number of bonds*2 (each is encoded twice because adj matrix is symmetric)
    unrelated_mol = Chem.MolFromSmiles("O=O") # unrelated molecule for calculating the number 
    n_node_features = len(get_atom_features(unrelated_mol.GetAtomWithIdx(0)))
    n_edge_features = len(get_bond_features(unrelated_mol.GetBondBetweenAtoms(0,1)))

    # construct node feature matrix X of shape (n_nodes, n_node_features)
    X = np.zeros((n_nodes, n_node_features))

    for atom in mol.GetAtoms():
        X[atom.GetIdx(), :] = get_atom_features(atom)

    X = torch.tensor(X, dtype = torch.float)

    # construct edge index array E of shape (2, n_edges)
    (rows, cols) = np.nonzero(GetAdjacencyMatrix(mol))
    torch_rows = torch.from_numpy(rows.astype(np.int64)).to(torch.long)
    torch_cols = torch.from_numpy(cols.astype(np.int64)).to(torch.long)
    E = torch.stack([torch_rows, torch_cols], dim = 0)

    # construct edge feature array EF of shape (n_edges, n_edge_features)
    EF = np.zeros((n_edges, n_edge_features))

    for (k, (i,j)) in enumerate(zip(rows, cols)):

        EF[k] = get_bond_features(mol.GetBondBetweenAtoms(int(i),int(j)))

    EF = torch.tensor(EF, dtype = torch.float)

    label_tens = torch.tensor(label)

    graph = Data(x=X, edge_index = E, edge_attr = EF, y=label_tens)

    return graph
    

# graph dataset class # data is input as a df of smiles, and pre processing converts the smiles to graphs
# this dataset class should be compatible with the torch geometric dataloaders
class molegraph_dataset(Dataset):
    """
    given a pandas dataframe, generate a pytorch geometric dataset that is compatible with dataloader (for batching graphs)
    df_type should be 'train', 'test', 'validation'
    """
    def __init__(self, dataframe, df_type, transform=None, pre_transform=None):
        
        self.df_type = df_type
        self.dataframe = dataframe
        
        super().__init__(None, transform, pre_transform)
    
    @property
    def raw_smiles(self): # return a list of raw smiles (in the order they are in the given dataframe)
        return [self.dataframe['smiles']]
    
    @property
    def raw_labels(self): # return a list of raw labels (in the order they are in the given dataframe)... label should be a string which can be converted to a list of integers
        return [self.dataframe.iloc[:, 2:]]

    @property
    def processed_file_names(self):
        return [f'data_{i}.pt' for i in range(self.dataframe.shape[0])] # data graphs will be stored as tensors with a .pt extension, and named by zinc_id

    @property
    def processed_dir(self):
        return f'{self.df_type}_data'
    
    @property
    def raw_file_names(self):
        # satisfy the `raw_file_names` of the parent class requirement with a dummy implementation
        return ['dummy_file']

    def process(self):
        os.makedirs(self.processed_dir, exist_ok=True) # make the data directory
        idx = 0
        
        # read smiles from raw smiles, read label from raw labels
        # read label as string, convert to list of integers
        for raw_smile, raw_label in zip(self.raw_paths, self.raw_labels):
            label = list([int(label) for label in raw_label]) # int list of bioactivity fingerprint from string 
            
            data = gen_molegraph(raw_smile, label)

            if self.pre_filter is not None and not self.pre_filter(data):
                continue

            if self.pre_transform is not None:
                data = self.pre_transform(data)

            torch.save(data, osp.join(self.processed_dir, f'data_{idx}.pt'))
            idx += 1

    def len(self):
        return len(self.processed_file_names)

    def get(self, idx):
        data = torch.load(osp.join(self.processed_dir, f'data_{idx}.pt'))
        return data        


class GCN(torch.nn.Module):
    """
    graph autoencoder and decoder (to generate molecular fingerprints)
    """
    def __init__(self, num_node_features, hidden_channels, bioprint_size):
        super(GCN, self).__init__()
        # first three layers are encoder layers, last layer is decoder layer (linear)
        self.conv1 = GCNConv(num_node_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.conv3 = GCNConv(hidden_channels, hidden_channels) # so greater than or equal to around 20,000 ???
        self.dc = Linear(hidden_channels, bioprint_size) # hidden channels should be > bioprint size

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        x = x.relu()
        x = self.conv3(x, edge_index)

        # readout layer
        x = global_mean_pool(x, batch)  # [batch_size, hidden_channels]

        # apply the final linear layer (decoder)
        x = F.dropout(x, p=0.5, training=self.training) # dropout
        x = self.dc(x)
        
        # binarize output 
        # x = x.sigmoid() # could also do sigmoid here
        x = x.softmax() # convert to probabilities between 0 and 1 
        threshold = Variable(torch.Tensor([0.5])) 
        x = (x >= threshold).float() # convert vector to binary fingerprint prediction
        
        return x
    

def train(model, traindata, valdata, testdata, epochs=100, lr=0.01, batchsize=64, loss=torch.nn.MSELoss):
    """
    train model on traindata, with default epochs=100, lr=0.01. Must provide loss function via `loss`. it also includes testing model on test set after last epoch
    """
    optimizer = optim.Adam(model.params(), lr)
    mseloss = loss(reduction='none')
    
    epoch_train_losses = []
    epoch_val_losses = []
    for epoch in range(len(epochs)):
        t = time.time()
        optimizer.zero_grad()
        
        print(f'start of training for epoch {epoch+1} out of {epochs+1} epochs')
        model.train()
        train_loader = DataLoader(traindata, batch_size=batchsize)
        
        batch_losses = []
        for data, label in train_loader:
            out = model(data)
            batch_loss = mseloss(out, label)
            
            # weight accuracy on hits higher than accuracy on non-hits
            weights = torch.where(label == 1, 2.0, 1.0)
            w_loss = torch.mean(weights * batch_loss)
            
            # back propagation
            w_loss.backward()
            optimizer.step()
            
            # w_loss to device
            w_loss = w_loss.cpu()
            w_loss = w_loss.item()        
            batch_losses.append(w_loss)    
            
        epoch_train_losses.append(np.mean(batch_losses))
        print(f'training loss at epoch {epoch+1}: {np.mean(batch_losses)}')

        # validate data within training loop via validate function
        val_loss = validate(model, valdata, batchsize, loss)
        epoch_val_losses.append(val_loss)
        print(f'validation loss at epoch {epoch+1}: {val_loss}')
        print(f'time for training and validation at {epoch+1}: {time.time() - t}')
        
        save(name, epoch+1, model, batchsize, lr, result_dir=name)
        
    print('training complete')
    
    # make plots of training and validation loss and save as figure with model name
    x = range(1,epochs+1)
    y = epoch_train_losses
    y2 = epoch_val_losses

    plt.plot(x, y, color='magenta', label='train loss')  
    plt.plot(x, y2, color='lightpink', label='validation loss') 

    plt.xlabel("epoch")
    plt.ylabel("weighted MSELoss")
    plt.title("loss across epochs")
    plt.legend()

    plt.savefig(f'models/{name}/train-val_loss.png')
    
    # test model on test data 
    test_loss = test(model, testdata, batchsize, loss) 
    print(f'loss on test set after training complete: {test_loss}')
    
    
def validate(model, valdata, batchsize, loss):
    """
    validate model given valdata
    """
    model.eval()
    mseloss = loss(reduction='none')
    
    val_loader = DataLoader(valdata, batch_size=batchsize)
    
    batch_losses = []
    with torch.no_grad():
        for data, label in val_loader:
            out = model(data)
            batch_loss = mseloss(out, label)
            
            # weight accuracy on hits higher than accuracy on non-hits
            weights = torch.where(label == 1, 2.0, 1.0)
            w_loss = torch.mean(weights * batch_loss)
            
            # w_loss to device
            w_loss = w_loss.cpu()
            w_loss = w_loss.item()
            batch_losses.append(w_loss)
            
    return np.mean(batch_losses)
    
def test(model, testdata, batchsize, loss):
    """
    test model given testdata
    """
    model.eval()
    mseloss = loss(reduction='none')
    
    test_loader = DataLoader(testdata, batch_size=batchsize)
    
    batch_losses = []
    with torch.no_grad():
        for data, label in test_loader:
            out = model(data)
            batch_loss = mseloss(out, label)
            
            # weight accuracy on hits higher than accuracy on non-hits
            weights = torch.where(label == 1, 2.0, 1.0)
            w_loss = torch.mean(weights * batch_loss)
            
            # w_loss to device
            w_loss = w_loss.cpu()
            w_loss = w_loss.item()
            batch_losses.append(w_loss)
            
    return np.mean(batch_losses)
        
