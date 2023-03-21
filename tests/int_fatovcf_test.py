import pytest
import os
import sabres.parsers.fatovcf_parse as fp
import pandas as pd
import pandas.testing as pdt

data_dir = "tests/data/fatovcf/"

@pytest.mark.parametrize(
    "input, expected",
    [
        (
            "bebtelomivab-res.vcf",
            "bebtelomivab-res.snpprofile",
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
def test_fatovcf_parser(input, expected):
    shouldbe = pd.read_csv(os.path.join(data_dir, expected), sep="\t", header=0)
    result = fp.fatovcf_setup(os.path.join(data_dir, input))
    pdt.assert_frame_equal(result, shouldbe)
