"""
Subscript of Sabres to parse nanopore medaka .vcf outputs for resistance detection
Unfortunately, medaka does not provide frequency of the mutation, so the mutations presented from this format would only show consensus level mutations.
"""

import os
import datetime
import pandas as pd
from io import StringIO
import pangolin_parse as pp

#file = "/Users/winx/Documents/testfile_medaka.vcf"
file = "C:\\Users\\Winkie\\Documents\\testfile_medaka.vcf"
#outfile = "/Users/winx/Documents/testfile_medaka.snpprofile"
outfile = "C:\\Users\\Winkie\\Documents\\testfile_medaka.snpprofile"
database = "C:\\Users\\Winkie\\Documents\\full_resistance_markers.txt"
now = datetime.datetime.now()
time_log = now.strftime("%Y-%m-%d %H:%M:%S")

pd.set_option('display.max_rows', None)

def file_cleanup(file):
    """
    Remove the lines of the vcf file that contain the ##
    """
    with open(file, 'r') as vcf:
        oneline = ''
        lines = vcf.readlines()
        for line in lines:
            if not line.startswith('##'):
                oneline += line
        return oneline

def file2df(file):
    """
    Sets up the read of varscan vcf file without the seriously unnecessary hashes,
    also will print which file is being read for the log.
    """
    now = datetime.datetime.now()
    time_log = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_log}: Reading File - {file}")
    return pd.read_csv(StringIO(file_cleanup(file)), sep='\t', header = 0)

def splitting_vcf(file, database):
    vcf_df = pd.DataFrame(file2df(file))
    if vcf_df.empty:
        return vcf_df
    appended_data = []
    for column in vcf_df.columns[9:]:
        dynam_split = vcf_df[column].str.split(':', expand=True).add_prefix(column + '_')
        appended_data.append(dynam_split)
    appended_data = pd.concat(appended_data, axis = 1)
    combined_df = pd.concat([vcf_df.iloc[:, :9], appended_data], axis = 1)
    combined_df = combined_df[combined_df.columns.drop(list(combined_df.filter(regex='_1')))]
    combined_df.columns = combined_df.columns.str.rstrip("_0")
    exploded_df = combined_df.assign(alt=combined_df.ALT.str.split(',')).explode('alt').reset_index(drop=True)
    exploded_df['ALT'] = exploded_df['alt']
    exploded_df.drop(exploded_df.columns[len(exploded_df.columns)-1], axis=1, inplace=True)
    for column in exploded_df.columns[9:]:
        generate_snpprofile_pango(file, column, exploded_df, database)



def generate_snpprofile_pango(file, column, sample_df, database, pango):
    """
    #print as separate file for easy manual checking.
    """
    sep_outfile = os.path.join(os.path.dirname(file), column + '.snpprofile')
    snpprofile = gen_per_sample_add_res(column, sample_df, database)
    pango_df = pp.lineage_addition(pango)
    snpprofile['Lineage'] = snpprofile['Filename'].map(
        pango_df.drop_duplicates(
            subset=['name'], keep='first'
        ).set_index('name')['Lineage']
    ).fillna('-')
    if snpprofile.empty is True:
        return snpprofile
    snpprofile.to_csv(
            sep_outfile, sep='\t', index = False
        )

    print(f"{time_log}: Generating File - {column}.snpprofile")
    #send to pull_resistance
    return snpprofile

def generate_snpprofile_xpango(file, database, outfile):
    """
    #print as separate file for easy manual checking.
"""
    snpprofile = resistance_addition(file, database)
    if snpprofile.empty is True:
        return snpprofile
    snpprofile.drop(
        drop_columns, axis = 1, inplace = True
    )
    snp_csv = snpprofile.reindex(
        columns=neworder_varscan)
    snp_csv.to_csv(
        outfile, sep='\t', index = False
    )
    #send to pull_resistance
    return snpprofile

"""

print(splitting_vcf(file, database))