#===============================================================================
# merge_sabres.py
# J.Draper 22 Aug 2022
#
# script to merge a bunch of individual sabres output files into one table
#

import argparse, pandas as pd

#initialise argument options & variables ---------------------------------------
argp = argparse.ArgumentParser(
                description='merge a bunch of individual sabres output files into one table',
                add_help=True)
argp.add_argument("--input", "-i", required=True, type=str, help="newline-separated list of sabres result files to merge")
argp.add_argument("--outfile","-o", required=True, type=str, help="name of merged file to write to")
args=argp.parse_args()

print("Launching merge_sabres.py on files in %s and writing to %s"%(args.input, args.outfile))

ret=pd.DataFrame()

with open(args.input, "r") as f:
    for fname in f:
        fname=fname.strip()
        print(fname)
        df = pd.read_csv(fname, sep="\t")
        ret = pd.concat([ret,df], axis=0, ignore_index=True)


ret.fillna("", inplace=True)
ret.to_csv(args.outfile,  sep="\t", index=False)

print("Done.")
