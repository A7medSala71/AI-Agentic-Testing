import pytest
from function_27 import Point
from function_27 import distance


def test_point_init_and_repr():
    p = Point(1.0, 2.5, -3)
    assert p.x == 1.0
    assert p.y == 2.5
    assert p.z == -3
    assert repr(p) == "Point(1.0, 2.5, -3)"


def test_distance_zero():
    p1 = Point(0, 0, 0)
    p2 = Point(0, 0, 0)
    assert distance(p1, p2) == pytest.approx(0.0)


def test_distance_nominal():
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 15)
    # dx=3, dy=4, dz=12 -> 9 + 16 + 144 = 169 -> sqrt(169) = 13
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_negative_coordinates():
    p1 = Point(-1, -2, -3)
    p2 = Point(-4, -6, -15)
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_floats():
    p1 = Point(0.5, 1.5, 2.5)
    p2 = Point(1.5, 2.5, 3.5)
    # dx=1, dy=1, dz=1 -> 1 + 1 + 1 = 3 -> sqrt(3)
    assert distance(p1, p2) == pytest.approx(1.7320508075688772)
