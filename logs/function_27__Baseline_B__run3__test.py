import pytest
from function_27 import Point, distance


def test_point_initialization_and_repr():
    p = Point(1, 2, 3)
    assert p.x == 1
    assert p.y == 2
    assert p.z == 3
    assert repr(p) == 'Point(1, 2, 3)'


def test_distance_same_point():
    p = Point(0, 0, 0)
    assert distance(p, p) == pytest.approx(0.0)


def test_distance_nominal():
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 15)
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_negative_coordinates():
    p1 = Point(-1, -2, -3)
    p2 = Point(-4, -6, -15)
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_floats():
    p1 = Point(0.5, 1.5, 2.5)
    p2 = Point(1.5, 2.5, 3.5)
    assert distance(p1, p2) == pytest.approx(1.7320508075688772)


def test_distance_mixed_signs_and_zeros():
    p1 = Point(0, -3, 4)
    p2 = Point(0, 0, 0)
    # dx = 0, dy = 3, dz = -4 -> dy^2 + dz^2 = 25 -> sqrt(25) = 5.0
    assert distance(p1, p2) == pytest.approx(5.0)
