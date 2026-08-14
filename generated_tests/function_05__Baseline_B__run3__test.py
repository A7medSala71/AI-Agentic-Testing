import pytest
from function_05 import median


def test_median_odd_length():
    assert median([1, 3, 2]) == 2
    assert median([5]) == 5
    assert median([-5, 0, 5]) == 0


def test_median_even_length():
    assert median([1, 2, 3, 4]) == 2.5
    assert median([2, 4]) == 3.0
    assert median([-2, 2]) == 0.0


def test_median_unsorted_input():
    assert median([3, 1, 4, 1, 5, 9, 2, 6]) == 3.5
    assert median([10, -1, 5]) == 5


def test_median_float_values():
    assert median([1.5, 2.5, 3.5]) == pytest.approx(2.5)
    assert median([1.0, 2.0]) == pytest.approx(1.5)
    assert median([-1.5, 1.5]) == pytest.approx(0.0)


def test_median_empty_list_error():
    with pytest.raises(IndexError):
        median([])


def test_median_duplicates():
    assert median([2, 2, 2, 2]) == 2
    assert median([1, 2, 2, 3]) == 2.0
