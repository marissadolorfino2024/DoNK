#!/bin/python

import pandas as pd
import pyarrow

zinc_csv = pd.read_csv('/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/pymolalign_designs_andDock_originalset/product/zinc_ids_smiles.csv', names=['zincid', 'smiles'])

zinc_csv.to_parquet('zinc_ids_smiles.parquet')

