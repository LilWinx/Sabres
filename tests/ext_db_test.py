import pytest
import os
import subprocess
import sys

data_dir = "tests/data/"
db_file = os.path.join(os.path.dirname(__file__), "data", "database", "full_resistance_markers.tsv")

@pytest.mark.parametrize(
    "vcall, input, database",
    [
        ("ivar", os.path.join(data_dir, "ivar"), db_file),
        ("varscan", os.path.join(data_dir, "varscan"), db_file),
        ("lofreq", os.path.join(data_dir, "lofreq"), db_file),
        ("fatovcf", os.path.join(data_dir, "fatovcf"), db_file),
        ("bcftools", os.path.join(data_dir, "bcftools"), db_file),
        ("shiver", os.path.join(data_dir, "shiver"), db_file),
        ("medaka", os.path.join(data_dir, "medaka", "testfile_medaka.vcf"), db_file),
    ],


)
def test_cli_db(vcall, input, database, out_dir):
    """
    test_cli_db
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
            "--database",
            database
        ],
        capture_output=True,
        check=True,
    )

    assert result.returncode == 0

    if vcall != "medaka" or vcall != "shiver":
        expected_files = [
            "bebtelovimab-res_snpprofile.tab",
            "molnupiravir-res_snpprofile.tab",
            "paxlovid-res_snpprofile.tab",
            "remdesivir-res_snpprofile.tab",
            "resistant_samples.tab",
            "sotrovimab-res_snpprofile.tab",
            "summary_counts.txt",
        ]

        for file in expected_files:
            output_file_path = os.path.join(out_dir, file)

        # check files exists
        assert os.path.isfile(output_file_path)
