import pytest
import os
import sabres.parsers.bcftools_parse as bp
import pandas as pd
import pandas.testing as pdt

data_dir = "tests/data/bcftools/"

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
def test_ivar_parser(input, expected):
    shouldbe = pd.read_csv(os.path.join(data_dir, expected), sep="\t", header=0)
    result = bp.bcftools_setup(os.path.join(data_dir, input))
    result = result.astype({"DP": int})
    pdt.assert_frame_equal(result, shouldbe)
