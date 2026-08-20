import pytest
from function_14 import Comparable, insertion_sort


def test_insertion_sort_empty():
    collection = []
    res = insertion_sort(collection)
    assert res == []


def test_insertion_sort_single_element():
    collection = [42]
    res = insertion_sort(collection)
    assert res == [42]


def test_insertion_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    res = insertion_sort(collection)
    assert res == [1, 2, 3, 4, 5]


def test_insertion_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    res = insertion_sort(collection)
    assert res == [1, 2, 3, 4, 5]


def test_insertion_sort_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    res = insertion_sort(collection)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]


def test_insertion_sort_floats_and_negative():
    collection = [-1.5, 2.0, 0, -3.2, 2.0]
    res = insertion_sort(collection)
    assert res == [-3.2, -1.5, 0, 2.0, 2.0]


def test_comparable_protocol_runtime():
    class Dummy:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            return self.val < other.val

    d1 = Dummy(1)
    d2 = Dummy(2)
    assert isinstance(d1, Comparable)
    assert (d1 < d2) is True
    
    collection = [Dummy(3), Dummy(1), Dummy(2)]
    res = insertion_sort(collection)
    assert [x.val for x in res] == [1, 2, 3]
