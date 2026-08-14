import pytest
from function_05 import median


def test_median_odd_length():
    assert median([1, 3, 2]) == 2


def test_median_even_length():
    assert median([1, 2, 3, 4]) == 2.5


def test_median_single_element():
    assert median([42]) == 42


def test_median_unsorted_negative_numbers():
    assert median([-5, 0, -10, 3, 2]) == 0


def test_median_empty_list():
    with pytest.raises(IndexError):
        median([])


def test_median_floats():
    assert median([1.5, 2.5, 3.5]) == pytest.approx(2.5)


def test_median_duplicates():
    assert median([2, 2, 10, 2]) == 6.0
