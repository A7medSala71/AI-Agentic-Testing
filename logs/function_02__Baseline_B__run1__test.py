import pytest
from math import pi
from function_02 import radians


def test_radians_zero():
    assert radians(0.0) == pytest.approx(0.0)


def test_radians_standard_angles():
    assert radians(180.0) == pytest.approx(pi)
    assert radians(90.0) == pytest.approx(pi / 2.0)
    assert radians(360.0) == pytest.approx(2.0 * pi)


def test_radians_negative_angles():
    assert radians(-180.0) == pytest.approx(-pi)
    assert radians(-90.0) == pytest.approx(-pi / 2.0)


def test_radians_fractional():
    assert radians(45.0) == pytest.approx(pi / 4.0)
    assert radians(57.29577951308232) == pytest.approx(1.0)
