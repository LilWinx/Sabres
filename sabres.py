"""
Welcome to the primary script of Sabres
"""

import datetime
import os
import sys
import argparse
import pangolin_parse as pp
import vcall_separator as vs
import medaka_cleanup as mc


__version__ = "1.1.0"

# argparse
parser = argparse.ArgumentParser(description="Sabres")
parser.add_argument("--full", "-f", action="store_true", help="Use Full Database")
parser.add_argument("--lineage", "-l", help="Add Lineage Information")
parser.add_argument(
    "--vcall",
    "-v",
    choices=["ivar", "varscan", "medaka"],
    required=True,
    help="Specify variant caller software used",
)
parser.add_argument("--outdir", "-o", help="Output directory to write to")
parser.add_argument("--input", "-i", help="Input directory or file")
parser.add_argument(
    "--version",
    action="version",
    help="get SABRes version",
    version="SABRes v%s" % __version__,
)
args = vars(parser.parse_args())

# ensure medaka input is a single file not a directory
if args["vcall"] == "medaka" and not os.path.isfile(args["input"]):
    print('FATAL ERROR: using --vcall "medaka" but --input is not a file.')
    sys.exit()

# if outdir wasn't specified, set outdir to dir of input file
if not args["outdir"]:
    indir = os.path.dirname(args["input"])
    if indir == "":
        args["outdir"] = "."
    else:
        args["outdir"] = indir

print(
    "Launching Sabres v%s with variant caller %s on %s and writing output files to directory %s"
    % (__version__, args["vcall"], args["input"], args["outdir"])
)

# database locations + time logs
dirname = os.path.dirname(__file__)
database = os.path.join(dirname, "database/resistance_markers.tsv")
full_database = os.path.join(dirname, "database/full_resistance_markers.tsv")
now = datetime.datetime.now()
time_log = now.strftime("%Y-%m-%d %H:%M:%S")

is_lineage = bool(args["lineage"] is not None)

db_selection = full_database if args["full"] else database

if is_lineage:
    pango = os.path.join(args["lineage"])
    pango_data = pp.data_setup(pango)
    print(f"{time_log}: Pangolin Lineage file successfully generated")

if args["vcall"] == "medaka":
    mc.format_resistance(
        args["input"],
        database,
        args["vcall"],
        is_lineage,
        args["lineage"],
        args["outdir"],
    )

if args["vcall"] in ["ivar", "varscan"]:
    vs.format_resistance(
        args["input"],
        database,
        args["vcall"],
        is_lineage,
        args["lineage"],
        args["outdir"],
    )
