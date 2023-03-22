import pytest
import os
import subprocess

data_dir = "tests/data/"

@pytest.mark.parametrize(
    "options,expected",
    [
        (["--vcall"], "argument --vcall/-v: expected one argument"),
        ([], "the following arguments are required: --vcall/-v, --input/-i"),
        (["--vcall", "ivar"], "the following arguments are required: --input/-i"),
        (
            ["--vcall", "ivar", "--outdir", "outdir"],
            "the following arguments are required: --input/-i",
        ),
    ],
)

def test_missing_args(options, expected):
    # testing the exit of not applying an R2
    result = subprocess.run(["python3", "-m", "sabres"] + options, capture_output=True)

    # assert that capture output is matching the expected
    lines = result.stderr.splitlines()
    last_line = lines[-1]
    assert result.returncode == 2
    assert last_line == expected
