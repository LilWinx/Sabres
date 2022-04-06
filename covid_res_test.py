import os
import unittest
import pull_resistance

dirname = os.path.dirname(__file__)
database = os.path.join(dirname, "database/resistance_markers.txt")
tsv = os.path.join(dirname, "database/covid_res_test.tsv")
nil_tsv = os.path.join(dirname, "database/covid_res_test_nil.tsv")
outfile = os.path.join(
    os.path.dirname(tsv), os.path.splitext(os.path.basename(tsv))[0] + ".snpprofile"
)


class TestCovidRes(unittest.TestCase):
    def covid_res_test(self):
        result = pull_resistance.get_resistance_only(tsv, database, outfile)
        self.assertEqual(
            result,
            "covid_res_test  A  22581  C  A22581C  2680  1.0  E  A  NS  S:E340A  A22581C  Sotromivab Resistance (>100-fold) - Manual Confirmation Required",
        )

    def empty_test(self):
        result = pull_resistance.get_resistance_only(tsv, database, outfile)
        self.assertEqual(result, "")
