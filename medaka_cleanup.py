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

now = datetime.datetime.now()
time_log = now.strftime("%Y-%m-%d %H:%M:%S")

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

def splitting_vcf_pango(file, database, pango):
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
    exploded_df = combined_df.assign(alt=combined_df.ALT.str.split(',')).explode('alt').reset_index(drop=True)
    exploded_df['ALT'] = exploded_df['alt']
    exploded_df.drop(exploded_df.columns[len(exploded_df.columns)-1], axis=1, inplace=True)
    for column in exploded_df.columns[9:]:
        mp.generate_snpprofile_pango(file, column, exploded_df, database, pango)

def splitting_vcf_xpango(file, database):
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
    exploded_df = combined_df.assign(alt=combined_df.ALT.str.split(',')).explode('alt').reset_index(drop=True)
    exploded_df['ALT'] = exploded_df['alt']
    exploded_df.drop(exploded_df.columns[len(exploded_df.columns)-1], axis=1, inplace=True)
    for column in exploded_df.columns[9:]:
        mp.generate_snpprofile_xpango(file, column, exploded_df, database)