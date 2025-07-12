# MIT License
#
# Copyright (c) 2025 ericsmacedo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Tests package against reference data."""

from pathlib import Path

import numpy as np
import pytest

from qformatpy import qformat as qfmt
from qformatpy._qformatpy import _rnd_array, _rnd_scalar

PRJ_PATH = Path(__file__).parent.parent


def parse_test_line(line):
    """Parse a line of test data into individual parameters."""
    parts = line.strip().split(", ")
    return {
        "x": float(parts[0]),
        "qi": int(parts[1]),
        "qf": int(parts[2]),
        "rnd_method": int(parts[3]),
        "ovf_method": int(parts[4]),
        "signed": parts[5] == "True",
        "expected": float(parts[6]),
    }


def pytest_generate_tests(metafunc):
    """Generate tests from test_data.txt."""
    if "test_case" in metafunc.fixturenames:
        test_file = PRJ_PATH / "tests" / "test_data.txt"
        lines = test_file.read_text().splitlines()[1:]  # Skip header
        test_cases = [parse_test_line(line) for line in lines if line.strip()]
        metafunc.parametrize("test_case", test_cases)


def test_qfmt_with_file_data(test_case):
    """Compares output of qfmt against test data."""
    result = qfmt(
        x=test_case["x"],  # Use dictionary keys
        qi=test_case["qi"],
        qf=test_case["qf"],
        rnd_method=test_case["rnd_method"],
        ovf_method=test_case["ovf_method"],
        signed=test_case["signed"],
    )
    assert result == test_case["expected"], f"Failed for test_case: {test_case}"


def test_overflow_error():
    """Test overflow error."""
    with pytest.raises(OverflowError):
        # Code that should raise OverflowError
        qfmt(x=512, qi=8, qf=0, ovf_method=2)


def test_overflow_error_array():
    """Test overflow error."""
    with pytest.raises(OverflowError):
        x = np.ones(100) * 1000
        # Code that should raise OverflowError
        qfmt(x=x, qi=8, qf=0, ovf_method=2)


def test_invalid_method_rnd_scalar():
    """Test invalid method error."""
    with pytest.raises(ValueError):
        # Code that should raise OverflowError
        _rnd_scalar(x=512, method=20)


def test_invalid_method_rnd_array():
    """Test invalid method error."""
    with pytest.raises(ValueError):
        # Code that should raise OverflowError
        _rnd_array(x=np.array([512]), method=20)
