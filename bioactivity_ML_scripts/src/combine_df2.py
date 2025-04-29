#!/bin/python

# Optimized script to process large dataframes and save as Parquet

import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import numpy as np
import sys

bio_data = sys.argv[1]
zinc_data = sys.argv[2]
output_file = 'pymol_donk_formatted4ML.parquet'

chunk_size = 10000  # Define chunk size for processing

# Read zinc data with optimized dtypes
zinc = pd.read_csv(zinc_data, names=['zincid', 'smiles'], dtype={'zincid': 'str', 'smiles': 'str'})

# Open the Parquet file for reading in chunks
parquet_file = pq.ParquetFile(bio_data)

# Write an empty Parquet file to start (if needed)
schema = pa.schema([("zincid", pa.string()), ("biofing", pa.string()), ("smiles", pa.string())])
with pq.ParquetWriter(output_file, schema) as writer:
    # Process bio data in chunks
    for i in range(parquet_file.num_row_groups):
        bio_chunk = parquet_file.read_row_group(i).to_pandas()
        bio_chunk.reset_index(inplace=True)
        
        # Convert columns to int, then to str for concatenation
        for col in bio_chunk.columns:
            if col != 'zincid':
                bio_chunk[col] = bio_chunk[col].fillna(0).astype(int).astype(str)
        
        # Create the 'biofing' column
        bio_chunk['biofing'] = bio_chunk.iloc[:, 1:].agg(''.join, axis=1)
        bio_chunk = bio_chunk[['zincid', 'biofing']]
        
        # Merge with zinc data
        combined = pd.merge(bio_chunk, zinc, on='zincid', how='inner')
        
        # Append combined chunk to the output Parquet file
        writer.write_table(pa.Table.from_pandas(combined))

