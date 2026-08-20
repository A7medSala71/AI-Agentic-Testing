import pytest
from function_27 import Point
from function_27 import distance


def test_point_init_and_repr():
    p = Point(1, 2, 3)
    assert p.x == 1
    assert p.y == 2
    assert p.z == 3
    assert repr(p) == "Point(1, 2, 3)"


def test_distance_same_point():
    p1 = Point(0, 0, 0)
    p2 = Point(0, 0, 0)
    assert distance(p1, p2) == pytest.approx(0.0)


def test_distance_axis_aligned():
    p1 = Point(1, 2, 3)
    p2 = Point(4, 2, 3)
    assert distance(p1, p2) == pytest.approx(3.0)


def test_distance_three_dimensions():
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 15)
    # dx = 3, dy = 4, dz = 12 -> sqrt(9 + 16 + 144) = sqrt(169) = 13
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_negative_coordinates():
    p1 = Point(-1, -2, -3)
    p2 = Point(-4, -6, -15)
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_float_coordinates():
    p1 = Point(0.0, 0.0, 0.0)
    p2 = Point(1.0, 2.0, 2.0)
    # sqrt(1 + 4 + 4) = sqrt(9) = 3
    assert distance(p1, p2) == pytest.approx(3.0)
