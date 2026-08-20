import pytest
from function_28 import sin


def test_sin_zero():
    assert sin(0.0) == 0.0


def test_sin_standard_angles():
    assert sin(30.0) == 0.5
    assert sin(90.0) == 1.0
    assert sin(180.0) == 0.0
    assert sin(270.0) == -1.0
    assert sin(360.0) == 0.0


def test_sin_negative_angles():
    assert sin(-30.0) == -0.5
    assert sin(-90.0) == -1.0


def test_sin_large_angles():
    assert sin(390.0) == 0.5
    assert sin(-330.0) == 0.5


def test_sin_custom_accuracy():
    res_low = sin(30.0, accuracy=1)
    res_high = sin(30.0, accuracy=10)
    assert res_low != res_high


def test_sin_custom_rounding():
    res = sin(45.0, rounded_values_count=2)
    assert res == 0.71
