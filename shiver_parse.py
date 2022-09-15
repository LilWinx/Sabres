"""
Subscript of Sabres to parse lofreq .vcf outputs for resistance detection
"""

import os
import datetime
from io import StringIO
import pandas as pd

pd.set_option('display.max_rows', None)

def file2df(file):
    """
    Sets up the read of shiver csv file, also will print which file is being read for the log.
    """
    now = datetime.datetime.now()
    time_log = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_log}: Reading File - {file}")
    return pd.read_csv(file, sep =',', header = 0)

def shiver_conversion(file):
    """
    convert shiver csv to vcf style file
    """
    csv_df = pd.DataFrame(file2df(file))
    csv_df.columns = ['POS', 'REF', 'A', 'C', 'G', 'T', 'Gap', 'N'] # completely replace the column names

#    for index, row in csv_df.iterrows():
#        if row['A'] > 0 and row['REF'] is not 'A':
            





def shiver_setup(file):
    vcf_df