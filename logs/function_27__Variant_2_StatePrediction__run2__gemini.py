import pytest
from function_27 import Point
from function_27 import distance


def test_point_init_and_repr():
    p = Point(1.0, 2.5, -3.2)
    assert p.x == 1.0
    assert p.y == 2.5
    assert p.z == -3.2
    assert repr(p) == 'Point(1.0, 2.5, -3.2)'


def test_distance_same_point():
    p = Point(1, 2, 3)
    assert distance(p, p) == pytest.approx(0.0)


def test_distance_nominal():
    p1 = Point(0, 0, 0)
    p2 = Point(3, 4, 12)
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_negative_coordinates():
    p1 = Point(-1, -2, -3)
    p2 = Point(1, 2, 3)
    expected = math.sqrt(2**2 + 4**2 + 6**2)
    assert distance(p1, p2) == pytest.approx(expected)


def test_distance_asymmetry():
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 15)
    assert distance(p1, p2) == pytest.approx(distance(p2, p1))
