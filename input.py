import sys
import os
import pull_resistance

dirname = os.path.dirname(__file__)
database = os.path.join(dirname, "database/resistance_markers.txt")
file = sys.argv[1]
outfile = os.path.join(os.path.dirname(file), os.path.splitext(os.path.basename(file))[0] + '.snpprofile')

print(pull_resistance.get_resistance_only(file, database, outfile))


