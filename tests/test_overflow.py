import numpy as np
import pytest
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from qformatpy import overflow


def test_overflow_error_action():
    input_array = np.array([127, 200, -129])
    with pytest.raises(OverflowError):
        overflow(input_array, signed=True, w=8, overflow_action='Error')


def test_overflow_wrap_action_signed():
    input_array = np.array([300, -200, 1000])
    expected_result = np.array([44, 56, -24], dtype=np.int64)
    result = overflow(input_array, signed=True, w=8, overflow_action='Wrap')
    np.testing.assert_array_equal(result, expected_result)


def test_overflow_wrap_action_unsigned():
    input_array = np.array([300, 500, 1000])
    expected_result = np.array([44, 244, 232], dtype=np.int64)
    result = overflow(input_array, signed=False, w=8, overflow_action='Wrap')
    np.testing.assert_array_equal(result, expected_result)


def test_overflow_saturate_action_signed():
    input_array = np.array([300, -200, 1000])
    expected_result = np.array([127, -128, 127], dtype=np.int64)
    result = overflow(input_array, signed=True, w=8, overflow_action='Saturate')
    np.testing.assert_array_equal(result, expected_result)


def test_overflow_saturate_action_unsigned():
    input_array = np.array([300, 500, 1000, -500])
    expected_result = np.array([255, 255, 255, 0], dtype=np.int64)
    result = overflow(input_array, signed=False, w=8, overflow_action='Saturate')
    np.testing.assert_array_equal(result, expected_result)


def test_invalid_overflow_action():
    input_array = np.array([100, 200, 300])
    with pytest.raises(ValueError):
        overflow(input_array, signed=True, w=8, overflow_action='InvalidAction')
