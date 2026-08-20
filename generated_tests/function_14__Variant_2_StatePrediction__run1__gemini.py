import pytest
from function_14 import insertion_sort, Comparable


def test_insertion_sort_empty():
    collection = []
    assert insertion_sort(collection) == []
    assert collection is collection


def test_insertion_sort_single_element():
    collection = [42]
    assert insertion_sort(collection) == [42]


def test_insertion_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    assert insertion_sort(collection) == [1, 2, 3, 4, 5]


def test_insertion_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert insertion_sort(collection) == [1, 2, 3, 4, 5]


def test_insertion_sort_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    assert insertion_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_insertion_sort_negative_numbers():
    collection = [-3, 5, 0, -1, 2]
    assert insertion_sort(collection) == [-3, -1, 0, 2, 5]


def test_insertion_sort_floats():
    collection = [3.14, 1.41, 2.71, 0.5]
    assert insertion_sort(collection) == [0.5, 1.41, 2.71, 3.14]


def test_insertion_sort_mutation_in_place():
    collection = [3, 1, 2]
    res = insertion_sort(collection)
    assert res is collection
    assert collection == [1, 2, 3]


def test_comparable_protocol():
    class Dummy:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            return self.val < other.val

    d1 = Dummy(1)
    d2 = Dummy(2)
    assert isinstance(d1, Comparable)
    collection = [d2, d1]
    sorted_collection = insertion_sort(collection)
    assert sorted_collection[0].val == 1
    assert sorted_collection[1].val == 2
