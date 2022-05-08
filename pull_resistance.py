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

def format_resistance(data, vcall):
    """
    cleaning up the lines containing resistance markers
    """
    if vcall == "ivar":
        data = data.reindex(
            columns=neworder_ivar
        ).fillna("-")
    elif vcall == "varscan":
        data = data.reindex(
            columns=neworder_varscan
        ).fillna("-")
    if data.empty is False:
        data = data[data['Interest'].str.contains('Resistance')]
        return data

def get_res_xpango(filename, database, outfile, vcall):
    """
    Checks filetypes and raises exceptions if filetype is incompatible
    """
    if vcall == "ivar":
        res_xpango_df = pd.DataFrame(
            ivar_parse.generate_snpprofile_xpango(
                filename, database, outfile
            )
        )
    elif vcall == "varscan":
        res_xpango_df = pd.DataFrame(
            varscan_parse.generate_snpprofile_xpango(
                filename, database, outfile
            )
        )
    else:
        raise Exception ("Incompatible Variant Caller")
    res_xpango_df['Filename'] = os.path.splitext(
        os.path.basename(
            filename
        )
    )[0]
    return format_resistance(res_xpango_df, vcall)

def get_res_pango(filename, database, pango, outfile, vcall):
    """
    If --pangolin flag is used
    Checks filetypes and raises exceptions if filetype is incompatible
    """
    if vcall == "ivar":
        res_pango_df = ivar_parse.generate_snpprofile(
            filename, database, pango, outfile
        )
    elif vcall == "varscan":
        res_pango_df = varscan_parse.generate_snpprofile(
            filename, database, pango, outfile
        )
    else:
        raise Exception ("Incompatible Variant Caller")
    return format_resistance(res_pango_df, vcall)
