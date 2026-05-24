"""Smoke tests for the pystatsinsurance package skeleton."""

import re

import pystatsinsurance


def test_version_is_semver():
    assert isinstance(pystatsinsurance.__version__, str)
    assert re.match(r"^\d+\.\d+\.\d+", pystatsinsurance.__version__)


def test_maintainer_metadata():
    assert pystatsinsurance.__author__ == "Hai-Shuo"
    assert pystatsinsurance.__email__ == "contact@sgcx.org"
