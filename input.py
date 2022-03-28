import sys
import os
import pull_resistance
import argparse

parser = argparse.ArgumentParser(description='covid_res')
parser.add_argument('--full', '-f', action='store_true', help='Use Full Database')
parser.add_argument('input', help='Input file')
args = vars(parser.parse_args())

dirname = os.path.dirname(__file__)
database = os.path.join(dirname, "database/resistance_markers.txt")
full_database = os.path.join(dirname, "database/full_resistance_markers.txt")

sys.stdout = open((args['input']) + '/resistant_isolates.txt', "w")
for file in os.listdir(args['input']):
    filename = os.path.join(args['input'], os.fsdecode(file))
    outfile = os.path.join(args['input'], os.path.splitext(os.path.basename(file))[0] + '.snpprofile')
    if filename.endswith(".tsv"):
        if args['full']:
            results = pull_resistance.get_resistance_only(filename, full_database, outfile)
            if results:
                print(results)
        else:
            results = pull_resistance.get_resistance_only(filename, database, outfile)
            if results:
                print(results)
