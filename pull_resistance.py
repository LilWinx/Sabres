import ivar_parse
import os
import pandas as pd
import numpy as np

neworder = ['filename', 'REF', 'POS', 'ALT', 'REFPOSALT', 'TOTAL_DP', 'ALT_FREQ', 'REF_AA', 'ALT_AA', 'SNS', 'Protein', 'Mutation', 'Interest']

def get_resistance_only(file, database, outfile):
    snpprofile_df = pd.DataFrame(ivar_parse.generate_snpprofile(file, database, outfile))
    snpprofile_df['filename'] = os.path.splitext(os.path.basename(file))[0]
    snpprofile_df=snpprofile_df.reindex(columns=neworder)
    resistance_df = snpprofile_df[snpprofile_df['Interest'].str.contains('Resistance')]
    if resistance_df.empty == False:
        return resistance_df.to_string(index = False, header = False)
