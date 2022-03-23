import pandas as pd
import numpy as np

def generate_snpprofile(file, database, outfile):
    data = pd.read_csv(file, sep='\t', header = 0)
    resistance_markers = pd.read_csv(database, sep='\t', header = 0)
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame(data)
    resdf = pd.DataFrame(resistance_markers)
    df.drop(['REGION', 'REF_DP', 'REF_RV', 'REF_QUAL', 'ALT_RV', 'ALT_QUAL', 'GFF_FEATURE', 'REF_CODON', 'ALT_CODON', 'PVAL', 'PASS'], axis = 1, inplace = True)
    df['REFPOSALT'] = df['REF'] + df['POS'].astype(str) + df['ALT']
    neworder = ['REF', 'POS', 'ALT', 'REFPOSALT', 'TOTAL_DP', 'ALT_FREQ']
    df=df.reindex(columns=neworder)
    dfsns = pd.DataFrame(data)
    dfsns = dfsns[['POS','REF_AA', 'ALT_AA']] 
    conditions = [
        (dfsns['REF_AA'] == "NA") & (dfsns['ALT_AA'] == "NA"),
        (dfsns['REF_AA'] == dfsns['ALT_AA'])
    ]
    choices = ('N/A', 'S')
    dfsns['SNS'] = np.select(conditions, choices, default='NS')
    dfmerge = pd.merge(df, dfsns, on='POS', how='left').fillna('-')
    lineage_merge = pd.merge(dfmerge, resdf, left_on='REFPOSALT', right_on='Mutation', how='left').fillna('-')
    lineage_merge.drop(['Nucleotide', 'Note'], axis = 1, inplace = True)
    lineage_merge.to_csv(outfile, sep='\t', index = False)
    return lineage_merge

#print(generate_snpprofile(file, database, outfile))