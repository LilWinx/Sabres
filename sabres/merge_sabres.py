# ===============================================================================
# merge_sabres.py
# J.Draper 20 Sep 2022
#
# script to merge a bunch of individual sabres output files into one table
#

import os, pandas as pd


def merge(input, outfile, verbose=False):
    print(
        "Launching merge_sabres.py on files in %s and writing to %s" % (input, outfile)
    )

    ret = pd.DataFrame()

    with open(input, "r") as f:
        for fname in f:

            fname = fname.strip()
            if not os.path.isfile(fname):
                if verbose:
                    print(fname + ": FILE NOT FOUND")

            else:
                if os.path.getsize(fname) != 0:
                    df = pd.read_csv(fname, sep="\t")
                    if not df.empty:
                        if verbose:
                            print(fname + ": resistant mutations appended")
                        ret = pd.concat([ret, df], axis=0, ignore_index=True)
                    elif verbose:
                        print(fname + ": empty file")
                elif verbose:
                    print(fname + ": empty file")

    ret.fillna("", inplace=True)
    ret.to_csv(outfile, sep="\t", index=False)

    print("Done.")
