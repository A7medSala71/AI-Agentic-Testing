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
    assert quick_sort([-3, -1, -4, 1, 0]) == [-4, -3, -1, 0, 1]


def test_quick_sort_strings():
    assert quick_sort(["banana", "apple", "cherry"]) == ["apple", "banana", "cherry"]


def test_quick_sort_floats():
    assert quick_sort([3.5, 1.1, 2.2, 0.0]) == [0.0, 1.1, 2.2, 3.5]


def test_quick_sort_type_error():
    with pytest.raises(TypeError):
        quick_sort([1, "two"])
