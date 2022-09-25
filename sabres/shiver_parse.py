"""
Subscript of Sabres to parse shiver .vcf outputs for resistance detection
"""

import os
import datetime
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
choices = ('A', 'C', 'G', 'T')
neworder = [
    'Filename',
    'REF',
    'POS',
    'ALT',
    'REFPOSALT',
    'Total DP',
    'Freq'
]

def file2df(file):
    """
    Sets up the read of shiver csv file, also will print which file is being read for the log.
    """
    now = datetime.datetime.now()
    time_log = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_log}: Reading File - {file}")
    return pd.read_csv(file, sep =',', header = 0)

def shiver_setup(file):
    """
    convert shiver csv to vcf style file
    """
    csv_df = pd.DataFrame(file2df(file))
    csv_df.columns = ['POS', 'REF', 'A', 'C', 'G', 'T', 'Gap', 'N'] # completely replace the column names
    csv_df['Total DP'] = csv_df['A'] + csv_df['C'] + csv_df['G'] + csv_df['T']
    csv_df[['A%', 'C%', 'G%', 'T%']] = csv_df[['A', 'C', 'G', 'T']]/csv_df['Total DP'].values[:,None] * 100
    # get new consensus column to know which are above 95%
    conditions = [
        (csv_df['A%'] > 95),
        (csv_df['C%'] > 95),
        (csv_df['G%'] > 95),
        (csv_df['T%'] > 95)
    ]
    csv_df['Sub'] = np.select(conditions, choices, default="Sub")
    # extract lines that are either "Sub" in the consensus column and not equal to REF
    snp_df = csv_df.loc[(csv_df['REF'] != csv_df['Sub'])]
    # calculate
    freq_choices = [snp_df['A%'], snp_df['C%'], snp_df['G%'], snp_df['T%']]
    if snp_df['Sub'].str.contains('Sub').any():
        sub_conditions = [
            (snp_df['A%'] > 5) & (snp_df['REF'] != 'A'),
            (snp_df['C%'] > 5) & (snp_df['REF'] != 'C'),
            (snp_df['G%'] > 5) & (snp_df['REF'] != 'G'),
            (snp_df['T%'] > 5) & (snp_df['REF'] != 'T')
        ]
        snp_df['ALT'] = np.select(sub_conditions, choices, default="This mutation is missing data")
        snp_df['Freq'] = np.select(sub_conditions, freq_choices, default="N/A")
    snp_df['REFPOSALT'] = snp_df['REF'] + snp_df['POS'].astype(str) + snp_df['ALT']
    snp_df['Filename'] = os.path.splitext(
        os.path.basename(file)
    )[0]
    str_rm = '|'.join(['_BaseFreqs.csv'])
    snp_df['Filename'] = snp_df['Filename'].str.replace(
        str_rm, ''
    )
    snp_df = snp_df.reindex(columns=neworder)
    return snp_df