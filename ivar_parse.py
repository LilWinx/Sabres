import pandas as pd
import numpy as np

ignored_columns = ['REGION', 'REF_DP', 'REF_RV', 'REF_QUAL', 'ALT_RV', 'ALT_QUAL', 'GFF_FEATURE', 'REF_CODON', 'ALT_CODON', 'PVAL', 'PASS']
neworder = ['REF', 'POS', 'ALT', 'REFPOSALT', 'TOTAL_DP', 'ALT_FREQ']
choices = ('N/A', 'S')
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
    res_merge.drop(['Nucleotide'], axis = 1, inplace = True)
    return res_merge

def generate_snpprofile(file, database, outfile):
    # print as separate file for easy manual checking.
    snpprofile = pd.DataFrame(resistance_addition(file, database))
    snpprofile.to_csv(outfile, sep='\t', index = False)
    
    #send to pull_resistance
    return snpprofile