import pytest
from function_27 import Point, distance


def test_point_initialization_and_repr():
    p = Point(1.0, 2.5, -3)
    assert p.x == 1.0
    assert p.y == 2.5
    assert p.z == -3
    assert repr(p) == "Point(1.0, 2.5, -3)"


def test_distance_same_point():
    p1 = Point(0, 0, 0)
    assert distance(p1, p1) == pytest.approx(0.0)


def test_distance_axis_aligned():
    p1 = Point(0, 0, 0)
    p2 = Point(3, 0, 0)
    p3 = Point(0, -4, 0)
    p4 = Point(0, 0, 5)
    assert distance(p1, p2) == pytest.approx(3.0)
    assert distance(p1, p3) == pytest.approx(4.0)
    assert distance(p1, p4) == pytest.approx(5.0)


def test_distance_arbitrary_points():
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 15)
    # dx=3, dy=4, dz=12 -> sqrt(9 + 16 + 144) = sqrt(169) = 13
    assert distance(p1, p2) == pytest.approx(13.0)
    assert distance(p2, p1) == pytest.approx(13.0)


def test_distance_negative_coordinates():
    p1 = Point(-1, -2, -3)
    p2 = Point(-4, -6, -15)
    assert distance(p1, p2) == pytest.approx(13.0)


def test_distance_floats():
    p1 = Point(0.5, 1.5, 2.5)
    p2 = Point(1.5, 3.5, 4.5)
    # dx=1, dy=2, dz=2 -> sqrt(1 + 4 + 4) = sqrt(9) = 3
    assert distance(p1, p2) == pytest.approx(3.0)
