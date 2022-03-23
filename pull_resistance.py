import ivar_parse
import os
import pandas as pd
import numpy as np

#file = r"C:\Users\Winkie\Documents\21-R002-NT08Pr_t01.tsv"
file = '/Users/winx/Documents/21-R002-NT08Pr_t01.tsv'
#database = r"C:\Users\Winkie\Documents\resistance_markers.txt"
database = '/Users/winx/Documents/resistance_markers.txt'
#outfile = r"C:\Users\Winkie\Documents\21-R002-NT08Pr_t01.snpprofile"
outfile = '/Users/winx/Documents/21-R002-NT08Pr_t01.snpprofile'

def get_resistance_only(file, database, outfile):
    snpprofile_df = pd.DataFrame(ivar_parse.generate_snpprofile(file, database, outfile))
    snpprofile_df['filename'] = os.path.splitext(os.path.basename(file))[0]
    neworder = ['filename', 'REF', 'POS', 'ALT', 'REFPOSALT', 'TOTAL_DP', 'ALT_FREQ', 'REF_AA', 'ALT_AA', 'SNS', 'Protein', 'Mutation', 'Interest']
    snpprofile_df=snpprofile_df.reindex(columns=neworder)
    resistance_df = snpprofile_df[snpprofile_df['Interest'].str.contains('Resistance')]
    return resistance_df.to_string(index = False, header = False)

