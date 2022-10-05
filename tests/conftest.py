import tempfile
import pytest


@pytest.fixture()
def out_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir
