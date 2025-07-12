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


import numpy as np
from numba import njit, types
from numba.extending import overload

from .constants import AWAY, CEIL, ERROR, HALF_AWAY, HALF_DOWN, HALF_EVEN, HALF_UP, HALF_ZERO, SAT, TO_ZERO, TRUNC, WRAP

RND_MIDPOINT = 0.5  # Threshold for half-way rounding


@njit
def _rnd_scalar(x, method=TRUNC):  # noqa: PLR0911, PLR0912, C901
    if method == TRUNC:
        return int(np.floor(x))
    if method == CEIL:
        return int(np.ceil(x))
    if method == TO_ZERO:
        return int(x)
    if method == AWAY:
        if x >= 0:
            return int(np.ceil(x))
        return int(-np.ceil(np.abs(x)))
    if method == HALF_UP:
        return int(np.floor(x + RND_MIDPOINT))
    if method == HALF_DOWN:
        return int(np.ceil(x - RND_MIDPOINT))
    if method == HALF_ZERO:
        if x >= 0:
            return int(np.ceil(x - RND_MIDPOINT))
        return int(-np.ceil(np.abs(x) - RND_MIDPOINT))
    if method == HALF_AWAY:
        if x >= 0:
            return int(np.floor(x + RND_MIDPOINT))
        return int(-np.floor(np.abs(x) + RND_MIDPOINT))
    if method == HALF_EVEN:
        floor_x = np.floor(x)
        frac = x - floor_x
        is_half = frac == RND_MIDPOINT
        if is_half:
            return int(floor_x + (floor_x % 2 == 1))
        return int(np.round(x))
    raise ValueError(f"invalid method: {method}")


@njit
def _rnd_array(x, method=TRUNC):
    if method == TRUNC:  # Round towards -inf
        x = np.floor(x)
    elif method == CEIL:  # Round towards +inf
        x = np.ceil(x)
    elif method == TO_ZERO:
        pass
    elif method == AWAY:
        x = np.where(x >= 0, np.ceil(np.abs(x)), -np.ceil(np.abs(x)))
    elif method == HALF_UP:
        x = np.floor(x + RND_MIDPOINT)
    elif method == HALF_DOWN:
        x = np.ceil(x - RND_MIDPOINT)
    elif method == HALF_ZERO:
        x = np.where(x >= 0, np.ceil(np.abs(x) - RND_MIDPOINT), -np.ceil(np.abs(x) - RND_MIDPOINT))
    elif method == HALF_AWAY:
        x = np.where(x >= 0, np.floor(np.abs(x) + RND_MIDPOINT), -np.floor(np.abs(x) + RND_MIDPOINT))
    elif method == HALF_EVEN:
        floor_x = np.floor(x)
        frac = x - floor_x
        is_half = frac == RND_MIDPOINT
        even_correction = floor_x % 2 == 1  # if odd, add 1 to make even
        x = np.where(
            is_half,
            floor_x + even_correction,
            np.round(x),  # normal round otherwise (to nearest)
        )
    else:
        raise ValueError(f"invalid method: {method}")

    return x.astype(np.int64)


@njit
def _overflow_scalar(x: int, signed: bool = True, w: int = 16, method: int = WRAP):
    # Maximum and minimum values with w bits representation
    if signed:
        upper = (1 << (w - 1)) - 1
        lower = -(1 << (w - 1))
    else:
        upper = (1 << w) - 1
        lower = 0

    if method == WRAP:
        mask = 1 << w
        x = x & (mask - 1)
        if signed:
            if x >= (1 << (w - 1)):
                return x | (-mask)
    elif method == SAT:
        if x > upper:
            return upper
        if x < lower:
            return lower
    elif method == ERROR:
        if x > upper or x < lower:
            raise OverflowError("Overflow!")
    else:
        raise ValueError(f"invalid method: {method}")

    return x


