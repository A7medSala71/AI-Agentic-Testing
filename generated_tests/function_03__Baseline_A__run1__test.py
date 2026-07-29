import pytest
from math import pi
from function_03 import arc_length


def test_arc_length_full_circle():
    assert arc_length(360, 1) == pytest.approx(2 * pi)


def test_arc_length_half_circle():
    assert arc_length(180, 5) == pytest.approx(5 * pi)


def test_arc_length_quarter_circle():
    assert arc_length(90, 2) == pytest.approx(pi)


def test_arc_length_zero_angle():
    assert arc_length(0, 10) == pytest.approx(0.0)


def test_arc_length_zero_radius():
    assert arc_length(120, 0) == pytest.approx(0.0)


def test_arc_length_negative_angle():
    assert arc_length(-90, 2) == pytest.approx(-pi)


def test_arc_length_negative_radius():
    assert arc_length(180, -3) == pytest.approx(-3 * pi)


def test_arc_length_multi_turn_angle():
    assert arc_length(720, 1) == pytest.approx(4 * pi)
