import os
from pathlib import Path
from sabres.cli import main
from sabres import merge_sabres
import pytest



@pytest.mark.parametrize(
    "options,expected", 
    [
        (["--help"], "show this help message and exit"),
        (["-h"], "show this help message and exit"),
        (["--version"], "SABRes v"),
])
def test_helpers(capsys, options, expected):
    try:
        main(options)
    except SystemExit:
        pass
    
    result = capsys.readouterr().out
    assert expected in result


@pytest.mark.parametrize(
    "options,expected", 
    [
        (["--vcall"], "argument --vcall/-v: expected one argument"),
        ([], "the following arguments are required: --vcall/-v, --input/-i"),
        (["--vcall", "ivar"], "the following arguments are required: --input/-i"),
        (["--vcall", "ivar", "--outdir", 'outdir'], "the following arguments are required: --input/-i"),
])
def test_missing_args(capsys, options, expected):
    try:
        main(options)
    except SystemExit:
        pass
    result = capsys.readouterr().err
    assert expected in result


@pytest.fixture()
def out_dir(OUTDIR = 'tests/outdir/'):
    try:
        os.mkdir(OUTDIR)
    except FileExistsError:
        pass
    yield OUTDIR
    for file in os.listdir(OUTDIR):
        os.remove(OUTDIR + file)
    os.rmdir(OUTDIR)


def test_cli_ivar(out_dir, data_dir = "tests/data/"):

    main(["--vcall", "ivar", "--outdir", out_dir, "--input", data_dir])

    expected_files = [
        "covid_res_test_nil_snpprofile.tab", 
        "covid_res_test_snpprofile.tab", 
        "resistant_samples.tab",
        "summary_counts.txt",
    ]

    for file in expected_files:
        # check files exists
        assert Path(out_dir + file).exists
        
        with open(data_dir + file) as f:
            expected_lines = f.readlines()
        with open(out_dir + file) as f:
            # check file contents match
            assert expected_lines == f.readlines()


def test_cli_merge(out_dir, merge_file = "tests/data/merge.txt"):

    output = f"{out_dir}/merge_out.tsv"


    main(["merge", "--input", merge_file, "--outfile", output])
    # merge_sabres.merge(input=merge_file, outfile=output)

    # check files exists
    assert Path(output).exists
    
    with open("tests/data/merge_out.tsv") as f:
        expected_lines = f.readlines()
    with open(output) as f:
        # check file contents match
        assert expected_lines == f.readlines()