@njit
def _overflow_array(x, signed: bool = True, w: int = 16, method: int = WRAP):
    x = np.asarray(x, dtype=np.int64)

    # Maximum and minimum values with w bits representation
    if signed:
        upper = (1 << (w - 1)) - 1
        lower = -(1 << (w - 1))
    else:
        upper = (1 << w) - 1
        lower = 0

    if method == WRAP:
        mask = 1 << w
        x = x & (mask - 1)
        if signed:
            x = np.where(x < (1 << (w - 1)), x, x | (-mask))
    elif method == SAT:
        x[x > upper] = upper
        x[x < lower] = lower
    elif method == ERROR:
        up = x > upper
        low = x < lower
        if np.any(up | low):
            raise OverflowError("Overflow!")
    else:
        raise ValueError(f"invalid method: {method}")

    return x


@njit
def _qfmt_array(x, qi: int, qf: int, signed: bool = True, rnd_method=TRUNC, ovf_method=WRAP):  # noqa: PLR0913
    x = x * 2.0**qf

    x = _rnd_array(x, method=rnd_method)
    x = _overflow_array(x, signed=signed, w=(qi + qf), method=ovf_method)

    return x / 2.0**qf


@njit
def _qfmt_scalar(x, qi: int, qf: int, signed: bool = True, rnd_method=TRUNC, ovf_method=WRAP):  # noqa: PLR0913
    x *= 2.0**qf

    x = _rnd_scalar(x, method=rnd_method)
    x = _overflow_scalar(x, signed=signed, w=(qi + qf), method=ovf_method)

    return x / 2.0**qf


def qformat(  # noqa: PLR0913
    x: float | np.ndarray, qi: int, qf: int, signed: bool = True, rnd_method=TRUNC, ovf_method=WRAP
) -> float | np.ndarray:
    """Convert a numeric value to fixed-point representation using Q-format notation.

    Parameters
    ----------
    x : int, float or array-like
        The input value(s) to convert.
    qi : int
        Number of integer bits (excluding sign bit if signed=True).
    qf : int
        Number of fractional bits.
    signed : bool, optional
        Whether the fixed-point format is signed (default is True).
    rnd_method : int, optional
        Rounding method to apply (default is TRUNC (0)).

        Supported methods:

        - TRUNC (0): Bit Truncation. Rounds towards negative infinity.
        - CEIL (1): Round toward positive infinity.
        - TO_ZERO (2): Round toward zero.
        - AWAY (3): Round away from zero.
        - HALF_UP (4): Round to nearest; ties round towards positive infinity.
        - HALF_DOWN (5): Round to nearest; ties round toward negative infinity.
        - HALF_EVEN (6): Round to nearest; ties round to even.
        - HALF_ZERO (7): Round to nearest; ties round toward zero.
        - HALF_AWAY (8): Round to nearest; ties round away from zero.

    ovf_method : int, optional
        Overflow handling method (default is WRAP (0)).

        Supported methods:

        - WRAP (0): Wrap around on overflow (modulo behavior).
        - SAT (1): Saturate to maximum/minimum representable value.
        - ERROR (2): Raise an error if overflow occurs.

    Returns:
    -------
    float or ndarray
        Fixed-point representation of the input, as integer(s).

    Notes:
    -----
    Uses ARM-style Q-format notation where a Qm.n format has:
        - m integer bits (qi)
        - n fractional bits (qf)
        - Optional sign bit if `signed` is True
    """
    if isinstance(x, np.ndarray):
        return _qfmt_array(x, qi, qf, signed, rnd_method, ovf_method)

    if isinstance(x, float | int):
        return _qfmt_scalar(x, qi, qf, signed, rnd_method, ovf_method)

    raise TypeError(f"Unsupported type: {x}")


@overload(qformat)
def qfmt_overload(x, qi: int, qf: int, signed: bool = True, rnd_method=TRUNC, ovf_method=WRAP):  # noqa: PLR0913, ARG001
    # Array case
    if isinstance(x, types.Array):

        def impl(x, qi: int, qf: int, signed: bool = True, rnd_method=TRUNC, ovf_method=WRAP):  # noqa: PLR0913
            return _qfmt_array(x, qi, qf, signed, rnd_method, ovf_method)

        return impl

    if isinstance(x, types.Integer | types.Float):

        def impl(x, qi: int, qf: int, signed: bool = True, rnd_method=TRUNC, ovf_method=WRAP):  # noqa: PLR0913
            return _qfmt_scalar(x, qi, qf, signed, rnd_method, ovf_method)

        return impl
    raise TypeError(f"Unsupported type: {x}")
