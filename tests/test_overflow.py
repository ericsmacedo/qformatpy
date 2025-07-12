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
"""Tests qformatpy for different overflow methods."""

import pytest

from qformatpy import ERROR, SAT, TRUNC, WRAP
from qformatpy import qformat as qfmt

# Test cases for overflow behavior
# Each tuple contains: (input_value, qi, qf, signed, expected_result_or_exception)
OVERFLOW_TEST_CASES = [
    # Unsigned tests (signed=False)
    # WRAP behavior - should wrap around on overflow
    (16, 4, 0, False, WRAP, 0),  # 16 wraps to 0 in 4-bit unsigned
    (17, 4, 0, False, WRAP, 1),  # 17 wraps to 1
    (-1, 4, 0, False, WRAP, 15),  # -1 wraps to 15 (2's complement)
    # SAT behavior - should saturate at max/min values
    (16, 4, 0, False, SAT, 15),  # Saturates at 15 (max 4-bit unsigned)
    (-1, 4, 0, False, SAT, 0),  # Saturates at 0 (min unsigned)
    # ERROR behavior - should raise exception
    (16, 4, 0, False, ERROR, OverflowError),
    (-1, 4, 0, False, ERROR, OverflowError),
    # Signed tests (signed=True)
    # WRAP behavior
    (8, 4, 0, True, WRAP, -8),  # 8 wraps to -8 in 4-bit signed
    (-9, 4, 0, True, WRAP, 7),  # -9 wraps to 7
    # SAT behavior
    (8, 4, 0, True, SAT, 7),  # Saturates at 7 (max 4-bit signed)
    (-9, 4, 0, True, SAT, -8),  # Saturates at -8 (min 4-bit signed)
    # ERROR behavior
    (8, 4, 0, True, ERROR, OverflowError),
    (-9, 4, 0, True, ERROR, OverflowError),
    # Tests with fractional bits (qf > 0)
    (8.0, 4, 2, True, WRAP, -8.0),  # Same wrapping behavior with fractions
    (8.0, 4, 2, True, SAT, 7.75),  # Max is 7.75 with 2 fractional bits
]


@pytest.mark.parametrize(
    "x, qi, qf, signed, ovf_method, expected",
    OVERFLOW_TEST_CASES,
)
def test_overflow_behavior(x, qi, qf, signed, ovf_method, expected):  # noqa: PLR0913
    """Test different overflow handling methods."""
    if ovf_method == ERROR:
        with pytest.raises(expected):
            qfmt(x, qi, qf, signed=signed, rnd_method=TRUNC, ovf_method=ovf_method)
    else:
        result = qfmt(x, qi, qf, signed=signed, rnd_method=TRUNC, ovf_method=ovf_method)
        assert result == expected, (
            f"Failed for {x} with qi={qi}, qf={qf}, signed={signed}, ovf={ovf_method}.",
            f"Got {result}, expected {expected}",
        )


# Edge case tests that might need special handling
SPECIAL_OVERFLOW_CASES = [
    # Maximum values shouldn't overflow
    (15, 4, 0, False, WRAP, 15),  # Max unsigned
    (15, 4, 0, False, SAT, 15),
    (7, 4, 0, True, WRAP, 7),  # Max signed
    (7, 4, 0, True, SAT, 7),
    # Minimum values shouldn't overflow
    (0, 4, 0, False, WRAP, 0),  # Min unsigned
    (0, 4, 0, False, SAT, 0),
    (-8, 4, 0, True, WRAP, -8),  # Min signed
    (-8, 4, 0, True, SAT, -8),
    # Fractional edge cases
    (7.75, 4, 2, True, SAT, 7.75),  # Max representable with Q4.2
    (-8.0, 4, 2, True, SAT, -8.0),  # Min representable with Q4.2
]


@pytest.mark.parametrize("x, qi, qf, signed, ovf_method, expected", SPECIAL_OVERFLOW_CASES)
def test_overflow_edge_cases(x, qi, qf, signed, ovf_method, expected):  # noqa: PLR0913
    """Test edge cases where values are exactly at the overflow boundary."""
    result = qfmt(x, qi, qf, signed=signed, rnd_method=TRUNC, ovf_method=ovf_method)
    assert result == expected, f"Edge case failed for {x} with qi={qi}, qf={qf}, signed={signed}, ovf={ovf_method}"
