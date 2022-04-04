import os
import pandas as pd
import numpy as np
from io import StringIO

pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'

def data_setup(pango_data):
    pangolin_data = os.path.join(pango_data, 'pangolin_lineage.csv')
    pango_line = ''
    for root, dirs, files in os.walk(pango_data, "."):
        for folder in dirs:
            dig_for_file = os.path.join(pango_data, folder + '/lineage_report.csv')
            with open(dig_for_file, 'r') as lineage_csv:
                with open(pangolin_data, 'w') as combined_csv:
                    last_line = lineage_csv.readlines()[-1]
                    pango_line += last_line
                    combined_csv.write(pango_line)
        return pango_line

def lineage_addition(pango_data):
    lineage_df = pd.read_csv(StringIO(data_setup(pango_data)), sep=',', header = None)
    filt_lin_df = lineage_df.iloc[:, [0,1]]
    filt_lin_df.columns = ['name', 'Lineage']
    filt_lin_df['name'] = filt_lin_df['name'].str.replace("_ivar","") #this wont work for everyone as only my lab adds _ivar to file names, prior to pangolin
    return filt_lin_df

