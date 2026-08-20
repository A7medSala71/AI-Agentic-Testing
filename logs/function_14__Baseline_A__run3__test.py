from function_14 import insertion_sort
from function_14 import Comparable


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
    assert collection is collection


def test_insertion_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert insertion_sort(collection) == [1, 2, 3, 4, 5]


def test_insertion_sort_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    assert insertion_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_insertion_sort_strings():
    collection = ['banana', 'apple', 'cherry', 'date']
    assert insertion_sort(collection) == ['apple', 'banana', 'cherry', 'date']


def test_comparable_protocol():
    class Dummy:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            return self.val < other.val

    d1 = Dummy(1)
    d2 = Dummy(2)
    assert isinstance(d1, Comparable)
    collection = [Dummy(3), Dummy(1), Dummy(2)]
    sorted_coll = insertion_sort(collection)
    assert [x.val for x in sorted_coll] == [1, 2, 3]
