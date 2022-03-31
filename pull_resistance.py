import ivar_parse
import varscan_parse
import os
import pandas as pd

neworder_ivar = ['Filename', 'REF', 'POS', 'ALT', 'REFPOSALT', 'TOTAL_DP', 'ALT_FREQ', 'REF_AA', 'ALT_AA', 'SNS', 'Protein', 'Interest', 'Note']
neworder_varscan = ['Filename', 'REF', 'POS', 'ALT', 'REFPOSALT', 'HET', 'DP', 'FREQ', 'Protein', 'Interest', 'Note']


def get_resistance_ivar(file, database, outfile):
    ivar_df = pd.DataFrame(ivar_parse.generate_snpprofile_xpango(file, database, outfile))
    ivar_df['Filename'] = os.path.splitext(os.path.basename(file))[0]
    ivar_df=ivar_df.reindex(columns=neworder_ivar)
    res_ivar_df = ivar_df[ivar_df['Interest'].str.contains('Resistance')]

    if res_ivar_df.empty == False:
        return res_ivar_df

def get_resistance_varscan(file, database, outfile):
    varscan_df = pd.DataFrame(varscan_parse.generate_snpprofile_xpango(file, database, outfile))
    varscan_df['Filename'] = os.path.splitext(os.path.basename(file))[0]
    varscan_df=varscan_df.reindex(columns=neworder_varscan)
    res_varscan_df = varscan_df[varscan_df['Interest'].str.contains('Resistance')]

    if res_varscan_df.empty == False:
        return res_varscan_df

def res_ivar_pango(file, database, pango, outfile):
    ivar_pango_df = pd.DataFrame(ivar_parse.generate_snpprofile(file, database, pango, outfile))
    res_ivar_pango_df = ivar_pango_df[ivar_pango_df['Interest'].str.contains('Resistance')]
    
    if res_ivar_pango_df.empty == False:
        return res_ivar_pango_df

def res_varscan_pango(file, database, pango, outfile):
    ivar_pango_df = pd.DataFrame(varscan_parse.generate_snpprofile(file, database, pango, outfile))
    res_ivar_pango_df = ivar_pango_df[ivar_pango_df['Interest'].str.contains('Resistance')]
    
    if res_ivar_pango_df.empty == False:
        return res_ivar_pango_df




