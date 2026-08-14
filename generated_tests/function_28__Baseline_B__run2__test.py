import pytest
from function_28 import sin


def test_sin_zero():
    assert sin(0.0) == 0.0


def test_sin_nominal_90():
    assert sin(90.0) == 1.0


def test_sin_nominal_180():
    assert sin(180.0) == 0.0


def test_sin_nominal_270():
    assert sin(270.0) == -1.0


def test_sin_normalization_positive():
    assert sin(450.0) == 1.0


def test_sin_normalization_negative():
    assert sin(-270.0) == 1.0


def test_sin_custom_accuracy():
    res_low = sin(30.0, accuracy=1, rounded_values_count=5)
    res_high = sin(30.0, accuracy=10, rounded_values_count=5)
    assert res_low != res_high


def test_sin_custom_rounding():
    val = sin(30.0, rounded_values_count=2)
    assert val == 0.5


def test_sin_negative_angle_non_quadrant():
    assert sin(-30.0) == -0.5


def test_sin_deep_negative_normalization():
    assert sin(-450.0) == -1.0


def test_sin_non_integer_angle():
    assert sin(30.5) == round(0.5075383624, 10)
