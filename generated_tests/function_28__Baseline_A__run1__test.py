import pytest
from function_28 import sin


def test_sin_zero():
    assert sin(0.0) == 0.0


def test_sin_standard_angles():
    assert sin(30.0) == 0.5
    assert sin(90.0) == 1.0
    assert sin(180.0) == 0.0
    assert sin(270.0) == -1.0


def test_sin_normalization_positive():
    assert sin(390.0) == 0.5
    assert sin(720.0) == 0.0


def test_sin_normalization_negative():
    assert sin(-330.0) == 0.5
    assert sin(-90.0) == -1.0


def test_sin_custom_rounded_values_count():
    res = sin(30.0, accuracy=18, rounded_values_count=2)
    assert res == 0.5


def test_sin_low_accuracy():
    res = sin(90.0, accuracy=1, rounded_values_count=10)
    assert res == pytest.approx(1.5707963268, abs=1e-5)
