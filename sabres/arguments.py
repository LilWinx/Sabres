import argparse

__version__ = "1.2.2"


def create_parser():
    parser = argparse.ArgumentParser(description="Sabres", prog="Sabres")

    # sabres
    parser.add_argument("--full", "-f", action="store_true", help="Use Full Database")
    parser.add_argument("--lineage", "-l", help="Add Lineage Information")
    parser.add_argument(
        "--vcall",
        "-v",
        choices=[
            "ivar",
            "varscan",
            "medaka",
            "lofreq",
            "shiver",
            "fatovcf",
            "bcftools",
        ],
        required=True,
        help="Specify variant caller software used",
    )
    parser.add_argument("--outdir", "-o", help="Output directory to write to")
    parser.add_argument("--input", "-i", help="Input directory or file", required=True)
    parser.add_argument(
        "--version",
        action="version",
        help="get SABRes version",
        version="SABRes v%s" % __version__,
    )
    parser.add_argument(
        "--merge",
        "-m",
        help="Merge a bunch of individual sabres output files into one table",
    )
    return parser
