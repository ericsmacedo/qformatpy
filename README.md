
[![PyPI Version](https://badge.fury.io/py/qformatpy.svg)](https://badge.fury.io/py/qformatpy)
[![Python Build](https://github.com/ericsmacedo/qformatpy/actions/workflows/main.yml/badge.svg)](https://github.com/ericsmacedo/qformatpy/actions/workflows/main.yml)
[![Documentation](https://readthedocs.org/projects/qformatpy/badge/?version=stable)](https://qformatpy.readthedocs.io/en/stable/)
[![Coverage Status](https://coveralls.io/repos/github/ericsmacedo/qformatpy/badge.svg?branch=main)](https://coveralls.io/github/ericsmacedo/qformatpy?branch=main)
[![python-versions](https://img.shields.io/pypi/pyversions/qformatpy.svg)](https://pypi.python.org/pypi/qformatpy)
[![semantic-versioning](https://img.shields.io/badge/semver-2.0.0-green)](https://semver.org/)

[![Contributors](https://img.shields.io/github/contributors/ericsmacedo/qformatpy.svg)](https://github.com/ericsmacedo/qformatpy/graphs/contributors/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
[![Issues](https://img.shields.io/github/issues/ericsmacedo/qformatpy)](https://github.com/ericsmacedo/qformatpy/issues)
[![PRs open](https://img.shields.io/github/issues-pr/ericsmacedo/qformatpy.svg)](https://github.com/ericsmacedo/qformatpy/pulls)
[![PRs done](https://img.shields.io/github/issues-pr-closed/ericsmacedo/qformatpy.svg)](https://github.com/ericsmacedo/qformatpy/pulls?q=is%3Apr+is%3Aclosed)

# Easy-to-use fixed-point library

**qformatpy** is a lightweight Python library for converting numbers to fixed-point format using the ARM-style Qm.n notation. It is designed to be simple, readable, and easy to integrate into simulation, modeling, or hardware verification pipelines.

The library provides a single function, `qformat`, that lets you control integer and fractional precision, signedness, rounding behavior, and overflow handling — all without the complexity of a full fixed-point arithmetic suite.

Whether you're developing embedded systems, DSP algorithms, or just need fast fixed-point conversion, **qformatpy** keeps things straightforward.

- [Documentation](https://qformatpy.readthedocs.io/en/latest/)
* [PyPI](https://pypi.org/project/qformatpy/)
* [Sources](https://github.com/ericsmacedo/qformatpy)
* [Issues](https://github.com/ericsmacedo/qformatpy/issues)

## Features

- **Support for Numba**
  Optimized with optional [Numba](https://numba.pydata.org/) acceleration for fast, JIT-compiled conversions.

- **Native NumPy Array Support**
  Seamlessly handles `numpy.ndarray` inputs for efficient batch processing.

- **Flexible Rounding Modes**
  Choose from 9 rounding modes, including truncation, ceiling, rounding to nearest (with tie-breaking), and more.

- **Customizable Overflow Handling**
  Select between wraparound, saturation, or error-on-overflow behavior.

- **Signed and Unsigned Formats**
  Easily switch between signed and unsigned representations using the `signed` parameter.

- **Consistent Q-Format Notation**
  Follows ARM-style Qm.n notation for compatibility with DSP and embedded tools.

- **Well-Suited for Embedded and DSP Simulation**
  Ideal for preparing and validating fixed-point behavior before deploying to hardware.

## Installation

Installing it is pretty easy:

```bash
pip install qformatpy
```
