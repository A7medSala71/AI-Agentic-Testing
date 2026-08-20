import pytest
from function_03 import arc_length


def test_arc_length_zero_angle():
    assert arc_length(0, 5) == pytest.approx(0.0)


def test_arc_length_zero_radius():
    assert arc_length(180, 0) == pytest.approx(0.0)


def test_arc_length_full_circle():
    assert arc_length(360, 10) == pytest.approx(2 * 3.141592653589793 * 10)


def test_arc_length_half_circle():
    assert arc_length(180, 7) == pytest.approx(3.141592653589793 * 7)


def test_arc_length_arbitrary_values():
    assert arc_length(90, 4) == pytest.approx(2 * 3.141592653589793 * 4 * (90 / 360))


def test_arc_length_negative_angle():
    assert arc_length(-90, 4) == pytest.approx(2 * 3.141592653589793 * 4 * (-90 / 360))


def test_arc_length_negative_radius():
    assert arc_length(90, -4) == pytest.approx(2 * 3.141592653589793 * -4 * (90 / 360))
