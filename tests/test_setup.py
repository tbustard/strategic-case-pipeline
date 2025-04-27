"""Basic smoke test for setup.py."""

import importlib.util
import pathlib
import sys


def test_setup_import():
    """Test that setup.py can be imported."""
    spec = importlib.util.spec_from_file_location(
        "setup", pathlib.Path("src/case_context/setup.py")
    )
    setup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(setup)
    assert hasattr(setup, "__file__")  # basic smoke import
