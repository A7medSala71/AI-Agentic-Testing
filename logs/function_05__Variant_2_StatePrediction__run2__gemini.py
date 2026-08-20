import pytest
from function_05 import median


def test_median_odd_length():
    assert median([1, 3, 2]) == 2


def test_median_even_length():
    assert median([1, 2, 3, 4]) == pytest.approx(2.5)


def test_median_single_element():
    assert median([42]) == 42


def test_median_negative_numbers():
    assert median([-5, -1, -3]) == -3


def test_median_mixed_numbers():
    assert median([-2, 0, 2, 4]) == pytest.approx(1.0)


def test_median_unsorted_input():
    assert median([10, 1, 5, 20, 3]) == 5


def test_median_empty_list():
    import pytest
    with pytest.raises(IndexError):
        median([])
