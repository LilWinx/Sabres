"""
Welcome to the primary script of Sabres
"""

import datetime
import os
import argparse
import pangolin_parse as pp
import vcall_separator as vs
import medaka_cleanup as mc

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
parser.add_argument("input", help="Input directory or file")
args = vars(parser.parse_args())

if not args["outdir"]:
    args["outdir"] = args["input"]

print(
    "Launching Sabres on %s files in directory %s and writing outdir files to directory %s"
    % (args["vcall"], args["input"], args["outdir"])
)

# database locations + time logs
dirname = os.path.dirname(__file__)
database = os.path.join(dirname, "database/resistance_markers.txt")
full_database = os.path.join(dirname, "database/full_resistance_markers.txt")
now = datetime.datetime.now()
time_log = now.strftime("%Y-%m-%d %H:%M:%S")

is_lineage = bool(args["lineage"] is not None)
is_medaka = bool(args["vcall"] == "medaka")  # if medaka is activated - this is true
db_selection = full_database if args["full"] else database

if is_lineage:
    pango = os.path.join(args["lineage"])
    pango_data = pp.data_setup(pango)
    print(f"{time_log}: Pangolin Lineage file successfully generated")

if is_medaka:
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
