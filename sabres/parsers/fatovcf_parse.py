"""
Subscript of Sabres to parse fatovcf (from UShER) .vcf outputs for resistance detection
"""

import os
import datetime
from io import StringIO
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
neworder = [
    'Filename',
    'REF',
    'POS',
    'ALT',
    'REFPOSALT'
]

def file_cleanup(file):
    """
    Remove the lines of the vcf file that contain the ##
    """
    with open(file, 'r') as vcf:
        oneline = ''
        lines = vcf.readlines()
        for line in lines:
            if not line.startswith('##'):
                oneline += line
        return oneline

def file2df(file):
    """
    Sets up the read of varscan vcf file without the seriously unnecessary hashes,
    also will print which file is being read for the log.
    """
    now = datetime.datetime.now()
    time_log = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_log}: Reading File - {file}")
    return pd.read_csv(StringIO(file_cleanup(file)), sep='\t', header = 0)

def fatovcf_setup(file):
    """
    converting tsv to dataframe and begin removing unwanted columns
    """
    vcf_df = pd.DataFrame(file2df(file))
    vcf_df.rename(columns={'ID': 'REFPOSALT'}, inplace=True)
    vcf_df['Filename'] = os.path.splitext(
        os.path.basename(file)
    )[0]
    str_rm = '|'.join(['.varscan.snps'])
    vcf_df['Filename'] = vcf_df['Filename'].str.replace(
        str_rm, ''
    )
    snp_df = vcf_df.reindex(columns=neworder)
    return snp_df
