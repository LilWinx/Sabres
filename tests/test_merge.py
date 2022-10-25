from dataclasses import dataclass
import os
from typing import List

from .utils import CLIRunner

merge_cli = CLIRunner(["/usr/local/bin/python3", "merge"])

def test_cli_merge(out_dir):
    "test_cli_merge"
    output_path = os.path.join(out_dir, "merge_out.tsv")
    out, err, code = merge_cli(
        ["--input", "tests/data/merge.txt", "--outfile", output_path]
    )

    assert code == 0
    assert 'Done' in out
    assert err == ''

    # check files exists
    assert os.path.isfile(output_path)

    # check output matches expected
    with open("tests/data/merge_out.tsv") as file:
        expected_lines = file.readlines()
    with open(output_path) as file:
        # check file contents match
        assert expected_lines == file.readlines()
