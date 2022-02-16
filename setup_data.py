"""
Purpose: Read input CSV datasets, process & save them in a arrow format for a faster I/O

Usage:
>>> python setup.py

"""

import argparse
import json
import os
import re
from glob import glob

import pyarrow.feather as feather

from itertools import chain
from datetime import date

import vaex
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.dataset as ds

input_path = 'gsk_gcc_dashboard/data/train.csv'

def read_data():
    return pd.read_csv(input_path)

def process_data():
    df = read_data()
    print(len(df))
    df['not_toxic'] = np.where((df['toxic']+df['severe_toxic']+df['obscene']+df['threat']+df['insult']+df['identity_hate'])>0, 0, 1)
    df = df.drop_duplicates()
    #df.to_csv("gsk_gcc_dashboard/data/final.csv")
    df = df.set_index(['toxic', 'severe_toxic', 'obscene', 'threat','insult', 'identity_hate', 'not_toxic'],
                      drop=False).sort_index()
    #df_ar = pa.Table.from_pandas(df)
    schema = pa.Schema.from_pandas(df, preserve_index=True)
    table = pa.Table.from_pandas(df, preserve_index=True)

    sink = "gsk_gcc_dashboard/data/final.arrow"
    # Note new_file creates a RecordBatchFileWriter
    writer = pa.ipc.new_file(sink, schema)
    writer.write(table)
    writer.close()
    #ds.write_table(df_ar,'gsk_gcc_dashboard/data/final.arrow',format='arrow')

if __name__ == "__main__":
    process_data()
