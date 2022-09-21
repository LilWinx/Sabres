#===============================================================================
# merge_sabres.py
# J.Draper 20 Sep 2022
#
# script to merge a bunch of individual sabres output files into one table
#

import argparse, os, pandas as pd

#initialise argument options & variables ---------------------------------------
argp = argparse.ArgumentParser(
                description='merge a bunch of individual sabres output files into one table',
                add_help=True)
argp.add_argument("--input", "-i", required=True, type=str, help="newline-separated list of sabres result files to merge")
argp.add_argument("--outfile","-o", required=True, type=str, help="name of merged file to write to")
argp.add_argument("--verbose","-v", action="store_true", help="verbose mode: print info about all files processed")
args=argp.parse_args()

print("Launching merge_sabres.py on files in %s and writing to %s"%(args.input, args.outfile))

ret=pd.DataFrame()

with open(args.input, "r") as f:
    for fname in f:

        fname = fname.strip()
        if not os.path.isfile(fname):
            if args.verbose:
                print(fname + ": FILE NOT FOUND")

        else:
            if os.path.getsize(fname) != 0:
                df = pd.read_csv(fname, sep="\t")
                if not df.empty:
                    if args.verbose:
                        print(fname + ": resistant mutations appended")
                    ret = pd.concat([ret, df], axis=0, ignore_index=True)
                elif args.verbose:
                    print(fname + ": empty file")
            elif args.verbose:
                print(fname + ": empty file")


ret.fillna("", inplace=True)
ret.to_csv(args.outfile, sep="\t", index=False)

print("Done.")
