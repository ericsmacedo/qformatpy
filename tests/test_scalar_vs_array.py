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
"""Checks if scalar, array, njin and non njit functions match."""

import numpy as np
import pytest
from numba import njit

from qformatpy import qformat as qfmt
from qformatpy.constants import (
    AWAY,
    CEIL,
    HALF_AWAY,
    HALF_DOWN,
    HALF_EVEN,
    HALF_UP,
    HALF_ZERO,
    SAT,
    TO_ZERO,
    TRUNC,
    WRAP,
)


def _qfmt_arr(a, qi, qf, signed, rnd_method, ovf_method):  # noqa: PLR0913
    return qfmt(a, qi, qf, signed, rnd_method, ovf_method)


def _qfmt_scalar(a, qi, qf, signed, rnd_method, ovf_method):  # noqa: PLR0913
    n = len(a)
    out = np.zeros(n)
    for i in range(n):
        out[i] = qfmt(a[i], qi, qf, signed=signed, rnd_method=rnd_method, ovf_method=ovf_method)
    return out


@njit
def _qfmt_arr_njit(a, qi, qf, signed, rnd_method, ovf_method):  # noqa: PLR0913
    return qfmt(a, qi, qf, signed=signed, rnd_method=rnd_method, ovf_method=ovf_method)


@njit
def _qfmt_scalar_njit(a, qi, qf, signed, rnd_method, ovf_method):  # noqa: PLR0913
    n = len(a)
    out = np.zeros(n)
    for i in range(n):
        out[i] = qfmt(a[i], qi, qf, signed=signed, rnd_method=rnd_method, ovf_method=ovf_method)
    return out


# Test configurations
QI_VALUES = [4, 8, 16, 9]
QF_VALUES = [0, 4, 8, 10, 1]
ROUNDING_METHODS = [TRUNC, CEIL, TO_ZERO, AWAY, HALF_UP, HALF_DOWN, HALF_EVEN, HALF_ZERO, HALF_AWAY]
OVERFLOW_METHODS = [WRAP, SAT]
SIGNED = [True, False]
ARR_NJIT = [True, False]
SCALAR_NJIT = [True, False]


@pytest.mark.parametrize("qi", QI_VALUES)
@pytest.mark.parametrize("qf", QF_VALUES)
@pytest.mark.parametrize("rnd_method", ROUNDING_METHODS)
@pytest.mark.parametrize("ovf_method", OVERFLOW_METHODS)
@pytest.mark.parametrize("signed", SIGNED)
@pytest.mark.parametrize("arr_njit", ARR_NJIT)
@pytest.mark.parametrize("scalar_njit", SCALAR_NJIT)
def test_array_vs_scalar_consistency(qi, qf, rnd_method, ovf_method, signed, arr_njit, scalar_njit):  # noqa: PLR0913
    """Test that array and scalar implementations produce identical results."""
    rng = np.random.default_rng()  # Create a Generator instance
    test_data = rng.uniform(low=-1000.0, high=1000.0, size=2**4)

    # Array implementation
    if arr_njit:
        arr_result = _qfmt_arr_njit(
            test_data, qi=qi, qf=qf, signed=signed, rnd_method=rnd_method, ovf_method=ovf_method
        )
    else:
        arr_result = _qfmt_arr(test_data, qi=qi, qf=qf, signed=signed, rnd_method=rnd_method, ovf_method=ovf_method)

    if scalar_njit:
        scalar_result = _qfmt_scalar_njit(
            test_data, qi=qi, qf=qf, signed=signed, rnd_method=rnd_method, ovf_method=ovf_method
        )
    else:
        scalar_result = _qfmt_scalar(
            test_data, qi=qi, qf=qf, signed=signed, rnd_method=rnd_method, ovf_method=ovf_method
        )

    # Compare results
    assert np.array_equal(arr_result, scalar_result), (
        f"Inconsistent results for Q{qi}.{qf} with "
        f"rnd={rnd_method}, ovf={ovf_method}\n"
        f"Input: {test_data}\n"
        f"Array result: {arr_result}\n"
        f"Scalar result: {scalar_result}"
    )
