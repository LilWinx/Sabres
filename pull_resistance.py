import ivar_parse
import varscan_parse
import os
import pandas as pd

neworder_ivar = ['Filename', 'Lineage', 'REF', 'POS', 'ALT', 'REFPOSALT', 'TOTAL_DP', 'ALT_FREQ', 'REF_AA', 'ALT_AA', 'SNS', 'Protein', 'Interest', 'Note']
neworder_varscan = ['Filename', 'Lineage', 'REF', 'POS', 'ALT', 'REFPOSALT', 'HET', 'DP', 'FREQ', 'Protein', 'Interest', 'Note']

def format_resistance(filename, data):
    if filename.endswith(".tsv"):
        data = data.reindex(columns=neworder_ivar).fillna("-")
    elif filename.endswith(".vcf"):
        data = data.reindex(columns=neworder_varscan).fillna("-")
    if data.empty == False:
        data = data[data['Interest'].str.contains('Resistance')]
        return data

def get_res_xpango(filename, database, outfile):
    if filename.endswith(".tsv"):
        df = pd.DataFrame(ivar_parse.generate_snpprofile_xpango(filename, database, outfile))
    elif filename.endswith(".vcf"):
        df = pd.DataFrame(varscan_parse.generate_snpprofile_xpango(filename, database, outfile))
    else:
        raise Exception ("Incompatible Filetype")
    df['Filename'] = os.path.splitext(os.path.basename(filename))[0]
    return format_resistance(filename, df)

def get_res_pango(filename, database, pango, outfile):
    if filename.endswith(".tsv"):
        df = ivar_parse.generate_snpprofile(filename, database, pango, outfile)
    elif filename.endswith(".vcf"):
        df = varscan_parse.generate_snpprofile(filename, database, pango, outfile)
    else:
        raise Exception ("Incompatible Filetype")
    return format_resistance(filename, df)
