"""Example of a fixed-point integrator model."""
import numpy as np
from numba import njit
import matplotlib.pyplot as plt
from qformatpy import qformat as qfmt
from qformatpy.constants import SAT


@njit
def integrator(x: np.ndarray) -> np.ndarray:
    """Example of a simple fixed-point integrator."""

    len_x = len(x)

    # convert float input to sQ4.5 and saturation
    # qformat accepts receiving numpy arrays
    x_qfmt = qfmt(x, 4, 5, ovf_method=SAT)

    # implement accumulator
    acc = 0
    y = np.zeros(n_smp)
    for i in range(len_x):

        # Adder output
        sum_out = acc + x[i]

        # The accumulator register is 12 bits, with 
        # fixed-point format of sQ6.6. The default overflow
        # method is WRAP
        acc = qfmt(sum_out, 7, 5)
        y[i] = sum_out 

    return y


# number of samples used for the simulation
n_smp = 2**18

# DC value of 5 + Gaussian noise
x = 5*np.ones(n_smp)

y = integrator(x)

plt.plot(y)
plt.show()
