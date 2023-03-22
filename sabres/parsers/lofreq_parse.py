"""
Subscript of Sabres to parse lofreq .vcf outputs for resistance detection
Written by Winkie Fong - winkie.fong@health.nsw.gov.au
"""

import os
import datetime
from io import StringIO
import pandas as pd
import logging

pd.set_option("display.max_rows", None)
neworder = ["Filename", "REF", "POS", "ALT", "REFPOSALT", "DP", "AF"]


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


def lofreq_setup(file):
    """
    converting tsv to dataframe and begin removing unwanted columns
    generates new column called REFPOSALT
    """
    vcf_df = pd.DataFrame(file2df(file))
    if vcf_df.empty:
        return vcf_df
    vcf_df = vcf_df[["REF", "POS", "ALT", "INFO"]]
    vcf_df[["DP", "AF", "SB", "DP4"]] = vcf_df.INFO.str.split(";", expand=True)
    vcf_df["REFPOSALT"] = vcf_df["REF"] + vcf_df["POS"].astype(str) + vcf_df["ALT"]
    vcf_df["Filename"] = os.path.splitext(os.path.basename(file))[0]
    str_rm = "|".join([".MN908947.vcf"])
    vcf_df["Filename"] = vcf_df["Filename"].str.replace(str_rm, "")
    vcf_df[['DP', 'AF']] = vcf_df[['DP', 'AF']].apply(lambda x: x.str.replace('DP=', '').str.replace('AF=', ''))
    vcf_df = vcf_df.reindex(columns=neworder)
    return vcf_df
