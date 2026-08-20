import pytest
from function_09 import binary_insertion_sort


def test_binary_insertion_sort_empty():
    collection = []
    res = binary_insertion_sort(collection)
    assert res == []
    assert res is collection


def test_binary_insertion_sort_single_element():
    collection = [42]
    res = binary_insertion_sort(collection)
    assert res == [42]
    assert res is collection


def test_binary_insertion_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    res = binary_insertion_sort(collection)
    assert res == [1, 2, 3, 4, 5]
    assert res is collection


def test_binary_insertion_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    res = binary_insertion_sort(collection)
    assert res == [1, 2, 3, 4, 5]
    assert res is collection


def test_binary_insertion_sort_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = binary_insertion_sort(collection)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    assert res is collection


def test_binary_insertion_sort_negative_numbers():
    collection = [-3, 5, 0, -1, 2]
    res = binary_insertion_sort(collection)
    assert res == [-3, -1, 0, 2, 5]
    assert res is collection


def test_binary_insertion_sort_strings():
    collection = ["banana", "apple", "cherry", "date"]
    res = binary_insertion_sort(collection)
    assert res == ["apple", "banana", "cherry", "date"]
    assert res is collection


def test_binary_insertion_sort_mutation_boundaries_low_high():
    collection = [2, 1, 3]
    res = binary_insertion_sort(collection)
    assert res == [1, 2, 3]
