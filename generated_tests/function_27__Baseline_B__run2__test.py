import pytest
from function_27 import Point
from function_27 import distance


def test_point_init_and_repr():
    p = Point(1.0, 2.5, -3.0)
    assert p.x == 1.0
    assert p.y == 2.5
    assert p.z == -3.0
    assert repr(p) == "Point(1.0, 2.5, -3.0)"


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


def test_distance_asymmetric():
    p1 = Point(0, 0, 0)
    p2 = Point(1, 2, 2)
    assert distance(p1, p2) == pytest.approx(3.0)
    assert distance(p2, p1) == pytest.approx(3.0)


def test_distance_mixed_coordinates():
    p1 = Point(-1, 2, -3)
    p2 = Point(2, -2, 9)
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_float_coordinates():
    p1 = Point(0.0, 0.0, 0.0)
    p2 = Point(0.0, 3.0, 4.0)
    assert distance(p1, p2) == pytest.approx(5.0)
