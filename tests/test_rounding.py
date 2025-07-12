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
"""Tests qformatpy for different rounding methods."""

import math

import pytest

from qformatpy import AWAY, CEIL, HALF_AWAY, HALF_DOWN, HALF_EVEN, HALF_UP, HALF_ZERO, TO_ZERO, TRUNC, WRAP
from qformatpy import qformat as qfmt

# Test cases for rounding behavior (ARM QFormat where qi includes sign bit)
# Format: (input_value, qi, qf, expected_results_dict)
ROUNDING_TEST_CASES = [
    # Basic rounding tests (Q4.0 - 3 integer bits + 1 sign bit)
    (
        3.3,
        4,
        0,
        {
            TRUNC: 3,
            CEIL: 4,
            TO_ZERO: 3,
            AWAY: 4,
            HALF_UP: 3,
            HALF_DOWN: 3,
            HALF_EVEN: 3,
        },
    ),
    (
        3.5,
        4,
        0,
        {
            TRUNC: 3,
            CEIL: 4,
            TO_ZERO: 3,
            AWAY: 4,
            HALF_UP: 4,
            HALF_DOWN: 3,
            HALF_EVEN: 4,
        },
    ),
    (
        -3.5,
        4,
        0,
        {
            TRUNC: -4,
            CEIL: -3,
            TO_ZERO: -3,
            AWAY: -4,
            HALF_UP: -3,
            HALF_DOWN: -4,
            HALF_EVEN: -4,
            HALF_ZERO: -3.0,
        },
    ),
    # Fractional bits tests (Q3.2 - 1 integer bit + 1 sign bit + 2 fractional)
    (
        0.999,
        3,
        2,
        {
            TRUNC: 0.75,
            CEIL: 1.0,
            HALF_UP: 1.0,
            HALF_EVEN: 1.0,
        },
    ),
    (
        -0.999,
        3,
        2,
        {
            TRUNC: -1.0,
            CEIL: -0.75,
            HALF_UP: -1.0,
            HALF_ZERO: -1.0,
        },
    ),
    (
        0.624,
        3,
        2,
        {
            TRUNC: 0.5,
            HALF_UP: 0.5,
            HALF_EVEN: 0.5,
            HALF_ZERO: 0.5,
        },
    ),
    (
        0.626,
        3,
        2,
        {
            TRUNC: 0.5,
            HALF_UP: 0.75,
            HALF_EVEN: 0.75,
        },
    ),
    # Edge cases
    (
        -0.1,
        3,
        2,
        {
            TRUNC: -0.25,
            CEIL: 0.0,
            TO_ZERO: 0.0,
        },
    ),
    (
        1.749,
        3,
        2,  # Just below max positive (1.75)
        {
            TRUNC: 1.5,
            CEIL: 1.75,
            HALF_UP: 1.75,
        },
    ),
    (
        -2.0,
        3,
        2,  # Exact min value
        {
            TRUNC: -2.0,
            CEIL: -2.0,
            HALF_EVEN: -2.0,
        },
    ),
]

# All rounding methods to test
ROUNDING_METHODS = [
    TRUNC,
    CEIL,
    TO_ZERO,
    AWAY,
    HALF_UP,
    HALF_DOWN,
    HALF_EVEN,
    HALF_ZERO,
    HALF_AWAY,
]


@pytest.mark.parametrize("x, qi, qf, expected_results", ROUNDING_TEST_CASES)
@pytest.mark.parametrize("rnd_method", ROUNDING_METHODS)
def test_rounding_methods(x, qi, qf, expected_results, rnd_method):
    """Test rounding methods with ARM QFormat (qi includes sign bit)."""
    if rnd_method not in expected_results:
        pytest.skip(f"Method {rnd_method} not tested for this case")

    expected = expected_results[rnd_method]
    result = qfmt(x, qi, qf, rnd_method=rnd_method, ovf_method=WRAP)

    # Float comparison with tolerance for fractional cases
    if isinstance(expected, float):
        assert math.isclose(result, expected, abs_tol=1e-9), (
            f"Q{qi}.{qf}: {x} rounded with {rnd_method} got {result}, expected {expected}"
        )
    else:
        assert result == expected, f"Q{qi}.{qf}: {x} rounded with {rnd_method} got {result}, expected {expected}"
