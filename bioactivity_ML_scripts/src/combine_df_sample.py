#!/bin/python

# script to extract a sample of 10,000 rows and save as parquet

import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import numpy as np
import sys

bio_data = sys.argv[1]
zinc_data = sys.argv[2]
output_file = 'pymol_donk_sample4ML.parquet'

chunk_size = 10000  # define chunk size for processing

# zinc data (smiles identified by zinc id)
zinc = pd.read_parquet(zinc_data)

zincid_to_smiles = dict(zip(zinc['zincid'], zinc['smiles']))

# parquet file containing zincid and binary label for binding of ligands to receptors
parquet_file = pq.ParquetFile(bio_data)
parq_df = pd.read_parquet(bio_data)

parq_df.reset_index(inplace=True) # reset index so zincid is a column, not the index
for col in parq_df.columns:
    if col != 'zincid':
        parq_df[col] == parq_df[col].astype(int)

parq_df['smiles'] = parq_df['zincid'].map(zincid_to_smiles)

parq_df.to_parquet(output_file)

# # write empty parquet file with columns to be written
# schema_list = [('zincid', pa.string(), ('smiles', pa.string()))] + [(col, pa.string()) for col in parq_df.columns if col != 'zincid']
# schema = pa.schema(schema_list)

# # process in chunks
# with pq.ParquetWriter(output_file, schema) as writer:
#     # process only the first chunk to get one sample
#     for i in range(parquet_file.num_row_groups):
#         bio_chunk = parquet_file.read_row_group(i).to_pandas()
#         bio_chunk.reset_index(inplace=True) # reset index so zincid is a column, not the index
#         for col in bio_chunk.columns:
#             if col != 'zincid':
#                 bio_chunk[col] == bio_chunk[col].astype(int)
#             else:
#                 continue

#         print(bio_chunk.shape)
#         print(bio_chunk.head())
        
#         # merge with zinc data to associate biofingerprint with smiles
#         combined = pd.merge(bio_chunk, zinc, on='zincid', how='left')

#         # write first chunk and exit
#         writer.write_table(pa.Table.from_pandas(combined))
#         print(f"sample of {chunk_size} rows written to {output_file}.")
#         break  # exit after processing the first chunk
