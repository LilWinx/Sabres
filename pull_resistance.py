"""
Subscript of Sabres - performs a clean up of files all while extracting
samples in the script that contains resistance markers.
"""
import os
import pandas as pd
import ivar_parse
import varscan_parse

neworder_ivar = [
    'Filename',
    'Lineage',
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
neworder_varscan = [
    'Filename',
    'Lineage',
    'REF',
    'POS',
    'ALT',
    'REFPOSALT',
    'HET',
    'DP',
    'FREQ',
    'Protein',
    'Interest',
    'Note'
]

def format_resistance(filename, data):
    """
    cleaning up the lines containing resistance markers
    """
    if filename.endswith(".tsv"):
        data = data.reindex(
            columns=neworder_ivar
        ).fillna("-")
    elif filename.endswith(".vcf"):
        data = data.reindex(
            columns=neworder_varscan
        ).fillna("-")
    if data.empty is False:
        data = data[data['Interest'].str.contains('Resistance')]
        return data

def get_res_xpango(filename, database, outfile):
    """
    Checks filetypes and raises exceptions if filetype is incompatible
    """
    if filename.endswith(".tsv"):
        res_xpango_df = pd.DataFrame(
            ivar_parse.generate_snpprofile_xpango(
                filename, database, outfile
            )
        )
    elif filename.endswith(".vcf"):
        res_xpango_df = pd.DataFrame(
            varscan_parse.generate_snpprofile_xpango(
                filename, database, outfile
            )
        )
    else:
        raise Exception ("Incompatible Filetype")
    res_xpango_df['Filename'] = os.path.splitext(
        os.path.basename(
            filename
        )
    )[0]
    return format_resistance(filename, res_xpango_df)

def get_res_pango(filename, database, pango, outfile):
    """
    If --pangolin flag is used
    Checks filetypes and raises exceptions if filetype is incompatible
    """
    if filename.endswith(".tsv"):
        res_pango_df = ivar_parse.generate_snpprofile(
            filename, database, pango, outfile
        )
    elif filename.endswith(".vcf"):
        res_pango_df = varscan_parse.generate_snpprofile(
            filename, database, pango, outfile
        )
    else:
        raise Exception ("Incompatible Filetype")
    return format_resistance(filename, res_pango_df)
