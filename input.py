"""
Welcome to the primary script of Sabres
"""

import datetime
import os
import argparse
import pandas as pd
import pull_resistance
import pangolin_parse


# argparse
parser = argparse.ArgumentParser(description='Sabres')
parser.add_argument('--full', '-f', action='store_true', help='Use Full Database')
parser.add_argument('--lineage', '-l', help = 'Add Lineage Information')
parser.add_argument('input', help='Input file')
args = vars(parser.parse_args())

# database locations + time logs
dirname = os.path.dirname(__file__)
database = os.path.join(
    dirname, "database/resistance_markers.txt"
)
full_database = os.path.join(
    dirname, "database/full_resistance_markers.txt"
)
now = datetime.datetime.now()
time_log = now.strftime(
    "%Y-%m-%d %H:%M:%S"
    )

is_lineage = bool(args['lineage'] is not None)
db_selection = full_database if args['full'] else database

output_csvs= []

# generates the concatenated csv file from pangolin lineage
if is_lineage:
    pango = os.path.join(args['lineage'])
    pango_data = pangolin_parse.data_setup(pango)
    print(f"{time_log}: Pangolin Lineage file successfully generated")

# loop through all the files in the designated input folder
for file in os.listdir(args['input']):
    filename = os.path.join(args['input'], os.fsdecode(file))
    outfile = os.path.join(
        args['input'], os.path.splitext(os.path.basename(file))[0] + '.snpprofile'
    )
    if filename.endswith((".tsv", ".vcf")) and os.stat(filename).st_size != 0:
        if is_lineage:
            pango = os.path.join(
                args['lineage']
            )
            results = pull_resistance.get_res_pango(
                filename, db_selection, pango, outfile
            )
            if results is not None and results.empty is False:
                output_csvs.append(results)
        else:
            results =pull_resistance.get_res_xpango(filename, db_selection, outfile)
            if results is not None and results.empty is False:
                output_csvs.append(results)


# generate the summary files
res_df = pd.concat(output_csvs)
string = res_df.to_csv(index = False, sep = '\t')
counts = str(res_df['Interest'].value_counts())

## list of all resistant isolates from the input folder
with open((args['input']) + '/resistant_isolates.txt', "w") as output:
    output.write(string.replace('\r\n', '\n'))

## list resistant markers and the number of isolates containing that marker
with open((args['input']) + '/summary_counts.txt', 'w') as summary:
    summary.write(counts.replace('Name: Interest, dtype: int64', ''))
