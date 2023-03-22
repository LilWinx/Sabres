import pytest
import os
import subprocess

data_dir = "tests/data/"

@pytest.mark.parametrize(
    "options,expected",
    [
        (["--vcall"], "b'Sabres: error: argument --vcall/-v: expected one argument'"),
        ([], "b'Sabres: error: the following arguments are required: --vcall/-v, --input/-i'"),
        (["--vcall", "ivar"], "b'Sabres: error: the following arguments are required: --input/-i'"),
        (
            ["--vcall", "ivar", "--outdir", "outdir"],
            "b'Sabres: error: the following arguments are required: --input/-i'",
        ),
    ],
)

def test_missing_args(options, expected):
    result = subprocess.run(["python", "-m", "sabres"] + options, capture_output=True)

    # assert that capture output is matching the expected
    lines = result.stderr.splitlines()
    last_line = lines[-1]
    assert result.returncode == 2
    assert str(last_line) == expected
