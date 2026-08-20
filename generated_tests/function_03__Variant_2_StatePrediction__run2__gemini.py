import pytest
from function_03 import arc_length
from math import pi


def test_arc_length_nominal():
    res = arc_length(90, 10)
    assert res == pytest.approx(5.0 * pi)


def test_arc_length_full_circle():
    res = arc_length(360, 5)
    assert res == pytest.approx(10.0 * pi)


def test_arc_length_zero_angle():
    res = arc_length(0, 10)
    assert res == pytest.approx(0.0)


def test_arc_length_zero_radius():
    res = arc_length(180, 0)
    assert res == pytest.approx(0.0)


def test_arc_length_negative_angle():
    res = arc_length(-90, 10)
    assert res == pytest.approx(-5.0 * pi)


def test_arc_length_negative_radius():
    res = arc_length(90, -10)
    assert res == pytest.approx(-5.0 * pi)
