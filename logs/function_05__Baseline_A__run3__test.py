import pytest
from function_05 import median


def test_median_empty_list():
    with pytest.raises(IndexError):
        median([])


def test_median_single_element():
    assert median([5]) == 5


def test_median_odd_length():
    assert median([3, 1, 2]) == 2
    assert median([10, 2, 5, 1, 9]) == 5


def test_median_even_length():
    assert median([1, 2, 3, 4]) == 2.5
    assert median([10, 20, 30, 40, 50, 60]) == 35.0


def test_median_unsorted_and_duplicates():
    assert median([5, 1, 5, 3, 3]) == 3
    assert median([2, 2, 2, 2]) == 2


def test_median_negative_numbers():
    assert median([-1, -5, -3]) == -3
    assert median([-1, -2, -3, -4]) == -2.5
