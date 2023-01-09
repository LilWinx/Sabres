"""
Subscript of SABRes to add Lineage column to dataframes should --lineage flag be called.
Written by Winkie Fong - winkie.fong@health.nsw.gov.au
"""

import os
from .parsers import pangolin_parse as pp
from . import add_resistance as ar

strict_cols = [
    'Filename',
    'Lineage',
    'REF',
    'POS',
    'ALT',
    'REFPOSALT'
]
def add_pango(file, database, vcall, pango_data):
    """
    if --pangolin was called, this is the function it runs.
    adds the lineage data from pangolin folder into the profile
    """
    pango_df = pp.lineage_addition(pango_data)
    res_df = ar.resistance_addition(file, database, vcall, 'None')
    if res_df.empty is True:
        return res_df
    res_df['Filename'] = os.path.splitext(
        os.path.basename(file)
    )[0]
    str_rm = '|'.join(['_t01', '_q20t01', '.varscan.snps'])
    res_df['Filename'] = res_df['Filename'].str.replace(
        str_rm, ''
    )
    res_df['Lineage'] = res_df['Filename'].map(
        pango_df.drop_duplicates(
            subset=['name'], keep='first'
        ).set_index('name')['Lineage']
    ).fillna('-')
    remain_cols = [col for col in res_df.columns if col not in strict_cols]
    pango_res_clean = res_df[strict_cols + remain_cols]
    return pango_res_clean
