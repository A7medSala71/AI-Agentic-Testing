import pytest
from function_28 import sin


def test_sin_zero_degrees():
    assert sin(0.0) == 0.0


def test_sin_standard_angles():
    assert sin(30.0) == pytest.approx(0.5)
    assert sin(90.0) == pytest.approx(1.0)
    assert sin(180.0) == pytest.approx(0.0)
    assert sin(270.0) == pytest.approx(-1.0)
    assert sin(360.0) == pytest.approx(0.0)


def test_sin_negative_angles():
    assert sin(-30.0) == pytest.approx(-0.5)
    assert sin(-90.0) == pytest.approx(-1.0)


def test_sin_large_angles():
    assert sin(390.0) == pytest.approx(0.5)
    assert sin(-330.0) == pytest.approx(0.5)
    assert sin(3600000.0) == pytest.approx(sin(3600000.0 % 360.0))


def test_sin_custom_rounding():
    val = sin(30.0, accuracy=18, rounded_values_count=2)
    assert val == 0.5


def test_sin_custom_accuracy():
    val_low = sin(30.0, accuracy=1, rounded_values_count=10)
    val_high = sin(30.0, accuracy=18, rounded_values_count=10)
    assert val_low != val_high


def test_sin_accuracy_zero():
    val = sin(30.0, accuracy=0, rounded_values_count=10)
    # With accuracy=0, result is radians(30.0) = pi / 6 = 0.5235987756
    assert val == pytest.approx(0.5235987756)


def test_sin_non_integer_degrees():
    val = sin(45.5)
    assert val == pytest.approx(0.7132504489, abs=1e-5)
