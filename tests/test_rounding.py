
import numpy as np
import pytest
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from qformatpy import rounding

# Assuming your rounding function is defined in a module named rounding_module


def test_trunc_method_positive_numbers():
    input_array = np.array([3.7, 2.2, 5.9])
    expected_result = np.array([3, 2, 5])
    result = rounding(input_array, 'Trunc')
    np.testing.assert_array_equal(result, expected_result)


def test_trunc_method_negative_numbers():
    input_array = np.array([-3.7, -2.2, -5.9])
    expected_result = np.array([-4, -3, -6])
    result = rounding(input_array, 'Trunc')
    np.testing.assert_array_equal(result, expected_result)


def test_trunc_method_mixed_numbers():
    input_array = np.array([3.7, -2.2, 5.9])
    expected_result = np.array([3, -3, 5])
    result = rounding(input_array, 'Trunc')
    np.testing.assert_array_equal(result, expected_result)


def test_trunc_method_zero():
    input_array = np.array([0.0, 0.1, -0.1])
    expected_result = np.array([0, 0, -1])
    result = rounding(input_array, 'Trunc')
    np.testing.assert_array_equal(result, expected_result)


def test_ceiling_method_positive_numbers():
    input_array = np.array([3.7, 2.2, 5.9])
    expected_result = np.array([4, 3, 6])
    result = rounding(input_array, 'Ceiling')
    np.testing.assert_array_equal(result, expected_result)


def test_ceiling_method_negative_numbers():
    input_array = np.array([-3.7, -2.2, -5.9])
    expected_result = np.array([-3, -2, -5])
    result = rounding(input_array, 'Ceiling')
    np.testing.assert_array_equal(result, expected_result)


def test_ceiling_method_mixed_numbers():
    input_array = np.array([3.7, -2.2, 5.9])
    expected_result = np.array([4, -2, 6])
    result = rounding(input_array, 'Ceiling')
    np.testing.assert_array_equal(result, expected_result)


def test_ceiling_method_zero():
    input_array = np.array([0.0, 0.1, -0.1])
    expected_result = np.array([0, 1, 0])
    result = rounding(input_array, 'Ceiling')
    np.testing.assert_array_equal(result, expected_result)


def test_zero_method_positive_numbers():
    input_array = np.array([3.7, 2.2, 5.9])
    expected_result = np.array([3, 2, 5])  # No change for positive numbers
    result = rounding(input_array, 'TowardsZero')
    np.testing.assert_array_equal(result, expected_result)


def test_zero_method_negative_numbers():
    input_array = np.array([-3.7, -2.2, -5.9])
    expected_result = np.array([-3, -2, -5])  # No change for negative numbers
    result = rounding(input_array, 'TowardsZero')
    np.testing.assert_array_equal(result, expected_result)


def test_zero_method_mixed_numbers():
    input_array = np.array([3.7, -2.2, 5.9])
    expected_result = np.array([3, -2, 5])  # No change for mixed numbers
    result = rounding(input_array, 'TowardsZero')
    np.testing.assert_array_equal(result, expected_result)


def test_zero_method_zero():
    input_array = np.array([0.0, 0.1, -0.1])
    expected_result = np.array([0, 0, 0])  # No change for zero
    result = rounding(input_array, 'TowardsZero')
    np.testing.assert_array_equal(result, expected_result)


def test_away_from_zero_method_positive_numbers():
    input_array = np.array([3.7, 2.2, 5.9])
    expected_result = np.array([4, 3, 6])  # Round up for positive numbers
    result = rounding(input_array, 'AwayFromZero')
    np.testing.assert_array_equal(result, expected_result)


def test_away_from_zero_method_negative_numbers():
    input_array = np.array([-3.7, -2.2, -5.9])
    expected_result = np.array([-4, -3, -6])  # Round down for negative numbers
    result = rounding(input_array, 'AwayFromZero')
    np.testing.assert_array_equal(result, expected_result)


def test_away_from_zero_method_mixed_numbers():
    input_array = np.array([3.7, -2.2, 5.9])
    expected_result = np.array([4, -3, 6])  # Round up for positive, round down for negative
    result = rounding(input_array, 'AwayFromZero')
    np.testing.assert_array_equal(result, expected_result)


def test_away_from_zero_method_zero():
    input_array = np.array([0.0, 0.1, -0.1])
    expected_result = np.array([0, 1, -1])  # Round up for positive zero, round down for negative zero
    result = rounding(input_array, 'AwayFromZero')
    np.testing.assert_array_equal(result, expected_result)

# Rounding to Nearest methods
def test_half_up_method_positive_numbers():
    input_array = np.array([3.7, 2.2, 5.9, 2.5])
    expected_result = np.array([4, 2, 6, 3])  # Round up for positive numbers
    result = rounding(input_array, 'HalfUp')
    np.testing.assert_array_equal(result, expected_result)


