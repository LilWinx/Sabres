"""
Welcome to the primary script of Sabres
Written by Winkie Fong - winkie.fong@health.nsw.gov.au
"""

import datetime
import os
import sys
import argparse
import logging
import warnings


from .parsers import pangolin_parse as pp
from . import medaka_cleanup as mc
from . import vcall_separator as vs
from sabres import arguments

__version__ = "1.2.2"

logging.getLogger().setLevel(logging.INFO)
warnings.simplefilter(action="ignore", category=FutureWarning)


def check_external_db(fp):
    headers = frozenset(["Protein", "Nucleotide", "Mutation", "Confers", "Evidence"])
    if not os.path.isfile(fp):
        logging.error(f"Database file specified {fp} does not appear to exist.")
        sys.exit(1)
    with open(fp, "r") as db:
        fline = set(db.readline().strip().split("\t"))
        if len(fline) != len(headers):
            logging.error(f"The database file: {fp} does not have the appropriate number of headers specified.")
            sys.exit(1)
        if headers != fline:
            logging.error(f"Database headers need to match {headers.join(' ')}")
            logging.error(f"Headers in user specified file: {fline.join(' ')} ")
            sys.exit(1)

    

def main():
    parser = arguments.create_parser()
    args = parser.parse_args()

    # ensure medaka input is a single file not a directory
    if args.vcall == "medaka" and not os.path.isfile(args.input):
        msg = 'FATAL ERROR: using --vcall "medaka" but --input is not a file.'
        logging.error(msg)
        sys.exit(1)

    # if outdir wasn't specified, set outdir to dir of input file
    if not args.outdir:
        indir = os.path.dirname(args.input)
        if indir == "":
            args.outdir = "."
        else:
            args.outdir = indir

    logging.info(
        "Launching Sabres v%s with variant caller %s on %s and writing output files to directory %s"
        % (__version__, args.vcall, args.input, args.outdir)
    )

    # database locations + time logs
    dirname = os.path.dirname(__file__)

    database = os.path.join(dirname, "database/resistance_markers.tsv")
    full_database = os.path.join(dirname, "database/full_resistance_markers.tsv")
    now = datetime.datetime.now()
    time_log = now.strftime("%Y-%m-%d %H:%M:%S")

    is_lineage = bool(args.lineage is not None)
    if args.database is None:
        db_selection = full_database if args.full else database
    else:
        check_external_db(args.database)
        db_selection = args.database

    if is_lineage:
        pango = os.path.join(args.lineage)
        pp.data_setup(pango)
        logging.info(f"{time_log}: Pangolin Lineage file successfully generated")

    if args.vcall == "medaka":
        mc.format_resistance(
            args.input,
            db_selection,
            args.vcall,
            is_lineage,
            args.lineage,
            args.outdir,
        )

    if args.vcall in ["ivar", "varscan", "lofreq", "shiver", "fatovcf", "bcftools"]:
        vs.format_resistance(
            args.input,
            db_selection,
            args.vcall,
            is_lineage,
            args.lineage,
            args.outdir,
        )


if __name__ == "__main__":
    main()
