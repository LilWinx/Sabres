"""
Subscript of Sabres - performs a clean up of files all while extracting
samples in the script that contains resistance markers.
"""

import os
import pandas as pd
import re
import add_resistance as ar
import add_lineage as al


output_csvs = []


def csv_export_pull_resistance(outname, dataframe_file):
    """
    generates the csv output "snpprofile" and extracts the resistant only lines
    """

    sep_outfile = os.path.join(outname + "_snpprofile.tab")

    if dataframe_file.empty is False:
        res_data = dataframe_file[dataframe_file["Confers"].str.contains("Resistance")]
        if res_data.empty:
            res_data = dataframe_file[0:0]
        else:
            ## parse the resistance strings into separate columns
            res_parsed = res_data.apply(
                lambda x: split_resistance(x["Confers"]), axis=1, result_type="expand"
            )
            res_parsed = res_parsed.fillna("")
            res_data = pd.concat([res_data, res_parsed], axis=1)
    else:
        res_data = dataframe_file[0:0]

    dataframe_file.to_csv(sep_outfile, sep="\t", index=False) # outputs all SNPs found in the VCF for further checking of other SNPs in region.
    return res_data


def data_append(res_data):
    """
    Add all resistant lines to a list
    """
    if res_data is not None and res_data.empty is False:
        output_csvs.append(res_data)


def file_folder_loop(input_file, database, vcall, pango, pango_data, outdir):
    """
    Loop all the varscan and ivar files
    """
    if vcall == "varscan":
        for file in os.listdir(input_file):
            filename = os.path.join(input_file, os.fsdecode(file))
            outname = os.path.join(outdir, file)

            if (
                filename.endswith((".vcf"))
                and os.stat(filename).st_size != 0
                and pango is not True
            ):
                varscan_file = ar.resistance_addition(filename, database, vcall, "None")
                res_data = csv_export_pull_resistance(outname, varscan_file)
                data_append(res_data)
            elif (
                filename.endswith((".vcf"))
                and os.stat(filename).st_size != 0
                and pango is True
            ):
                varscan_file = al.add_pango(filename, database, vcall, pango_data)
                res_data = csv_export_pull_resistance(outname, varscan_file)
                data_append(res_data)
    elif vcall == "ivar":
        for file in os.listdir(input_file):

            filename = os.path.join(input_file, os.fsdecode(file))
            outname = os.path.join(outdir, file)

            if (
                filename.endswith((".tsv"))
                and os.stat(filename).st_size != 0
                and pango is not True
            ):
                ivar_file = ar.resistance_addition(filename, database, vcall, "None")
                res_data = csv_export_pull_resistance(outname, ivar_file)
                data_append(res_data)
            elif (
                filename.endswith((".tsv"))
                and os.stat(filename).st_size != 0
                and pango is True
            ):
                ivar_file = al.add_pango(filename, database, vcall, pango_data)
                res_data = csv_export_pull_resistance(outname, ivar_file)
                data_append(res_data)
    return output_csvs


def format_resistance(input_file, database, vcall, pango, pango_data, outdir):
    """
    cleaning up the lines containing resistance markers
    """

    res_df = pd.DataFrame
    import_res_df = file_folder_loop(
        input_file, database, vcall, pango, pango_data, outdir
    )
    if not import_res_df == []:
        res_df = pd.concat(import_res_df)
        string = res_df.to_csv(index=False, sep="\t")
        counts = str(res_df["Confers"].value_counts())
    else:
        string = ""
        counts = ""

    ## list of all resistant samples from the input folder
    with open("%s/resistant_samples.tab"%outdir, "w") as output:
        output.write(string.replace("\r\n", "\n"))

    ## list resistant markers and the number of samples containing that marker
    with open("%s/summary_counts.txt"%outdir, "w") as summary:
        summary.write(counts.replace("Name: Confers, dtype: int64", ""))

    return res_df


def split_resistance(s):
    """
    split the resistance list string into separate columns per marker/drug
    """
    ret_drugs = []
    ret_folds = []

    # replace all the separation point "," with ";" for easy splitting
    s = s.replace("), ", "); ")
    s = s.replace(") and ", "); ")
    s = s.replace("K, ", "K; ")
    s = s.replace("N, ", "N; ")
    s = s.replace("8, ", "8; ")
    s = s.replace("7.3, ", "7.3; ")
    s = s.replace("1, ", "1; ")

    s = s.split(";")
    for item in s:
        drug = item.partition("Resistance (")[0].strip()
        fold = item.partition("Resistance (")[2].partition(")")[0].strip()
        if fold == "":
            fold = "Y"
        ret_drugs.append(re.sub("^and | Resistance$", "", drug))
        ret_folds.append(fold)

    ret = pd.Series(ret_folds, index=ret_drugs)
    return ret
