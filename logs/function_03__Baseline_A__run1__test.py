import pytest
from function_03 import arc_length


def test_arc_length_zero_angle():
    assert arc_length(0, 5) == pytest.approx(0.0)


def test_arc_length_full_circle():
    from math import pi
    assert arc_length(360, 5) == pytest.approx(2 * pi * 5)


def test_arc_length_nominal_case():
    from math import pi
    assert arc_length(180, 10) == pytest.approx(pi * 10)


def test_arc_length_zero_radius():
    assert arc_length(90, 0) == pytest.approx(0.0)


def test_arc_length_negative_angle():
    from math import pi
    assert arc_length(-90, 10) == pytest.approx(-2 * pi * 10 * (90 / 360))


def test_arc_length_negative_radius():
    from math import pi
    assert arc_length(90, -10) == pytest.approx(2 * pi * -10 * (90 / 360))
