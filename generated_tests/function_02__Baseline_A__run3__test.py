import pytest
from math import pi
from function_02 import radians


def test_radians_zero():
    assert radians(0.0) == pytest.approx(0.0)


def test_radians_positive_nominal():
    assert radians(180.0) == pytest.approx(pi)


def test_radians_complete_circle():
    assert radians(360.0) == pytest.approx(2 * pi)


def test_radians_negative():
    assert radians(-180.0) == pytest.approx(-pi)


def test_radians_arbitrary_value():
    assert radians(90.0) == pytest.approx(pi / 2)
