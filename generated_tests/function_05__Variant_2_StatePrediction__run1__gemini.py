import pytest
from function_05 import median


def test_median_empty_list():
    with pytest.raises(IndexError):
        median([])


def test_median_single_element():
    assert median([5]) == 5


def test_median_odd_length():
    assert median([3, 1, 2]) == 2
    assert median([10, 2, 5, 8, 1]) == 5


def test_median_even_length():
    assert median([1, 2, 3, 4]) == pytest.approx(2.5)
    assert median([10, 20, 30, 40, 50, 60]) == pytest.approx(35.0)


def test_median_negative_numbers():
    assert median([-5, -1, -3]) == -3
    assert median([-10, -20, 10, 20]) == pytest.approx(0.0)


def test_median_duplicate_values():
    assert median([2, 2, 2, 2]) == 2
    assert median([1, 2, 2, 3]) == pytest.approx(2.0)


def test_median_unsorted_floats():
    assert median([1.5, 2.5, 3.5]) == pytest.approx(2.5)
    assert median([1.1, 2.2, 3.3, 4.4]) == pytest.approx(2.75)
