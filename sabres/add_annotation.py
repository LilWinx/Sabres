"""
Subscript of Sabres to add annotations of genes
Written by Winkie Fong - winkie.fong@health.nsw.gov.au
"""

import pandas as pd
import numpy as np

pd.set_option("display.max_rows", None)


def annotate(pre_df):
    genes = [
        "ORF1ab:NSP1",
        "ORF1ab:NSP2",
        "ORF1ab:NSP3",
        "ORF1ab:NSP4",
        "ORF1ab:NSP5",
        "ORF1ab:NSP6",
        "ORF1ab:NSP7",
        "ORF1ab:NSP8",
        "ORF1ab:NSP9",
        "ORF1ab:NSP10",
        "ORF1ab:NSP12",
        "ORF1ab:NSP13",
        "ORF1ab:NSP14",
        "ORF1ab:NSP15",
        "ORF1ab:NSP16",
        "S",
        "ORF3a",
        "E",
        "M",
        "ORF6",
        "ORF7a",
        "ORF7b",
        "ORF8",
        "N",
        "ORF10",
    ]
    conditions = [
        (pre_df["POS"] >= 266) & (pre_df["POS"] <= 805),  # ORF1ab:NSP1
        (pre_df["POS"] >= 806) & (pre_df["POS"] <= 2719),  # ORF1ab:NSP2
        (pre_df["POS"] >= 2720) & (pre_df["POS"] <= 8554),  # ORF1ab:NSP3
        (pre_df["POS"] >= 8555) & (pre_df["POS"] <= 10054),  # ORF1ab:NSP4
        (pre_df["POS"] >= 10055) & (pre_df["POS"] <= 10972),  # ORF1ab:NSP5
        (pre_df["POS"] >= 10973) & (pre_df["POS"] <= 11842),  # ORF1ab:NSP6
        (pre_df["POS"] >= 11843) & (pre_df["POS"] <= 12091),  # ORF1ab:NSP7
        (pre_df["POS"] >= 12092) & (pre_df["POS"] <= 12685),  # ORF1ab:NSP8
        (pre_df["POS"] >= 12686) & (pre_df["POS"] <= 13024),  # ORF1ab:NSP9
        (pre_df["POS"] >= 13025) & (pre_df["POS"] <= 13441),  # ORF1ab:NSP10
        (pre_df["POS"] >= 13442) & (pre_df["POS"] <= 16236),  # ORF1ab:NSP12
        (pre_df["POS"] >= 16237) & (pre_df["POS"] <= 18039),  # ORF1ab:NSP13
        (pre_df["POS"] >= 18040) & (pre_df["POS"] <= 19620),  # ORF1ab:NSP14
        (pre_df["POS"] >= 19621) & (pre_df["POS"] <= 20658),  # ORF1ab:NSP15
        (pre_df["POS"] >= 20659) & (pre_df["POS"] <= 21552),  # ORF1ab:NSP16
        (pre_df["POS"] >= 21563) & (pre_df["POS"] <= 25384),  # S
        (pre_df["POS"] >= 25393) & (pre_df["POS"] <= 26220),  # ORF3a
        (pre_df["POS"] >= 26245) & (pre_df["POS"] <= 26472),  # E
        (pre_df["POS"] >= 26523) & (pre_df["POS"] <= 27191),  # M
        (pre_df["POS"] >= 27202) & (pre_df["POS"] <= 27387),  # ORF6
        (pre_df["POS"] >= 27394) & (pre_df["POS"] <= 27759),  # ORF7a
        (pre_df["POS"] >= 27756) & (pre_df["POS"] <= 27887),  # ORF7b
        (pre_df["POS"] >= 27894) & (pre_df["POS"] <= 28259),  # ORF8
        (pre_df["POS"] >= 28274) & (pre_df["POS"] <= 29533),  # N
        (pre_df["POS"] >= 29558) & (pre_df["POS"] <= 29674),  # ORF10
    ]
    pre_df["Gene/NSP"] = np.select(conditions, genes, default="Intergenic Region")
    return pre_df
