import pytest
from math import pi
from function_02 import radians


def test_radians_zero():
    assert radians(0.0) == pytest.approx(0.0)


def test_radians_positive_standard():
    assert radians(180.0) == pytest.approx(pi)


def test_radians_negative_standard():
    assert radians(-180.0) == pytest.approx(-pi)


def test_radians_fractional():
    assert radians(90.0) == pytest.approx(pi / 2)
