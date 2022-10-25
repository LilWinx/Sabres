import os
from typing import List
import pytest

from .utils import CLIRunner

sabres_cli = CLIRunner(["/usr/local/bin/python3", "sabres"])

@pytest.mark.parametrize(
    "options,expected",
    [
        (["--vcall"], "argument --vcall/-v: expected one argument"),
        ([], "the following arguments are required: --vcall/-v, --input/-i"),
        (["--vcall", "ivar"], "the following arguments are required: --input/-i"),
        (["--vcall", "ivar", "--outdir", 'outdir'],
    "the following arguments are required: --input/-i"),
])

def test_missing_args(options, expected):
    out, err, code = sabres_cli(options)
    assert code == 2
    assert expected in err
    assert out == ''

def test_cli_ivar(out_dir):
    """
    test_cli_ivar
    """
    data_dir = "tests/data/"

    out, err, code = sabres_cli(["--vcall", "ivar", "--outdir", out_dir, "--input", data_dir])

    assert code == 0

    expected_files = [
        "covid_res_test_nil_snpprofile.tab",
        "covid_res_test_snpprofile.tab",
        "resistant_samples.tab",
        "summary_counts.txt",
    ]

    for file in expected_files:
        output_file_path = os.path.join(out_dir, file)
        expected_file_path = os.path.join(data_dir, file)

        # check files exists
        assert os.path.isfile(output_file_path)
        with open(expected_file_path) as expected_file:
            expected_lines = expected_file.readlines()
        with open(output_file_path) as output_file:
            # check file contents match
            assert expected_lines == output_file.readlines()
