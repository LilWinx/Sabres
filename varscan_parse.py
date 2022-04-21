"""
Subscript of Sabres to parse Varscan .vcf outputs for resistance detection
"""

import os
import datetime
from io import StringIO
import pandas as pd
import pangolin_parse as pp

pd.set_option('display.max_rows', None)
drop_columns_pango= ['Nucleotide', 'Mutation', 'name']
drop_columns = ['Nucleotide', 'Mutation']
neworder_varscan_pango = [
    'Filename',
    'Lineage',
    'REF',
    'POS',
    'ALT',
    'REFPOSALT',
    'HET',
    'DP',
    'FREQ',
    'Protein',
    'Interest',
    'Note'
]
neworder_varscan = [
    'REF',
    'POS',
    'ALT',
    'REFPOSALT',
    'HET',
    'DP',
    'FREQ',
    'Protein',
    'Interest',
    'Note'
]
neworder = [
    'REF',
    'POS',
    'ALT',
    'REFPOSALT',
    'HET',
    'DP',
    'FREQ'
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

def data_setup(file):
    """
    converting tsv to dataframe and begin removing unwanted columns
    generates new column called REFPOSALT
    """
    vcf_df = pd.DataFrame(file2df(file))
    if vcf_df.empty:
        return vcf_df
    vcf_df.drop(
        vcf_df.columns[[0, 2, 5, 6, 8]], axis = 1, inplace = True
    )
    vcf_df = vcf_df[['REF', 'POS', 'ALT', 'INFO', 'Sample1']]
    vcf_df[['adp', 'wt', 'HET', 'hom', 'nc']] = vcf_df.INFO.str.split(
        ';', expand=True
    )
    vcf_df.drop(
        ['adp', 'wt', 'hom', 'nc', 'INFO'], axis = 1, inplace = True
    )
    vcf_df[[
        'GT',
        'GQ',
        'SDP',
        'DP',
        'RD',
        'AD',
        'FREQ',
        'PVAL',
        'RBQ',
        'ABQ',
        'RDF',
        'RDR',
        'ADF',
        'ADR']] = vcf_df.Sample1.str.split(
            ':', expand=True
        )
    vcf_df.drop(
        [
            'GT',
            'GQ',
            'SDP',
            'RD',
            'AD',
            'PVAL',
            'RBQ',
            'ABQ',
            'RDF',
            'RDR',
            'ADF',
            'ADR',
            'Sample1'
        ], axis = 1, inplace = True
    )
    vcf_df['REFPOSALT'] = vcf_df['REF'] + vcf_df['POS'].astype(str) + vcf_df['ALT']
    vcf_df=vcf_df.reindex(columns=neworder)
    result = vcf_df.sort_values (by = 'POS')
    return result

def resistance_addition(file, database):
    """
    merge the resistance database to the new dataframe
    """
    preres_df = data_setup(file)
    if preres_df.empty is True:
        return preres_df
    resistance_markers = pd.read_csv(
        database, sep='\t', header = 0
    )
    resdf = pd.DataFrame(resistance_markers)
    res_merge = pd.merge(
        preres_df, resdf, left_on='REFPOSALT', right_on='Mutation', how='left'
    ).fillna('-')
    return res_merge

def varscan_pango(file, database, pango):
    """
    if --pangolin was called, this is the function it runs.
    adds the lineage data from pangolin folder into the profile
    """
    pango_df = pp.lineage_addition(pango)
    varscan_df = resistance_addition(file, database)
    if varscan_df.empty is True:
        return varscan_df
    varscan_df['Filename'] = os.path.splitext(
        os.path.basename(file)
    )[0]
    varscan_df['Filename'] = varscan_df['Filename'].str.replace(
        ".varscan.snps","", regex = True
    )
    varscan_df['Lineage'] = varscan_df['Filename'].map(
        pango_df.drop_duplicates(
            subset=['name'], keep='first'
        ).set_index('name')['Lineage']
    ).fillna('-')
    varscan_df.drop(
        drop_columns, axis = 1, inplace = True
    )
    pango_res_clean=varscan_df.reindex(
        columns=neworder_varscan_pango
    )
    return pango_res_clean

def generate_snpprofile(file, database, pango, outfile):
    """
    print as separate file for easy manual checking.
    """
    snpprofile = varscan_pango(
        file, database, pango
    )
    if snpprofile.empty is True:
        return snpprofile
    snpprofile.to_csv(
        outfile, sep='\t', index = False
    )
    #send to pull_resistance
    return snpprofile

def generate_snpprofile_xpango(file, database, outfile):
    """
    print as separate file for easy manual checking.
    """
    snpprofile = resistance_addition(file, database)
    if snpprofile.empty is True:
        return snpprofile
    snpprofile.drop(
        drop_columns, axis = 1, inplace = True
    )
    snp_csv = snpprofile.reindex(
        columns=neworder_varscan)
    snp_csv.to_csv(
        outfile, sep='\t', index = False
    )
    #send to pull_resistance
    return snpprofile
