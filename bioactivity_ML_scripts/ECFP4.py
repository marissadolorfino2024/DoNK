#!/bin/python

# script to get ECFP4 fingerprints from SMILES string

import pandas as pd
import subprocess
import numpy as np
import pyarrow
from rdkit import Chem
from rdkit.Chem import AllChem, MACCSkeys
from rdkit.Chem.AtomPairs import Pairs, Sheridan

# get ECFP4 fingerprint
def retrieve_mol_fp(smiles, fingerprint_type, fingerprint_length=1024):
    """Generate and return the molecule's fingerprint as a numpy array.
        Args:
            smiles (str): SMILES string of molecule
            fingerprint_type (str): 'ECFP4', 'FCFP4', 'MACCS'
            fingerprint_length (int): length of bit array
        Returns:
            np.ndarray: The fingerprint as a NumPy array.
    """
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        raise ValueError(f"Invalid SMILES string: {smiles}.")

    if fingerprint_type == 'ECFP4':
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=fingerprint_length)
    elif fingerprint_type == 'FCFP4':
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, useFeatures=True, nBits=fingerprint_length)
    elif fingerprint_type == 'MACCS':
        fp = list(MACCSkeys.GenMACCSKeys(mol).ToBitString()[1:])
    elif fingerprint_type == 'APDP':
        ap_fp = Pairs.GetAtomPairFingerprint(mol)
        dp_fp = Sheridan.GetBPFingerprint(mol)
        fp = np.zeros(fingerprint_length, dtype=np.uint8)
        ap_nonzero_elements = ap_fp.GetNonzeroElements().keys()
        dp_nonzero_elements = dp_fp.GetNonzeroElements().keys()
        for i in ap_nonzero_elements:
            fp[i % fingerprint_length] = 1
        for i in dp_nonzero_elements:
            fp[(i + 8388608) % fingerprint_length] = 1
    else:
        raise ValueError("Unsupported fingerprint type. Choose 'ECFP4', 'FCFP4', 'MACCS', or 'APDP'.")

    return np.array(fp, dtype=np.uint8)
