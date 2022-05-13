"""
Subscript of Sabres to parse nanopore medaka .vcf outputs for resistance detection
Unfortunately, medaka does not provide frequency of the mutation, so the mutations presented from this format would only show consensus level mutations.
"""

import os
import datetime
import pandas as pd
from io import StringIO
import pangolin_parse as pp
import medaka_parse as mp

def gen_per_sample_add_res(column, sample_df, database):
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
    if sample_data.empty is True:
        return sample_data
    resistance_markers = pd.read_csv(
        database, sep='\t', header = 0
    )
    resdf = pd.DataFrame(resistance_markers)
    res_merge = pd.merge(
        sample_data, resdf, left_on='REFPOSALT', right_on='Mutation', how='left'
    ).fillna('-')
    return res_merge