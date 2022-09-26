"""
Subscript of Sabres to parse nanopore medaka .vcf outputs for resistance detection
Unfortunately, medaka does not provide frequency of the mutation, so the mutations
presented from this format would only show consensus level mutations.
"""

import os
import datetime
from io import StringIO
import pandas as pd
import sabres.add_resistance as ar
import sabres.add_lineage as al
import sabres.vcall_separator as vs

now = datetime.datetime.now()
time_log = now.strftime("%Y-%m-%d %H:%M:%S")

pd.set_option('display.max_rows', None)
output_csvs = []

def file_cleanup(input_file):
    """
    Remove the lines of the vcf file that contain the ##
    """
    with open(input_file, 'r') as vcf:
        oneline = ''
        lines = vcf.readlines()
        for line in lines:
            if not line.startswith('##'):
                oneline += line
        return oneline

def file2df(input_file):
    """
    Sets up the read of varscan vcf file without the seriously unnecessary hashes,
    also will print which file is being read for the log.
    """
    return pd.read_csv(StringIO(file_cleanup(input_file)), sep='\t', header = 0)

def splitting_vcf(input_file):
    """
    Clean up the Medaka dataframe so that it is easily read and extracted for file_folder loop.
    """
    vcf_df = pd.DataFrame(file2df(input_file))
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
    exploded_df = combined_df.assign(
        alt=combined_df.ALT.str.split(',')
    ).explode('alt').reset_index(drop=True)
    exploded_df['ALT'] = exploded_df['alt']
    exploded_df.drop(exploded_df.columns[len(exploded_df.columns)-1], axis=1, inplace=True)
    return exploded_df

def file_folder_loop(input_file, database, vcall, pango, pango_data, outdir):
    """
    Loop all the samples based on column.
    """
    import_df = splitting_vcf(input_file)
    for column in import_df.columns[9:]:
        outname = os.path.join(outdir, column)
        if pango is not True:
            medaka_file = ar.resistance_addition(input_file, database, vcall, column)
            res_data = vs.csv_export_pull_resistance(outname, medaka_file)
            data_append(res_data)
        else:
            medaka_file = al.add_pango(input_file, database, vcall, pango, pango_data)
            res_data = vs.csv_export_pull_resistance(outname, medaka_file)
            data_append(res_data)
    return output_csvs

def data_append(res_data):
    """
    Add all resistant lines to a list
    """
    if res_data is not None and res_data.empty is False:
        output_csvs.append(res_data)

def format_resistance(input_file, database, vcall, pango, pango_data, outdir):
    """
    cleaning up the lines containing resistance markers
    """
    import_res_df = file_folder_loop(input_file, database, vcall, pango, pango_data, outdir)
    res_df = pd.concat(import_res_df)
    string = res_df.to_csv(index = False, sep = '\t')
    counts = str(res_df['Confers'].value_counts())

    ## list of all resistant samples from the input folder
    with open("%s/resistant_samples.tab"%outdir, "w") as output:
        output.write(string.replace("\r\n", "\n"))

    ## list resistant markers and the number of samples containing that marker
    with open("%s/summary_counts.txt"%outdir, "w") as summary:
        summary.write(counts.replace("Name: Confers, dtype: int64", ""))
        return res_df
