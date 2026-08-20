import pytest
from function_14 import insertion_sort, Comparable


def test_insertion_sort_empty():
    collection = []
    assert insertion_sort(collection) == []


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
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    assert insertion_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]


def test_insertion_sort_strings():
    collection = ['banana', 'apple', 'cherry', 'date']
    assert insertion_sort(collection) == ['apple', 'banana', 'cherry', 'date']


def test_insertion_sort_mutates_in_place():
    collection = [3, 1, 2]
    res = insertion_sort(collection)
    assert res is collection
    assert collection == [1, 2, 3]


def test_comparable_protocol():
    class CustomItem:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            return self.val < other.val
        def __eq__(self, other):
            return self.val == other.val
    
    c1 = CustomItem(2)
    c2 = CustomItem(1)
    assert isinstance(c2, Comparable)
    collection = [c1, c2]
    sorted_coll = insertion_sort(collection)
    assert sorted_coll[0].val == 1
    assert sorted_coll[1].val == 2
