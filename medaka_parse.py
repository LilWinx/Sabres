"""
Subscript of Sabres to parse nanopore medaka .vcf outputs for resistance detection
Unfortunately, medaka does not provide frequency of the mutation, so the mutations presented from this format would only show consensus level mutations.
"""

import os
import datetime
from random import sample
import pandas as pd
import numpy as np
from io import StringIO

file = "/Users/winx/Documents/testfile_medaka.vcf"
outfile = "/Users/winx/Documents/testfile_medaka.snpprofile"

pd.set_option('display.max_rows', None)

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

def splitting_vcf(file, outfile):
    vcf_df = pd.DataFrame(file2df(file))
    if vcf_df.empty:
        return vcf_df
    appended_data = []
    for column in vcf_df.columns[9:]:
        dynam_split = vcf_df[column].str.split(':', expand=True).add_prefix(column + '_')
        appended_data.append(dynam_split)
    appended_data = pd.concat(appended_data, axis = 1)
    combined_df = pd.concat([vcf_df.iloc[:, :9], appended_data], axis = 1)
    combined_df = combined_df[combined_df.columns.drop(list(combined_df.filter(regex='_1')))]
    combined_df.columns = combined_df.columns.str.rstrip("_0")
    combined_df['ALT'] = combined_df['ALT'].astype(str)
    exploded_df = combined_df.set_index(['ALT']).apply(lambda x: x.str.split(',').explode()).reset_index()
    for column in exploded_df.columns[9:]:
        gen_per_sample(file, column, exploded_df)
    exploded_df.to_csv(outfile, sep = '/t', index = False)

def gen_per_sample(file, column, sample_df):
    now = datetime.datetime.now()
    time_log = now.strftime("%Y-%m-%d %H:%M:%S")
    sep_outfile = os.path.join(os.path.dirname(file), column + '.snpprofile')
    sample_df[['DPS', 'Pool', 'DP']] = sample_df.INFO.str.split(';', expand=True)
    sample_df['DP'] = sample_df['DP'].str.replace("DP=", "")
    sample_df['Filename'] = str(column)
    sample_df['REFPOSALT'] = sample_df['REF'] + sample_df['POS'].astype(str) + sample_df['ALT']
    if sample_df.empty is True:
        return sample_df
    sample_data = sample_df[sample_df[column].str.contains('1')]
    sample_data = sample_data.reindex(
        columns=[
            'Filename',
            'REF',
            'POS',
            'ALT',
            'REFPOSALT',
            'DP',
            column
            ]
        ).fillna("-")
    print(f"{time_log}: Generating File - {column}.snpprofile")
    sample_data.to_csv(sep_outfile, sep = '\t', index = False)

print(splitting_vcf(file, outfile))