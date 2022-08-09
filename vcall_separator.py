"""
Subscript of Sabres - performs a clean up of files all while extracting
samples in the script that contains resistance markers.
"""

import os
import pandas as pd
import add_resistance as ar
import add_lineage as al

output_csvs= []
def csv_export_pull_resistance(outname, dataframe_file):
    """
    generates the csv output "snpprofile" and extracts the resistant only lines
    """
    sep_outfile = os.path.join(outname + '.snpprofile')
    dataframe_file.to_csv(
            sep_outfile, sep='\t', index = False
        )
    if dataframe_file.empty is False:
        res_data = dataframe_file[dataframe_file['Interest'].str.contains('Resistance')]
        return res_data

def data_append(res_data):
    """
    Add all resistant lines to a list
    """
    if res_data is not None and res_data.empty is False:
        output_csvs.append(res_data)

def file_folder_loop(input_file, database, vcall, pango, pango_data):
    """
    Loop all the varscan and ivar files
    """
    if vcall == "varscan":
        for file in os.listdir(input_file):
            filename = os.path.join(input_file, os.fsdecode(file))
            outname = os.path.join(input_file, os.path.splitext(
                os.path.basename(file)
            )[0])
            if filename.endswith((".vcf")) and os.stat(filename).st_size != 0 and pango is not True:
                varscan_file = ar.resistance_addition(filename, database, vcall, 'None')
                res_data = csv_export_pull_resistance(outname, varscan_file)
                data_append(res_data)
            elif filename.endswith((".vcf")) and os.stat(filename).st_size != 0 and pango is True:
                varscan_file = al.add_pango(filename, database, vcall, pango_data)
                res_data = csv_export_pull_resistance(outname, varscan_file)
                data_append(res_data)
    elif vcall == "ivar":
        for file in os.listdir(input_file):
            filename = os.path.join(input_file, os.fsdecode(file))
            outname = os.path.join(input_file, os.path.splitext(
                os.path.basename(file)
            )[0])
            if filename.endswith((".tsv")) and os.stat(filename).st_size != 0 and pango is not True:
                ivar_file = ar.resistance_addition(filename, database, vcall, 'None')
                res_data = csv_export_pull_resistance(outname, ivar_file)
                data_append(res_data)
            elif filename.endswith((".tsv")) and os.stat(filename).st_size != 0 and pango is True:
                ivar_file = al.add_pango(filename, database, vcall, pango_data)
                res_data = csv_export_pull_resistance(outname, ivar_file)
                data_append(res_data)
    return output_csvs

def format_resistance(input_file, database, vcall, pango, pango_data):
    """
    cleaning up the lines containing resistance markers
    """
    import_res_df = file_folder_loop(input_file, database, vcall, pango, pango_data)
    res_df = pd.concat(import_res_df)
    string = res_df.to_csv(index = False, sep = '\t')
    counts = str(res_df['Interest'].value_counts())

    ## list of all resistant isolates from the input folder
    with open((input_file) + '/resistant_isolates.txt', "w") as output:
        output.write(string.replace('\r\n', '\n'))

    ## list resistant markers and the number of isolates containing that marker
    with open((input_file) + '/summary_counts.txt', 'w') as summary:
        summary.write(counts.replace('Name: Interest, dtype: int64', ''))
        return res_df
