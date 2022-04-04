import sys
import os
import pull_resistance
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='covid_res')
parser.add_argument('--full', '-f', action='store_true', help='Use Full Database')
parser.add_argument('--lineage', '-l', help = 'Add Lineage Information')
parser.add_argument('input', help='Input file')
args = vars(parser.parse_args())

dirname = os.path.dirname(__file__)
database = os.path.join(dirname, "database/resistance_markers.txt")
full_database = os.path.join(dirname, "database/full_resistance_markers.txt")

is_lineage = bool(args['lineage'] != None)
db_selection = full_database if args['full'] else database

output_csvs= []

for file in os.listdir(args['input']):
    filename = os.path.join(args['input'], os.fsdecode(file))
    outfile = os.path.join(args['input'], os.path.splitext(os.path.basename(file))[0] + '.snpprofile')
    if filename.endswith((".snpprofile", ".txt")) or filename == ".DS_Store":
        continue
    if is_lineage:
        pango = os.path.join(args['lineage']) #returns /Users/winx/Documents/pangolin_testdir
        results = pull_resistance.get_res_pango(filename, db_selection, pango, outfile)
        if results is not None and results.empty == False:
            output_csvs.append(results)
    else:
        results =pull_resistance.get_res_xpango(filename, db_selection, outfile)
        if results is not None and results.empty == False:
            output_csvs.append(results)


res_df = pd.concat(output_csvs)
string = res_df.to_csv(index = False, sep = '\t')
counts = str(res_df['Interest'].value_counts())

with open((args['input']) + '/resistant_isolates.txt', "w") as output:
    output.write(string.replace('\r\n', '\n'))

with open((args['input']) + '/summary_counts.txt', 'w') as summary:
    summary.write(counts.replace('Name: Interest, dtype: int64', ''))
