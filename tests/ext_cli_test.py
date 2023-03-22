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
        ("medaka", os.path.join(data_dir, "medaka", "testfile_medaka.vcf")),
    ],
)

def test_cli(vcall, input, out_dir):
    """
    test_cli
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