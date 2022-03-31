import os
import pandas as pd
import numpy as np
from io import StringIO
import pangolin_parse as pp

pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'
drop_columns_pango= ['Nucleotide', 'Mutation', 'name']
drop_columns = ['Nucleotide', 'Mutation']
neworder_varscan_pango = ['Filename', 'Lineage', 'REF', 'POS', 'ALT', 'REFPOSALT', 'HET', 'DP', 'FREQ', 'Protein', 'Interest', 'Note']

def file_cleanup(file):
    with open(file, 'r') as vcf:
        oneline = ''
        lines = vcf.readlines()
        for line in lines:
            if not line.startswith('##'):
                oneline += line
        return oneline

def data_setup(file):
    df = pd.read_csv(StringIO(file_cleanup(file)), sep='\t', header = 0)
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
    preres_df = pd.DataFrame(data_setup(file))
    resistance_markers = pd.read_csv(database, sep='\t', header = 0)
    resdf = pd.DataFrame(resistance_markers)
    res_merge = pd.merge(preres_df, resdf, left_on='REFPOSALT', right_on='Mutation', how='left').fillna('-')
    res_merge.drop(['Nucleotide'], axis = 1, inplace = True)
    return res_merge

def varscan_pango(file, database, pango):
    pango_df = pd.DataFrame(pp.lineage_addition(pango))
    varscan_df = pd.DataFrame(resistance_addition(file, database))
    varscan_df['Filename'] = os.path.splitext(os.path.basename(file))[0]
    varscan_df['Filename'] = varscan_df['Filename'].str.replace("_t01","") #this wont work for everyone as only my lab adds _ivar to file names, prior to pangolin
    pango_res_merge = pd.merge(pango_df, varscan_df, left_on='name', right_on='Filename').fillna('-')
    pango_res_merge.drop(drop_columns_pango, axis = 1, inplace = True)
    pango_res_merge=pango_res_merge.reindex(columns=neworder_varscan_pango)
    
    return pango_res_merge

def generate_snpprofile(file, database, pango, outfile):
    # print as separate file for easy manual checking.
    snpprofile = pd.DataFrame(varscan_pango(file, database, pango))
    snpprofile.to_csv(outfile, sep='\t', index = False)
    
    #send to pull_resistance
    return snpprofile
    
def generate_snpprofile_xpango(file, database, outfile):
    # print as separate file for easy manual checking.
    snpprofile = pd.DataFrame(resistance_addition(file, database))
    snpprofile.to_csv(outfile, sep='\t', index = False)
    
    #send to pull_resistance
    return snpprofile
