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
    assert sin(-390.0) == -0.5
    assert sin(750.0) == 0.5


def test_sin_custom_rounding():
    val = sin(30.0, rounded_values_count=2)
    assert val == 0.5


def test_sin_custom_accuracy():
    val_low = sin(30.0, accuracy=1)
    val_high = sin(30.0, accuracy=20)
    assert val_low != val_high


def test_sin_zero_accuracy():
    val = sin(30.0, accuracy=0)
    assert val == 0.5235987756
