import pytest
from math import pi
from function_03 import arc_length


def test_arc_length_zero_angle():
    assert arc_length(0, 5) == pytest.approx(0.0)


def test_arc_length_zero_radius():
    assert arc_length(90, 0) == pytest.approx(0.0)


def test_arc_length_full_circle():
    assert arc_length(360, 10) == pytest.approx(2 * pi * 10)


def test_arc_length_fractional():
    assert arc_length(90, 4) == pytest.approx(2 * pi * 4 * (90 / 360))


def test_arc_length_negative_angle():
    assert arc_length(-180, 5) == pytest.approx(2 * pi * 5 * (-180 / 360))


def test_arc_length_negative_radius():
    assert arc_length(180, -5) == pytest.approx(2 * pi * -5 * (180 / 360))
