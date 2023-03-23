"""
Subscript of Sabres to parse BCFtools .vcf outputs for resistance detection
Written by Winkie Fong - winkie.fong@health.nsw.gov.au
"""

import os
import datetime
from io import StringIO
import pandas as pd
import logging

pd.set_option("display.max_rows", None)
neworder = ["Filename", "REF", "POS", "ALT", "REFPOSALT", "DP", "FREQ"]


def file_cleanup(file):
    """
    Remove the lines of the vcf file that contain the ##
    """
    with open(file, "r") as vcf:
        oneline = ""
        lines = vcf.readlines()
        for line in lines:
            if not line.startswith("##"):
                oneline += line
        return oneline


def file2df(file):
    """
    Sets up the read of varscan vcf file without the seriously unnecessary hashes,
    also will print which file is being read for the log.
    """
    now = datetime.datetime.now()
    time_log = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{time_log}: Reading File - {file}")
    return pd.read_csv(StringIO(file_cleanup(file)), sep="\t", header=0)


def bcftools_setup(file):
    """
    converting tsv to dataframe and begin removing unwanted columns
    generates new column called REFPOSALT
    """
    vcf_df = pd.DataFrame(file2df(file))
    if vcf_df.empty:
        return vcf_df

    # masking the INDEL rows
    # mask = vcf_df.apply(lambda x: x.astype(str).str.contains('INDEL')).any(axis=1)
    # filtered_df = vcf_df[~mask]

    # split the filtered dataframe by INFO
    info_data = vcf_df["INFO"].str.split(";", expand=True)

    # masking columns that don't contain DP
    mask2 = info_data.apply(lambda x: x.astype(str).str.contains("DP", na=False))
    dp_only_data = info_data[mask2].fillna("")

    # combining the dp only columns with the filtered dataframe
    combined_df = pd.concat([vcf_df, dp_only_data], axis=1)
    combined_df.drop(columns=["INFO"], inplace=True)

    # iterate over the original dataframe and extract the DP and DP4 values
    dp_df = pd.DataFrame(columns=["DP"])
    for index, row in combined_df.iterrows():
        dp_value = ""
        for col in row:
            if isinstance(col, str) and col.startswith("DP="):
                dp_value = col.split("=")[1]
        dp_df.loc[index] = [dp_value]

    dp4_df = pd.DataFrame(columns=["DP4"])
    for index, row in combined_df.iterrows():
        dp4_value = ""
        for col in row:
            if isinstance(col, str) and col.startswith("DP4="):
                dp4_value = col.split("=")[1]
        dp4_df.loc[index] = [dp4_value]

    # combine the dp and dp4 columns
    dp_dp4_df = pd.concat([dp_df, dp4_df], axis=1)

    # calculate the frequency of the alts
    dp_data = dp_dp4_df["DP4"].str.split(",", expand=True).add_prefix("DP4" + "_")
    dp_data["alt_sum"] = dp_data["DP4_2"].astype(int) + dp_data["DP4_3"].astype(int)
    combined_df = pd.concat([combined_df, dp_df, dp_data], axis=1)
    combined_df["FREQ"] = combined_df["alt_sum"].astype(int) / combined_df["DP"].astype(
        int
    )

    # add refposalt column
    combined_df["REFPOSALT"] = vcf_df["REF"] + vcf_df["POS"].astype(str) + vcf_df["ALT"]

    # add the file names
    combined_df["Filename"] = os.path.splitext(os.path.basename(file))[0]
    combined_df = combined_df.reindex(columns=neworder)
    return combined_df
