from function_14 import insertion_sort
from collections.abc import MutableSequence


def test_insertion_sort_empty():
    collection = []
    assert insertion_sort(collection) == []
    assert collection == []


def test_insertion_sort_single_element():
    collection = [42]
    assert insertion_sort(collection) == [42]
    assert collection == [42]


def test_insertion_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    assert insertion_sort(collection) == [1, 2, 3, 4, 5]
    assert collection == [1, 2, 3, 4, 5]


def test_insertion_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert insertion_sort(collection) == [1, 2, 3, 4, 5]
    assert collection == [1, 2, 3, 4, 5]


def test_insertion_sort_random_order():
    collection = [3, 1, 4, 1, 5, 9, 2, 6]
    assert insertion_sort(collection) == [1, 1, 2, 3, 4, 5, 6, 9]
    assert collection == [1, 1, 2, 3, 4, 5, 6, 9]


def test_insertion_sort_mutation_check():
    collection = [2, 1]
    res = insertion_sort(collection)
    assert res is collection


def test_comparable_protocol():
    class Dummy:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            return self.val < other.val
    
    collection = [Dummy(3), Dummy(1), Dummy(2)]
    sorted_col = insertion_sort(collection)
    assert [x.val for x in sorted_col] == [1, 2, 3]


def test_insertion_sort_negative_and_floats():
    collection = [3.5, -1.2, 0, 2.1, -5.0]
    assert insertion_sort(collection) == [-5.0, -1.2, 0, 2.1, 3.5]


def test_insertion_sort_identical_elements():
    collection = [7, 7, 7, 7]
    assert insertion_sort(collection) == [7, 7, 7, 7]
    assert collection == [7, 7, 7, 7]
