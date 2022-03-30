import pandas as pd
import numpy as np
from io import StringIO

pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'

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

def generate_snpprofile(file, database, outfile):
    # print as separate file for easy manual checking.
    snpprofile = pd.DataFrame(resistance_addition(file, database))
    snpprofile.to_csv(outfile, sep='\t', index = False)
    
    #send to pull_resistance
    return snpprofile
