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


def test_median_unsorted_input():
    assert median([4, 1, 3, 2]) == 2.5
    assert median([9, 0, 5, 2, 7]) == 5


def test_median_duplicate_values():
    assert median([2, 2, 2, 2]) == 2
    assert median([1, 2, 2, 3]) == 2.0
    assert median([1, 1, 3, 3, 3]) == 3


def test_median_empty_list_error():
    with pytest.raises(IndexError):
        median([])
