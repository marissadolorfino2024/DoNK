#!/bin/python

import pandas as pd
import sys

data = sys.argv[1]

df = pd.read_parquet(data)

print(df.shape)
print(df.columns)
print(df.head())
