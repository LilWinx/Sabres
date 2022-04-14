import os
import pandas as pd
import numpy as np
from io import StringIO
import pangolin_parse as pp
import datetime

pd.set_option('display.max_rows', None)
drop_columns_pango= ['Nucleotide', 'Mutation', 'name']
drop_columns = ['Nucleotide', 'Mutation']
neworder_varscan_pango = ['Filename', 'Lineage', 'REF', 'POS', 'ALT', 'REFPOSALT', 'HET', 'DP', 'FREQ', 'Protein', 'Interest', 'Note']
neworder_varscan = ['REF', 'POS', 'ALT', 'REFPOSALT', 'HET', 'DP', 'FREQ', 'Protein', 'Interest', 'Note']

def file_cleanup(file):
    with open(file, 'r') as vcf:
        oneline = ''
        lines = vcf.readlines()
        for line in lines:
            if not line.startswith('##'):
                oneline += line
        return oneline

def file2df(file):
    now = datetime.datetime.now()
    time_log = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_log}: Reading File - {file}")
    return pd.read_csv(StringIO(file_cleanup(file)), sep='\t', header = 0)

def data_setup(file):
    df = pd.DataFrame(file2df(file))
    if df.empty:
        return df
    df.drop(df.columns[[0, 2, 5, 6, 8]], axis = 1, inplace = True)
    df = df[['REF', 'POS', 'ALT', 'INFO', 'Sample1']]
    df[['adp', 'wt', 'HET', 'hom', 'nc']] = df.INFO.str.split(';', expand=True)
    df.drop(['adp', 'wt', 'hom', 'nc', 'INFO'], axis = 1, inplace = True)
    df[['GT', 'GQ', 'SDP', 'DP', 'RD', 'AD', 'FREQ', 'PVAL', 'RBQ', 'ABQ', 'RDF', 'RDR', 'ADF', 'ADR']] = df.Sample1.str.split(':', expand=True)
    df.drop(['GT', 'GQ', 'SDP', 'RD', 'AD', 'PVAL', 'RBQ', 'ABQ', 'RDF', 'RDR', 'ADF', 'ADR', 'Sample1'], axis = 1, inplace = True)
    df['REFPOSALT'] = df['REF'] + df['POS'].astype(str) + df['ALT']
    neworder = ['REF', 'POS', 'ALT', 'REFPOSALT', 'HET', 'DP', 'FREQ']
    df=df.reindex(columns=neworder)
    result = df.sort_values (by = 'POS')
    return result


def resistance_addition(file, database):
    preres_df = data_setup(file)
    if preres_df.empty == True:
        return preres_df
    resistance_markers = pd.read_csv(database, sep='\t', header = 0)
    resdf = pd.DataFrame(resistance_markers)
    res_merge = pd.merge(preres_df, resdf, left_on='REFPOSALT', right_on='Mutation', how='left').fillna('-')
    return res_merge
    
def varscan_pango(file, database, pango):
    pango_df = pp.lineage_addition(pango)
    varscan_df = resistance_addition(file, database)
    if varscan_df.empty == True:
        return varscan_df
    varscan_df['Filename'] = os.path.splitext(os.path.basename(file))[0]
    varscan_df['Filename'] = varscan_df['Filename'].str.replace(".varscan.snps","", regex = True)
    varscan_df['Lineage'] = varscan_df['Filename'].map(pango_df.drop_duplicates(subset=['name'], keep='first').set_index('name')['Lineage']).fillna('-')
    varscan_df.drop(drop_columns, axis = 1, inplace = True)
    pango_res_clean=varscan_df.reindex(columns=neworder_varscan_pango)
    return pango_res_clean
    

def generate_snpprofile(file, database, pango, outfile):
    # print as separate file for easy manual checking.
    snpprofile = varscan_pango(file, database, pango)
    if snpprofile.empty == True:
        return snpprofile
    snpprofile.to_csv(outfile, sep='\t', index = False)
    #send to pull_resistance
    return snpprofile
   

def generate_snpprofile_xpango(file, database, outfile):
    # print as separate file for easy manual checking.
    snpprofile = resistance_addition(file, database)
    if snpprofile.empty == True:
        return snpprofile
    snpprofile.drop(drop_columns, axis = 1, inplace = True)
    snp_csv = snpprofile.reindex(columns=neworder_varscan)
    snp_csv.to_csv(outfile, sep='\t', index = False)
    #send to pull_resistance
    return snpprofile

