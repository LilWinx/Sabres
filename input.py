import sys
import os
import pull_resistance
import argparse

#file = sys.argv[1]

parser = argparse.ArgumentParser(description='covid_res')
parser.add_argument('--full', '-f', action='store_true', help='Use Full Database')
parser.add_argument('input', help='Input file')
args = vars(parser.parse_args())

dirname = os.path.dirname(__file__)
database = os.path.join(dirname, "database/resistance_markers.txt")
full_database = os.path.join(dirname, "database/full_resistance_markers.txt")
outfile = os.path.join(os.path.dirname(args['input']), os.path.splitext(os.path.basename(args['input']))[0] + '.snpprofile')

if args['full']:
	results = pull_resistance.get_resistance_only(args['input'], full_database, outfile)
	if results:
		print(results)
else:
    results = pull_resistance.get_resistance_only(args['input'], database, outfile)
    if results:
        print(results)