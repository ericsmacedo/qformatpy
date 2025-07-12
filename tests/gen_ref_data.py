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
"""Generates reference data for tests."""

from itertools import product
from pathlib import Path

import numpy as np
from tqdm import tqdm

from qformatpy import qformat as qfmt
from qformatpy.constants import rounding_modes

PRJ_PATH = Path(__file__).parent.parent


def gen_ref():
    """Generate reference data for tests."""
    n_smp = 2**8

    rng = np.random.default_rng()  # Create a Generator instance
    w = rng.randint(low=1, high=16, size=n_smp)
    qf = rng.randint(low=0, high=8, size=n_smp)
    qi = w - qf
    x = rng.normal(loc=0, scale=60, size=n_smp)
    qfmt_args = list(product(rounding_modes.values(), [0, 1], [True, False]))

    ref_file = ""
    for i in tqdm(range(n_smp)):
        for rnd_method, ovf_method, signed in qfmt_args:
            out = qfmt(x[i], qi=qi[i], qf=qf[i], rnd_method=rnd_method, ovf_method=ovf_method, signed=signed)
            ref_file += f"{x[i]}, {qi[i]}, {qf[i]}, {rnd_method}, {ovf_method}, {signed}, {out}\n"

    output_path = PRJ_PATH / "tests" / "test_data.txt"
    output_path.write_text(ref_file)


if __name__ == "__main__":
    gen_ref()
