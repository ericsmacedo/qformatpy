.. Python Qformat (fixed point) documentation master file, created by
   sphinx-quickstart on Sun Jan 14 18:09:20 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to QformatPy documentation!
========================================================

.. automodule:: qformatpy
   :members:
   :undoc-members:
   :show-inheritance:

.. contents::

Introduction
------------
Welcome to the qformat Python library, a powerful tool for formatting floating-point
numbers into fixed-point representation with Q notation.

This library supports ARM's Q format, where QI includes the sign bit.

The main function, qformat, allows users to specify the number of integer bits (QI),
fractional bits (QF), whether the number is signed or unsigned, and provides flexibility
in choosing rounding and overflow handling methods.

Whether you're working on embedded systems, signal processing, or any application requiring fixed-point
representation, qformat is here to streamline the process.

The example below shows pi being converter to the sQ4.8 format, using Truncation as the
rounding method:

.. code-block:: python

   >>> from qformatpy import qformat

   >>> x = 3.141592653589793
   >>> result = qformat(x, qi=4, qf=8, rnd_method='Trunc')
   >>> result
   array([3.140625])


Installation
------------

The qformatpy library is available via PIP install:

.. code-block:: python

   python3 -m venv pyenv
   source pyenv/bin/activate

   pip install qformatpy

Import the package as shown below:

.. code-block:: python

   import qformatpy

The following functions should be available:

.. toctree::
   :maxdepth: 1

   overflow
   rounding
   qformat

A brief description of the functions can be seen below:

.. autosummary::
   .. toctree:: generated/

   overflow
   rounding
   qformat


Example usage
-------------

.. code-block:: python

   >>> import numpy as np
   >>> import qformatpy

   >>> test_array = np.array([1.4, 5.57, 3.14])
   >>> qformatpy.rounding(test_array, 'TowardsZero')
   array([1, 5, 3])

   >>> qformatpy.rounding(test_array, 'HalfDown')
   array([1, 6, 3])

   # Tests showing overflow and wrap
   >>> test_array = np.array([4, 5.6778, 356.123])
   >>> qformatpy.qformat(test_array, qi=5, qf=3)
   array([4.   , 5.625, 4.   ])

   >>> qformatpy.qformat(test_array, qi=9, qf=3)
   array([   4.   ,    5.625, -156.   ])

   # The input does not need to be an array
   >>> qformatpy.qformat(np.pi, qi=3, qf=4)
   3.125




Rounding methods
----------------

The library support the rounding methods listed below

Directed rounding to an integer: the displacements from the original number x to the
rounded value y are all directed toward or away from the same limiting value
(0, +inf, or -inf)

* 'Trunc': Round towards -inf.
* 'Ceiling': Round towards +inf.
* 'TowardsZero': Round towards zero.
* 'AwayFromZero': Round away from zero.

Round to the nearest: Rounding a number x to the nearest integer requires some
tie-breaking rule for those cases when x is exactly half-way between two integers
— that is, when the fraction part of x is exactly 0.5.

* 'HalfUp': Round half up.
* 'HalfDown': Round half down.
* 'HalfTowardsZero': Round half towards zero.
* 'HalfAwayFromZero': Round half away from zero.

For more information about the rounding methods above, refer to:
`Rounding <https://en.wikipedia.org/wiki/Rounding>`_

Speed Comparison
----------------

The test compares the time needed to convert 2^20 samples to the sQ6.8, using
HalfAwayFromZero rounding method, and wrap overflow method.

Results:

* QformatPy: 4.6 ms ± 51.8 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
* FxpMath: 6.2 ms ± 21.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
* Numfi: 33.7 ms ± 125 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
* Matlab: Elapsed time is 0.037031 seconds.

Using Truncation as rounding method (round towards -inf) and saturate for overflow:

* QformatPy: 2.19 ms ± 44.5 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
* FxpMath: 522 ms ± 4.84 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
* Numfi: 23.5 ms ± 113 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
* Matlab: Elapsed time is 0.026836 seconds.

Example code used for the comparison:

Matlab code:

.. code:: matlab

   n_samples = 2^20;
   test_data = randn(n_samples, 1)*10;

   % save test data to use it in python tests
   save('test_data.txt', 'test_data', '-ascii');

   F = fimath('OverflowAction','Wrap', 'RoundingMethod','Round');
   % Round: round towards nearest. Ties round toward negative infinity for
   % negative numbers, and toward positive infinity for positive numbers.

   qi = 6;
   qf = 8;
   w = qi + qf;

   tic;
   fxp_data = fi(test_data, 1, w, qf, F);
   toc;

Elapsed time is 0.037031 seconds.

.. code:: python

   import numpy as np
   from qformatpy import qformat
   from fxpmath import Fxp
   import numfi

   x = np.loadtxt('examples/test_data.txt')

   # Used by numfi and fxpmath
   s = 1
   qi = 6
   qf = 8
   w = qi + qf
   # Qformat (used by QformatPy)

   # Fixed point initialization
   init_qfmt = %timeit -o qfmt_x = qformat(x, qi=qi, qf=qf, rnd_method='HalfAwayFromZero')
   init_fxp = %timeit -o fxpmath_x = Fxp(x, s, w, qf, rounding='around', overflow='wrap')
   init_numfi = %timeit -o numfi_x = numfi(x, s, w, qf, RoudingMethod='Round', OverflowAction='Wrap')

   init_qfmt = %timeit -o qfmt_x = qformat(x, qi=qi, qf=qf, rnd_method='Trunc', overflow_action="Saturate")
   init_fxp = %timeit -o fxpmath_x = Fxp(x, s, w, qf, rounding='trunc', overflow='saturate')
   init_numfi = %timeit -o numfi_x = numfi(x, s, w, qf, RoudingMethod='Floor', OverflowAction='Saturate')
