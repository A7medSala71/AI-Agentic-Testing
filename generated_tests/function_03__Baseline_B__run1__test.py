import pytest
from function_03 import arc_length
from math import pi


def test_arc_length_zero_angle():
    assert arc_length(0, 5) == pytest.approx(0.0)


def test_arc_length_zero_radius():
    assert arc_length(180, 0) == pytest.approx(0.0)


def test_arc_length_full_circle():
    assert arc_length(360, 10) == pytest.approx(2 * pi * 10)


def test_arc_length_semi_circle():
    assert arc_length(180, 7) == pytest.approx(pi * 7)


def test_arc_length_arbitrary():
    assert arc_length(90, 4) == pytest.approx(2 * pi * 4 * (90 / 360))


def test_arc_length_negative_angle():
    assert arc_length(-90, 4) == pytest.approx(-2 * pi * 4 * (90 / 360))


def test_arc_length_negative_radius():
    assert arc_length(90, -4) == pytest.approx(2 * pi * -4 * (90 / 360))


def test_arc_length_angle_greater_than_360():
    assert arc_length(720, 5) == pytest.approx(2 * pi * 5 * (720 / 360))
