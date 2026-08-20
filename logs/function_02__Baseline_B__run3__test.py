import pytest
from math import pi
from function_02 import radians


def test_radians_zero():
    assert radians(0.0) == pytest.approx(0.0)


def test_radians_positive_standard():
    assert radians(180.0) == pytest.approx(pi)


def test_radians_positive_360():
    assert radians(360.0) == pytest.approx(2 * pi)


def test_radians_negative():
    assert radians(-180.0) == pytest.approx(-pi)


def test_radians_fractional():
    assert radians(90.0) == pytest.approx(pi / 2)


def test_radians_integer_input():
    assert radians(180) == pytest.approx(pi)


def test_radians_large_float():
    assert radians(1e6) == pytest.approx(1e6 / (180 / pi))
