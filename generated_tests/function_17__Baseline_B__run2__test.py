from function_17 import quick_sort
import pytest


def test_quick_sort_empty_and_single():
    assert quick_sort([]) == []
    assert quick_sort([42]) == [42]


def test_quick_sort_sorted_and_reverse():
    assert quick_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_quick_sort_duplicates_and_negatives():
    assert quick_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    assert quick_sort([-5, 0, -2, 3, 1]) == [-5, -2, 0, 1, 3]


def test_quick_sort_strings():
    assert quick_sort(["banana", "apple", "cherry"]) == ["apple", "banana", "cherry"]


def test_quick_sort_floats():
    assert quick_sort([3.5, 1.1, 4.2, 2.0]) == [1.1, 2.0, 3.5, 4.2]


def test_quick_sort_mixed_types_raises_type_error():
    with pytest.raises(TypeError):
        quick_sort([1, "string"])
