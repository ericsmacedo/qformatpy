import numpy as np


__all__ = ["rounding", "overflow", "qformat"]


def rounding(iarray, rnd_method):
    """
    Rounds each element in the input array according to the specified rounding method.

    Parameters
    ----------
    iarray : numpy.ndarray
        Input array containing numerical values.
    rnd_method : str
        Rounding method to be applied. Supported methods:
            - 'Trunc': Round towards -inf.
            - 'Ceiling': Round towards +inf.
            - 'TowardsZero': Round towards zero.
            - 'AwayFromZero': Round away from zero.
            - 'HalfUp': Round half up.
            - 'HalfDown': Round half down.
            - 'HalfTowardsZero': Round half towards zero.
            - 'HalfAwayFromZero': Round half away from zero.

    Returns
    -------
    numpy.ndarray
        Array of rounded values based on the specified rounding method.

    Raises
    ------
    ValueError
        If an invalid rounding method is provided.

    Examples
    --------
    >>> input_array = np.array([3.7, 2.2, -5.5])
    >>> rounding(input_array, 'Trunc')
    array([ 3,  2, -6])

    >>> rounding(input_array, 'HalfUp')
    array([ 4,  2, -5])
    """

    if rnd_method == 'Trunc':  # Round towards -inf
        iarray = np.floor(iarray)
    elif rnd_method == 'Ceiling':  # Round towards +inf
        iarray = np.ceil(iarray)
    elif rnd_method == 'TowardsZero':  # Round towards zero
        pass
    elif rnd_method == "AwayFromZero":
        iarray = np.sign(iarray) * np.ceil(np.abs(iarray))
    elif rnd_method == 'HalfUp':
        iarray = np.floor(iarray + 0.5)
    elif rnd_method == 'HalfDown':
        iarray = np.ceil(iarray - 0.5)
    elif rnd_method == "HalfTowardsZero":
        iarray = np.sign(iarray) * np.ceil(np.abs(iarray) - 0.5)
    elif rnd_method == 'HalfAwayFromZero':
        iarray = np.sign(iarray) * np.floor(np.abs(iarray) + 0.5)
    else:
        raise ValueError(f"invaild rnd_method: {rnd_method}")

    return iarray.astype(np.int64)


def overflow(iarray, signed, w, overflow_action):
    """
    Handle overflow in an integer array based on the specified overflow action.

    Parameters
    ----------
    iarray : numpy.ndarray
        Input array containing integer values.
    signed : bool
        Indicates whether the numbers in the array are signed (True) or unsigned (False).
    w : int
        Number of bits used to represent each value in the array.
    overflow_action : str
        Action to be taken in case of overflow. Supported actions:
            - 'Error': Raise an OverflowError if overflow occurs.
            - 'Wrap': Wraparound overflow, values wrap around the representable range.
            - 'Saturate': Saturate overflow, values are clamped to the maximum or minimum representable value.

    Returns
    -------
    numpy.ndarray
        Array with overflow-handled values.

    Raises
    ------
    OverflowError
        If overflow_action is 'Error' and overflow occurs.
    ValueError
        If an invalid overflow_action is provided.
    """

    iarray = iarray.astype(np.int64)

    # Maximum and minimum values with w bits representation
    if signed:
        upper = (1 << (w - 1)) - 1
        lower = -(1 << (w - 1))
    else:
        upper = (1 << w) - 1
        lower = 0

    if overflow_action == 'Error':
        up = iarray > upper
        low = iarray < lower
        if np.any(up | low):
            raise OverflowError("Overflow!")
    elif overflow_action == 'Wrap':
        mask = (1 << w)
        iarray &= (mask - 1)
        if signed:
            iarray[iarray >= (1 << (w - 1))] |= (-mask)
    elif overflow_action == 'Saturate':
        up = iarray > upper
        low = iarray < lower
        iarray[up] = upper
        iarray[low] = lower
    else:
        raise ValueError(f"invaild overflow_action: {overflow_action}")

    return iarray


def qformat(x, qi: int, qf: int, signed: bool = True, rnd_method='Trunc',
            overflow_action='Wrap'):
    """
    Format a given numeric value 'x' into fixed-point representation with Q format.

    The Q format is specified using ARM's notation, where QI includes the sign bit.

    Parameters
    ----------
    x : float or numpy.ndarray
        Input numeric value or array to be formatted.
    qi : int
        Number of integer bits in the Q format.
    qf : int
        Number of fractional bits in the Q format.
    signed : bool, optional
        Indicates whether the number is signed (True) or unsigned (False). Default is True.
    rnd_method : str, optional
        Rounding method to be applied. Supported methods:
            - 'Trunc': Round towards -inf.
            - 'Ceiling': Round towards +inf.
            - 'TowardsZero': Round towards zero.
            - 'AwayFromZero': Round away from zero.
            - 'HalfUp': Round half up.
            - 'HalfDown': Round half down.
            - 'HalfTowardsZero': Round half towards zero.
            - 'HalfAwayFromZero': Round half away from zero.
        Default is 'Trunc'.
    overflow_action : str, optional
        Action to be taken in case of overflow. Supported actions:
            - 'Error': Raise an OverflowError if overflow occurs.
            - 'Wrap': Wraparound overflow, values wrap around the representable range.
            - 'Saturate': Saturate overflow, values are clamped to the maximum or minimum representable value.
        Default is 'Wrap'.
    """
    x = np.asarray(x * 2**qf, dtype=np.float64)

    if x.shape == ():
        x = x.reshape(1, )

    x = rounding(x, rnd_method=rnd_method)
    x = overflow(x, signed=signed, w=(qi + qf), overflow_action=overflow_action) / 2**qf

    return x
