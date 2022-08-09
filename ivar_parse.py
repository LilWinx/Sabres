"""
Subscript of Sabres to parse iVar .tsv outputs for resistance detection
"""
import os
import datetime
import pandas as pd
import numpy as np


neworder = [
    'Filename',
    'REF',
    'POS',
    'ALT',
    'REFPOSALT',
    'TOTAL_DP',
    'ALT_FREQ',
    'REF_AA',
    'ALT_AA',
    'SNS'
]
choices = ('N/A', 'S')
pd.set_option('display.max_rows', None)

def file2df(file):
    """
    Sets up the read of ivar tsv file, also will print which file is being read for the log.
    """
    now = datetime.datetime.now()
    time_log = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_log}: Reading File - {file}")
    return pd.read_csv(file, sep ='\t', header = 0)

def ivar_setup(file):
    """
    converting tsv to dataframe and begin removing unwanted columns
    generates new column called REFPOSALT
    calculates S/NS
    """
    # tsv file parsing and set up for removal
    tsv_df = pd.DataFrame(file2df(file))

    # remove unwanted columns and reorder
    tsv_df['REFPOSALT'] = tsv_df['REF'] + tsv_df['POS'].astype(str) + tsv_df['ALT']

    # calculate synonymous and non-synonymous mutations
    conditions = [
        (tsv_df['REF_AA'] == "NA") & (tsv_df['ALT_AA'] == "NA"),
        (tsv_df['REF_AA'] == tsv_df['ALT_AA'])
    ]
    tsv_df['SNS'] = np.select(conditions, choices, default='NS')
    tsv_df['Filename'] = os.path.splitext(
        os.path.basename(file)
    )[0]
    str_rm = '|'.join(['_t01', '_q20t01'])
    tsv_df['Filename'] = tsv_df['Filename'].str.replace(
        str_rm, ''
    )
    tsv_df=tsv_df.reindex(columns=neworder)
    return tsv_df
