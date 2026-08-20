import pytest
from function_23 import quick_select, median, _partition


def test_partition_basic():
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    less, equal, greater = _partition(data, 4)
    assert sorted(less) == [1, 1, 2, 3]
    assert sorted(equal) == [4]
    assert sorted(greater) == [5, 6, 9]


def test_quick_select_bounds_error():
    items = [10, 20, 30]
    assert quick_select(items, -1) is None
    assert quick_select(items, 3) is None
    assert quick_select(items, 100) is None


def test_quick_select_nominal():
    items = [7, 2, 1, 6, 8, 5, 3, 4]
    sorted_items = sorted(items)
    for i in range(len(items)):
        assert quick_select(items, i) == sorted_items[i]


def test_quick_select_duplicates():
    items = [5, 1, 5, 3, 5, 2, 5]
    sorted_items = sorted(items)
    for i in range(len(items)):
        assert quick_select(items, i) == sorted_items[i]


def test_median_odd_length():
    items = [3, 1, 4, 1, 5]
    assert median(items) == 3


def test_median_even_length():
    items = [3, 1, 4, 2]
    assert median(items) == 2.5


def test_median_single_element():
    items = [42]
    assert median(items) == 42
