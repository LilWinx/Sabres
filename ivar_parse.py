import os
import pandas as pd
import numpy as np
import pangolin_parse as pp

ignored_columns = ['REGION', 'REF_DP', 'REF_RV', 'REF_QUAL', 'ALT_RV', 'ALT_QUAL', 'GFF_FEATURE', 'REF_CODON', 'ALT_CODON', 'PVAL', 'PASS']
neworder = ['REF', 'POS', 'ALT', 'REFPOSALT', 'TOTAL_DP', 'ALT_FREQ']
neworder_ivar_pango = ['Filename', 'Lineage', 'REF', 'POS', 'ALT', 'REFPOSALT', 'TOTAL_DP', 'ALT_FREQ', 'REF_AA', 'ALT_AA', 'SNS', 'Protein', 'Interest', 'Note']
choices = ('N/A', 'S')
drop_columns_pango= ['Nucleotide', 'Mutation', 'name']
drop_columns = ['Nucleotide', 'Mutation']

pd.options.mode.chained_assignment = None  # default='warn'

def data_setup(file):
    # tsv file parsing and set up for removal
    data = pd.read_csv(file, sep='\t', header = 0)
    df = pd.DataFrame(data)
    pd.set_option('display.max_rows', None)
    
    # remove unwanted columns and reorder
    df.drop(ignored_columns, axis = 1, inplace = True)
    df['REFPOSALT'] = df['REF'] + df['POS'].astype(str) + df['ALT']
    df=df.reindex(columns=neworder)

    # calculate synonymous and non-synonymous mutations
    dfsns = pd.DataFrame(data)
    dfsns = dfsns[['POS','REF_AA', 'ALT_AA']] 
    conditions = [
        (dfsns['REF_AA'] == "NA") & (dfsns['ALT_AA'] == "NA"),
        (dfsns['REF_AA'] == dfsns['ALT_AA'])
    ]
    dfsns['SNS'] = np.select(conditions, choices, default='NS')
    dfmerge = pd.merge(df, dfsns, on='POS', how='left').fillna('-')
    return dfmerge
        
def resistance_addition(file, database):
    # merge the resistance database to the new dataframe 
    preres_df = pd.DataFrame(data_setup(file))
    resistance_markers = pd.read_csv(database, sep='\t', header = 0)
    resdf = pd.DataFrame(resistance_markers)
    pd.set_option('display.max_rows', None)
    res_merge = pd.merge(preres_df, resdf, left_on='REFPOSALT', right_on='Mutation', how='left').fillna('-')
    return res_merge

def ivar_pango(file, database, pango):
    pango_df = pd.DataFrame(pp.lineage_addition(pango))
    ivar_df = pd.DataFrame(resistance_addition(file, database))
    ivar_df['Filename'] = os.path.splitext(os.path.basename(file))[0]
    ivar_df['Filename'] = ivar_df['Filename'].str.replace("_t01","") #this wont work for everyone as only my lab adds _ivar to file names, prior to pangolin
    pango_res_merge = pd.merge(pango_df, ivar_df, left_on='name', right_on='Filename').fillna('-')
    pango_res_merge.drop(drop_columns_pango, axis = 1, inplace = True)
    pango_res_merge=pango_res_merge.reindex(columns=neworder_ivar_pango)
    
    return pango_res_merge

def generate_snpprofile(file, database, pango, outfile):
    # print as separate file for easy manual checking.
    snpprofile = pd.DataFrame(ivar_pango(file, database, pango))
    snpprofile.to_csv(outfile, sep='\t', index = False)
    
    #send to pull_resistance
    return snpprofile


def generate_snpprofile_xpango(file, database, outfile):
    # print as separate file for easy manual checking.
    snpprofile = pd.DataFrame(resistance_addition(file, database))
    snpprofile.drop(drop_columns, axis = 1, inplace = True)
    snpprofile.to_csv(outfile, sep='\t', index = False)
    
    #send to pull_resistance
    return snpprofile