def test_half_up_method_negative_numbers():
    input_array = np.array([-3.7, -2.2, -5.9, -3.5])
    expected_result = np.array([-4, -2, -6, -3])  # No change for negative numbers
    result = rounding(input_array, 'HalfUp')
    np.testing.assert_array_equal(result, expected_result)


def test_half_up_method_mixed_numbers():
    input_array = np.array([3.7, -2.2, 5.9])
    expected_result = np.array([4, -2, 6])  # Round up for positive, no change for negative
    result = rounding(input_array, 'HalfUp')
    np.testing.assert_array_equal(result, expected_result)


def test_half_up_method_zero():
    input_array = np.array([0.0, 0.5, -0.5])
    expected_result = np.array([0, 1, 0])  # No change for zero
    result = rounding(input_array, 'HalfUp')
    np.testing.assert_array_equal(result, expected_result)


def test_half_down_method_positive_numbers():
    input_array = np.array([3.7, 2.2, 5.9, 10.5])
    expected_result = np.array([4, 2, 6, 10])  # Round down for positive numbers
    result = rounding(input_array, 'HalfDown')
    np.testing.assert_array_equal(result, expected_result)


def test_half_down_method_negative_numbers():
    input_array = np.array([-3.7, -2.2, -5.9, -7.5])
    expected_result = np.array([-4, -2, -6, -8])  # Round down for negative numbers
    result = rounding(input_array, 'HalfDown')
    np.testing.assert_array_equal(result, expected_result)


def test_half_down_method_mixed_numbers():
    input_array = np.array([3.7, -2.2, 5.9, 2.5])
    expected_result = np.array([4, -2, 6, 2])  # Round down for positive, round down for negative
    result = rounding(input_array, 'HalfDown')
    np.testing.assert_array_equal(result, expected_result)


def test_half_down_method_zero():
    input_array = np.array([0.0, 0.5, -0.5])
    expected_result = np.array([0, 0, -1])  # No change for zero
    result = rounding(input_array, 'HalfDown')
    np.testing.assert_array_equal(result, expected_result)


def test_half_towards_zero_method_positive_numbers():
    input_array = np.array([3.7, 2.2, 5.9, 2.5])
    expected_result = np.array([4, 2, 6, 2])  # Round down for positive numbers
    result = rounding(input_array, 'HalfTowardsZero')
    np.testing.assert_array_equal(result, expected_result)


def test_half_towards_zero_method_negative_numbers():
    input_array = np.array([-3.7, -2.2, -5.9, -2.5])
    expected_result = np.array([-4, -2, -6, -2])  # Round down for negative numbers
    result = rounding(input_array, 'HalfTowardsZero')
    np.testing.assert_array_equal(result, expected_result)


def test_half_towards_zero_method_mixed_numbers():
    input_array = np.array([3.7, -2.2, 5.9, 13.5])
    expected_result = np.array([4, -2, 6, 13])  # Round down for positive, round down for negative
    result = rounding(input_array, 'HalfTowardsZero')
    np.testing.assert_array_equal(result, expected_result)


def test_half_towards_zero_method_zero():
    input_array = np.array([0.0, 0.5, -0.5])
    expected_result = np.array([0, 0, 0])  # No change for zero
    result = rounding(input_array, 'HalfTowardsZero')
    np.testing.assert_array_equal(result, expected_result)


def test_half_away_from_zero_method_positive_numbers():
    input_array = np.array([3.7, 2.2, 5.5])
    expected_result = np.array([4, 2, 6])  # Round up for positive numbers
    result = rounding(input_array, 'HalfAwayFromZero')
    np.testing.assert_array_equal(result, expected_result)


def test_half_away_from_zero_method_negative_numbers():
    input_array = np.array([-3.7, -2.5, -5.9])
    expected_result = np.array([-4, -3, -6])  # Round down for negative numbers
    result = rounding(input_array, 'HalfAwayFromZero')
    np.testing.assert_array_equal(result, expected_result)


def test_half_away_from_zero_method_mixed_numbers():
    input_array = np.array([3.5, -2.2, 5.9])
    expected_result = np.array([4, -2, 6])  # Round up for positive, round down for negative
    result = rounding(input_array, 'HalfAwayFromZero')
    np.testing.assert_array_equal(result, expected_result)


def test_half_away_from_zero_method_zero():
    input_array = np.array([0.0, 0.5, -0.5])
    expected_result = np.array([0, 1, -1])  # Round up for positive zero, round down for negative zero
    result = rounding(input_array, 'HalfAwayFromZero')
    np.testing.assert_array_equal(result, expected_result)


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
