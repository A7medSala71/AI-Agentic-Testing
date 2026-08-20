import pytest
from function_05 import median


def test_median_odd_length():
    assert median([1, 3, 2]) == 2
    assert median([5]) == 5
    assert median([-5, 0, 5]) == 0


def test_median_even_length():
    assert median([1, 2, 3, 4]) == 2.5
    assert median([10, 20]) == 15.0
    assert median([-2, -1, 1, 2]) == 0.0


def test_median_unsorted():
    assert median([3, 1, 4, 1, 5, 9, 2, 6]) == 3.5
    assert median([10, 1, 5]) == 5


def test_median_empty_list():
    with pytest.raises((IndexError, TypeError)):
        median([])
