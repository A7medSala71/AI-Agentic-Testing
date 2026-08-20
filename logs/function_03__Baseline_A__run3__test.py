import pytest
from math import pi
from function_03 import arc_length


def test_arc_length_nominal():
    res = arc_length(180, 10)
    assert res == pytest.approx(10 * pi)


def test_arc_length_full_circle():
    res = arc_length(360, 5)
    assert res == pytest.approx(2 * pi * 5)


def test_arc_length_zero_angle():
    res = arc_length(0, 10)
    assert res == pytest.approx(0.0)


def test_arc_length_zero_radius():
    res = arc_length(90, 0)
    assert res == pytest.approx(0.0)


def test_arc_length_negative_angle():
    res = arc_length(-180, 10)
    assert res == pytest.approx(-10 * pi)


def test_arc_length_negative_radius():
    res = arc_length(180, -10)
    assert res == pytest.approx(-10 * pi)
