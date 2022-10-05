"""
Subscript of Sabres to parse nanopore medaka .vcf outputs for resistance detection
Unfortunately, medaka does not provide frequency of the mutation, so the mutations
presented from this format would only show consensus level mutations.
"""

import datetime
import pandas as pd

import medaka_cleanup as mc

now = datetime.datetime.now()
time_log = now.strftime("%Y-%m-%d %H:%M:%S")
drop_columns = ['Nucleotide', 'Mutation']
pd.set_option('display.max_rows', None)

def medaka_setup(input_file, column):
    """
    Takes the medaka dataframe and generates a new dataframe per sample.
    """
    sample_df = mc.splitting_vcf(input_file)
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
            'DP'
            ]
        ).fillna("-")
    print(f"{time_log}: Generating File - {column}.snpprofile")
    return sample_data
