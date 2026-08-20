import pytest
from function_03 import arc_length


def test_arc_length_zero_angle():
    assert arc_length(0, 5) == pytest.approx(0.0)


def test_arc_length_zero_radius():
    assert arc_length(90, 0) == pytest.approx(0.0)


def test_arc_length_full_circle():
    assert arc_length(360, 10) == pytest.approx(62.83185307179586)


def test_arc_length_quarter_circle():
    assert arc_length(90, 10) == pytest.approx(15.707963267948966)


def test_arc_length_negative_angle():
    assert arc_length(-90, 10) == pytest.approx(-15.707963267948966)


def test_arc_length_negative_radius():
    assert arc_length(90, -10) == pytest.approx(-15.707963267948966)


def test_arc_length_greater_than_360():
    assert arc_length(720, 10) == pytest.approx(125.66370614359172)
