import pytest
from function_27 import Point, distance


def test_point_initialization_and_repr():
    p = Point(1, 2.5, -3)
    assert p.x == 1
    assert p.y == 2.5
    assert p.z == -3
    assert repr(p) == "Point(1, 2.5, -3)"


def test_distance_same_point():
    p = Point(0, 0, 0)
    assert distance(p, p) == pytest.approx(0.0)


def test_distance_standard_case():
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 15)
    # dx = 3, dy = 4, dz = 12 -> 9 + 16 + 144 = 169 -> sqrt(169) = 13
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_negative_coordinates():
    p1 = Point(-1, -2, -3)
    p2 = Point(2, 2, 9)
    # dx = 3, dy = 4, dz = 12 -> sqrt(9 + 16 + 144) = 13
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_asymmetry_robustness():
    p1 = Point(0, 0, 0)
    p2 = Point(1, 2, 2)
    assert distance(p1, p2) == pytest.approx(distance(p2, p1))
