from operator import ge
from webbrowser import get
import ivar_parse
import os

snpprofile = ivar_parse.generate_snpprofile
file = r"C:\Users\Winkie\Documents\21-R002-NT08Pr_t01.tsv"

def get_resistance_only(snpprofile, file):
    snpprofile['filename'] = os.path.splitext(os.path.basename(file))[0]
    interest_string = "Resistance"
    for item in snpprofile.split("/n"):
        if interest_string in item:
            print(item.strip())

print(get_resistance_only(snpprofile, file))

