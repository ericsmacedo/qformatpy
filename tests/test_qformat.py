
import numpy as np
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from qformatpy import qformat


def test_trunc_method_positive_numbers():
    qf = 5
    qi = 10
    input_array = np.array([3.7, 2.2, 5.9]) / 2**qf
    expected_result = np.array([3, 2, 5]) / 2**qf
    result = qformat(input_array, qi=qi, qf=qf, rnd_method='Trunc')
    np.testing.assert_array_equal(result, expected_result)


def test_away_from_zero_method_zero():
    qf = 5
    qi = 3

    input_array = np.array([0.0, 0.1, -0.1]) / 2**qf
    expected_result = np.array([0, 1, -1]) / 2**qf  # Round up for positive zero, round down for negative zero
    result = qformat(input_array, qi=qi, qf=qf, rnd_method='AwayFromZero')
    np.testing.assert_array_equal(result, expected_result)


def test_overflow_wrap_action_signed():
    qi = 5
    qf = 3
    input_array = np.array([300, -200, 1000]) / 2**qf
    expected_result = np.array([44, 56, -24], dtype=np.int64) / 2**qf
    result = qformat(input_array, signed=True, qi=qi, qf=qf, overflow_action='Wrap')
    np.testing.assert_array_equal(result, expected_result)


def test_overflow_wrap_action_signed_single_number():
    qi = 5
    qf = 3
    input_value = 1000 / 2**qf
    expected_result = -24 / 2**qf
    result = qformat(input_value, signed=True, qi=qi, qf=qf, overflow_action='Wrap')
    np.testing.assert_array_equal(result, expected_result)
    assert type(result) is float


def test_overflow_wrap_action_unsigned():
    qi = 5
    qf = 3
    input_array = np.array([300, 500, 1000]) / 2**qf
    expected_result = np.array([44, 244, 232], dtype=np.int64) / 2**qf
    result = qformat(input_array, signed=False, qi=qi, qf=qf, overflow_action='Wrap')
    np.testing.assert_array_equal(result, expected_result)
