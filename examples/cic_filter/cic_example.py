"""Simple CIC example."""
from qformatpy import qformat as qfmt
from numba import njit
import numpy as np

import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt

@njit
def integrator(x):
    """16 bits integrator."""

    n_smp = len(x)
    out = np.zeros(n_smp + 1)

    for i in range(n_mp):
        out[i+1] = qfmt(out[i] + x[i], qi=16, qf=0) 
    return out


def cic_filter(x):
    n_smp = len(x)
    # Convert input to sQ5.7
    x = qfmt(x, qi=5, qf=7)

    # 12 bits integrator
    integrator_out = np.zeros(n_smp + 1)
    for i in range(n_smp):
        int_sum = integrator_out[i] + x[i]
        integrator_out[i+1] = qfmt(int_sum, qi=16, qf=0) 

    # 4th order comb filter
    diff_out = np.diff(x, n=4)

    return diff_out


if __name__ == "__main__":

    # DC input
    x = np.ones(2**18)
    cic_out = cic_filter(x)

    plt.plot(cic_out)
    plt.show()
