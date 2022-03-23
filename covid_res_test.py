import unittest
import ivar_parse

class TestSum(unittest.TestCase):
    def test(self):
        result = ivar_parse.generate_snpprofile(tsv, database, snpprofile)
        self.assertEqual(result, "string")