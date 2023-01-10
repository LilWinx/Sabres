"""
Utilised with --lineage flag
Subscript for Sabres that converts the pangolin folder to a concatenated file
Then turns the newly generated csv file into a readable dataframe
Written by Winkie Fong - winkie.fong@health.nsw.gov.au
"""
import os
import pandas as pd


pd.set_option("display.max_rows", None)
pd.options.mode.chained_assignment = None  # default='warn'


def data_setup(pango_data):
    """
    Takes the lineage_report.csv file that is genereated by Pangolin and concatenates them
    into a new file called pangolin_lineage.csv
    """
    pangolin_data = os.path.join(pango_data, "pangolin_lineage.csv")
    pango_line = ""
    for root, dirs, files in os.walk(pango_data, "."):
        for folder in dirs:
            dig_for_file = os.path.join(pango_data, folder + "/lineage_report.csv")
            with open(dig_for_file, "r") as lineage_csv:
                with open(pangolin_data, "w") as combined_csv:
                    last_line = lineage_csv.readlines()[-1]
                    pango_line += last_line
                    combined_csv.write(pango_line)


def lineage_addition(pango_data):
    """
    Converts the pangolin_lineage.csv into a dataframe for ivar_parse and varscan_parse
    """
    pangolin_data = os.path.join(pango_data, "pangolin_lineage.csv")
    lineage_df = pd.read_csv(pangolin_data, sep=",", header=None)
    filt_lin_df = lineage_df.iloc[:, [0, 1]]
    filt_lin_df.columns = ["name", "Lineage"]
    filt_lin_df["name"] = filt_lin_df["name"].str.replace("_ivar", "")
    return filt_lin_df
