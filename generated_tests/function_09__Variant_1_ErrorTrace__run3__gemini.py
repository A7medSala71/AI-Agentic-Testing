import pytest
from function_09 import binary_insertion_sort


def test_binary_insertion_sort_empty():
    collection = []
    res = binary_insertion_sort(collection)
    assert res == []


def test_binary_insertion_sort_single():
    collection = [42]
    res = binary_insertion_sort(collection)
    assert res == [42]


def test_binary_insertion_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    res = binary_insertion_sort(collection)
    assert res == [1, 2, 3, 4, 5]


def test_binary_insertion_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    res = binary_insertion_sort(collection)
    assert res == [1, 2, 3, 4, 5]


def test_binary_insertion_sort_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = binary_insertion_sort(collection)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_binary_insertion_sort_negative_numbers():
    collection = [-3, 5, 0, -1, 2]
    res = binary_insertion_sort(collection)
    assert res == [-3, -1, 0, 2, 5]


def test_binary_insertion_sort_mutates_in_place():
    collection = [3, 1, 2]
    res = binary_insertion_sort(collection)
    assert res is collection
    assert collection == [1, 2, 3]


def test_binary_insertion_sort_with_equal_elements():
    # Kills mutmut_18 (< changed to <=) by testing duplicate elements where 
    # stable insertion order matters (or right insertion position).
    collection = [2, 2, 1]
    res = binary_insertion_sort(collection)
    assert res == [1, 2, 2]