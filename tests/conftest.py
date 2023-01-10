import tempfile
import pytest

"""
Written by @Wytamma
"""


@pytest.fixture()
def out_dir():
    "conftest"
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir
