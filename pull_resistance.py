import ivar_parse
import varscan_parse
import os
import pandas as pd

neworder_ivar = ['filename', 'REF', 'POS', 'ALT', 'REFPOSALT', 'TOTAL_DP', 'ALT_FREQ', 'REF_AA', 'ALT_AA', 'SNS', 'Protein', 'Mutation', 'Interest', 'Note']
neworder_varscan = ['filename', 'REF', 'POS', 'ALT', 'REFPOSALT', 'HET', 'DP', 'FREQ', 'Protein', 'Mutation', 'Interest', 'Note']
drop_columns = ['Mutation']
def get_resistance_ivar(file, database, outfile):
    ivar_df = pd.DataFrame(ivar_parse.generate_snpprofile(file, database, outfile))
    ivar_df['filename'] = os.path.splitext(os.path.basename(file))[0]
    ivar_df=ivar_df.reindex(columns=neworder_ivar)
    res_ivar_df = ivar_df[ivar_df['Interest'].str.contains('Resistance')]
    res_ivar_df.drop(drop_columns, axis = 1, inplace = True)

    if res_ivar_df.empty == False:
        return res_ivar_df

def get_resistance_varscan(file, database, outfile):
    varscan_df = pd.DataFrame(varscan_parse.generate_snpprofile(file, database, outfile))
    varscan_df['filename'] = os.path.splitext(os.path.basename(file))[0]
    varscan_df=varscan_df.reindex(columns=neworder_varscan)
    res_varscan_df = varscan_df[varscan_df['Interest'].str.contains('Resistance')]
    res_varscan_df.drop(drop_columns, axis = 1, inplace = True)

    if res_varscan_df.empty == False:
        return res_varscan_df