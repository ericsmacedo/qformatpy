Welcome to QformatPy documentation!
========================================================

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

Links
-----

- Documentation: https://qformatpy.readthedocs.io/en/latest/
