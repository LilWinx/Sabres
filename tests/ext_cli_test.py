import pytest
import os
import subprocess
import sys

data_dir = "tests/data/"

@pytest.mark.parametrize(
    "vcall, input",
    [
        ("ivar", os.path.join(data_dir, "ivar")),
        ("varscan", os.path.join(data_dir, "varscan")),
        ("lofreq", os.path.join(data_dir, "lofreq")),
        ("fatovcf", os.path.join(data_dir, "fatovcf")),
        ("bcftools", os.path.join(data_dir, "bcftools")),
        ("shiver", os.path.join(data_dir, "shiver")),
        ("medaka", os.path.join(data_dir, "medaka")),
    ],
)

def test_cli(vcall, input, out_dir):
    """
    test_cli_ivar
    """
    result = subprocess.run(
        [
            "python",
            "-m",
            "sabres",
            "--vcall",
            vcall,
            "--input",
            input,
            "--outdir",
            out_dir,
        ],
        capture_output=True,
        check = True
    )

    assert result.returncode == 0