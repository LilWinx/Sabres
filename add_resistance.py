"""
Subscript of SABres to merge the resistance database per sample
"""

import pandas as pd
from varscan_parse import varscan_setup
from ivar_parse import ivar_setup
from medaka_parse import medaka_setup

drop_columns = ['Nucleotide', 'Mutation']
strict_cols = ['Filename']
hotspots = [
    *range(10484,10487), # covers S144
    *range(10547,10553), # covers M165 and E166
    *range(10568,10571), # covers H172
    *range(10628,10631) # covers Q192
]

def vcall_selection(file, vcall, column):
    """
    makes the selection on what vcall was used and send to resistance_addition.
    """
    if vcall == 'ivar':
        preres_df = ivar_setup(file)
    elif vcall == 'varscan':
        preres_df  = varscan_setup(file)
    elif vcall == 'medaka':
        preres_df = medaka_setup(file, column)
    return preres_df

def resistance_addition(file, database, vcall, column):
    """
    merge the resistance database to the new dataframe
    &
    Nirmatrelvir has regions of resistance hotspots ∴ markers within these codons need to be marked with "hotspot"
    """
    preres_df = vcall_selection(file, vcall, column)
    if preres_df.empty is True:
        return preres_df

    ## adding the Confers column
    resistance_markers = pd.read_csv(
        database, sep='\t', header = 0
    )
    resdf = pd.DataFrame(resistance_markers)
    res_merge = pd.merge(
        preres_df, resdf, left_on='REFPOSALT', right_on='Mutation', how='left'
    ).fillna('-')
    res_merge.drop(drop_columns, axis = 1, inplace = True)
    remain_cols = [col for col in res_merge.columns if col not in strict_cols]
    res_clean = res_merge[strict_cols + remain_cols]

    ## adding the hotspots into the Confers column
    for hotspot in hotspots:
        res_clean.loc[(res_clean['POS'] == hotspot) & (res_clean['Confers'] == '-'), 'Confers'] = 'Nirmatrelvir (Paxlovid) Resistance Hotspot'
    return res_clean
