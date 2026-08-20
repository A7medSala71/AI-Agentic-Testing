import pytest
from function_17 import quick_sort


def test_quick_sort_empty():
    assert quick_sort([]) == []


def test_quick_sort_single_element():
    assert quick_sort([42]) == [42]


def test_quick_sort_already_sorted():
    assert quick_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_quick_sort_reverse_sorted():
    assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_quick_sort_duplicates():
    assert quick_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_quick_sort_negative_numbers():
    assert quick_sort([-3, -1, -4, 0, 2]) == [-4, -3, -1, 0, 2]


def test_quick_sort_floats():
    assert quick_sort([3.14, 1.41, 2.71, 0.5]) == [0.5, 1.41, 2.71, 3.14]
