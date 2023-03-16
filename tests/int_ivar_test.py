import pytest
import os
import sabres.parsers.ivar_parse as ip
import pandas as pd
import pandas.testing as pdt

data_dir = "tests/data/ivar/"

@pytest.mark.parametrize(
    "input, expected",
    [
        (
            "bebtelomivab-res.tsv",
            "bebtelomivab-res.snpprofile",
        ),
        (
            "molnupiravir-res.tsv",
            "molnupiravir-res.snpprofile",
        ),
        (
            "paxlovid-res.tsv",
            "paxlovid-res.snpprofile",
        ),
        (
            "remdesivir-res.tsv",
            "remdesivir-res.snpprofile",
        ),
        (
            "sotrovimab-res.tsv",
            "sotrovimab-res.snpprofile",
        ),
    ],
)
def test_ivar_parser(input, expected):
    shouldbe = pd.read_csv(os.path.join(data_dir, expected), sep="\t", header=0)
    result = ip.ivar_setup(os.path.join(data_dir, input))
    pdt.assert_frame_equal(result, shouldbe)
