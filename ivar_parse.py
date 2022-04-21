"""
Subscript of Sabres to parse iVar .tsv outputs for resistance detection
"""
import os
import datetime
import pandas as pd
import numpy as np
import pangolin_parse as pp


ignored_columns = [
    'REGION',
    'REF_DP',
    'REF_RV',
    'REF_QUAL',
    'ALT_RV',
    'ALT_QUAL',
    'GFF_FEATURE',
    'REF_CODON',
    'ALT_CODON',
    'PVAL',
    'PASS'
]
neworder_ivar_pango = [
    'Filename',
    'Lineage',
    'REF', 'POS',
    'ALT',
    'REFPOSALT',
    'TOTAL_DP',
    'ALT_FREQ',
    'REF_AA',
    'ALT_AA',
    'SNS',
    'Protein',
    'Interest',
    'Note'
]
neworder_ivar = [
    'REF',
    'POS',
    'ALT',
    'REFPOSALT',
    'TOTAL_DP',
    'ALT_FREQ',
    'REF_AA',
    'ALT_AA',
    'SNS',
    'Protein',
    'Interest',
    'Note'
]
choices = ('N/A', 'S')
drop_columns = ['Nucleotide', 'Mutation']
pd.set_option('display.max_rows', None)

def file2df(file):
    """
    Sets up the read of ivar tsv file, also will print which file is being read for the log.
    """
    now = datetime.datetime.now()
    time_log = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_log}: Reading File - {file}")
    return pd.read_csv(file, sep ='\t', header = 0)

def data_setup(file):
    """
    converting tsv to dataframe and begin removing unwanted columns
    generates new column called REFPOSALT
    calculates S/NS
    """
    # tsv file parsing and set up for removal
    tsv_df = pd.DataFrame(file2df(file))

    # remove unwanted columns and reorder
    tsv_df.drop(ignored_columns, axis = 1, inplace = True)
    tsv_df['REFPOSALT'] = tsv_df['REF'] + tsv_df['POS'].astype(str) + tsv_df['ALT']

    # calculate synonymous and non-synonymous mutations
    conditions = [
        (tsv_df['REF_AA'] == "NA") & (tsv_df['ALT_AA'] == "NA"),
        (tsv_df['REF_AA'] == tsv_df['ALT_AA'])
    ]
    tsv_df['SNS'] = np.select(conditions, choices, default='NS')
    return tsv_df

def resistance_addition(file, database):
    """
    merge the resistance database to the new dataframe
    """
    preres_df = data_setup(file)
    resistance_markers = pd.read_csv(database, sep='\t', header = 0)
    resdf = pd.DataFrame(resistance_markers)
    res_merge = pd.merge(
        preres_df, resdf, left_on='REFPOSALT', right_on='Mutation', how='left'
    ).fillna('-')
    return res_merge

def ivar_pango(file, database, pango):
    """
    if --pangolin was called, this is the function it runs.
    adds the lineage data from pangolin folder into the profile
    """
    pango_df = pp.lineage_addition(pango)
    ivar_df = resistance_addition(file, database)
    ivar_df['Filename'] = os.path.splitext(os.path.basename(file))[0]
    str_rm = '|'.join(['_t01', '_q20t01'])
    ivar_df['Filename'] = ivar_df['Filename'].str.replace(
        str_rm, ''
     ) #this wont work for everyone as only my lab adds _ivar to file names, prior to pangolin
    ivar_df['Lineage'] = ivar_df['Filename'].map(
        pango_df.drop_duplicates(
            subset=['name'], keep='first'
        ).set_index('name')['Lineage']
    ).fillna('-')
    ivar_df.drop(drop_columns, axis = 1, inplace = True)
    pango_res_clean = ivar_df.reindex(columns=neworder_ivar_pango)
    return pango_res_clean


def generate_snpprofile(file, database, pango, outfile):
    """
    print as separate file for easy manual checking.
    then send to pull_resistance.py
    """
    snpprofile = ivar_pango(file, database, pango)
    snpprofile.to_csv(outfile, sep='\t', index = False)
    return snpprofile


def generate_snpprofile_xpango(file, database, outfile):
    """
    WITHOUT PANGO DATA
    print as separate file for easy manual checking.
    then send to pull_resistance.py
    """
    # print as separate file for easy manual checking.
    snpprofile = resistance_addition(file, database)
    snpprofile.drop(drop_columns, axis = 1, inplace = True)
    snp_csv = snpprofile.reindex(columns=neworder_ivar)
    snp_csv.to_csv(outfile, sep='\t', index = False)
    return snpprofile
