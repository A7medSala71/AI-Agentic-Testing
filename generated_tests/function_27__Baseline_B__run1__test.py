import pytest
import math
from function_27 import Point
from function_27 import distance


def test_point_init_and_repr():
    p = Point(1.0, 2.5, -3.0)
    assert p.x == 1.0
    assert p.y == 2.5
    assert p.z == -3.0
    assert repr(p) == "Point(1.0, 2.5, -3.0)"


def test_distance_zero():
    p1 = Point(1, 2, 3)
    p2 = Point(1, 2, 3)
    assert distance(p1, p2) == pytest.approx(0.0)


def test_distance_nominal():
    p1 = Point(0, 0, 0)
    p2 = Point(3, 4, 12)
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_negative_coordinates():
    p1 = Point(-1, -2, -3)
    p2 = Point(1, 2, 3)
    assert distance(p1, p2) == pytest.approx(math.sqrt(4 + 16 + 36))


def test_distance_float_coordinates():
    p1 = Point(0.5, 1.5, 2.5)
    p2 = Point(1.5, 3.5, 4.5)
    assert distance(p1, p2) == pytest.approx(math.sqrt(1.0 + 4.0 + 4.0))
