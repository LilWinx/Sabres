import pytest
import os
import sabres.parsers.varscan_parse as vp
import pandas as pd
import pandas.testing as pdt

data_dir = "tests/data/varscan/"


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            "bebtelovimab-res.vcf",
            "bebtelovimab-res.snpprofile",
        ),
        (
            "molnupiravir-res.vcf",
            "molnupiravir-res.snpprofile",
        ),
        (
            "paxlovid-res.vcf",
            "paxlovid-res.snpprofile",
        ),
        (
            "remdesivir-res.vcf",
            "remdesivir-res.snpprofile",
        ),
        (
            "sotrovimab-res.vcf",
            "sotrovimab-res.snpprofile",
        ),
    ],
)
def test_varscan_parser(input, expected):
    shouldbe = pd.read_csv(os.path.join(data_dir, expected), sep="\t", header=0)
    result = vp.varscan_setup(os.path.join(data_dir, input))
    result = result.astype({"DP": "int64"})
    pdt.assert_frame_equal(result, shouldbe)
