import pytest
from function_14 import insertion_sort, Comparable


def test_insertion_sort_empty_collection():
    collection = []
    result = insertion_sort(collection)
    assert result == []
    assert result is collection


def test_insertion_sort_single_element():
    collection = [42]
    result = insertion_sort(collection)
    assert result == [42]
    assert result is collection


def test_insertion_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    result = insertion_sort(collection)
    assert result == [1, 2, 3, 4, 5]


def test_insertion_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    result = insertion_sort(collection)
    assert result == [1, 2, 3, 4, 5]


def test_insertion_sort_unsorted_with_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    result = insertion_sort(collection)
    assert result == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_insertion_sort_strings():
    collection = ['banana', 'apple', 'cherry', 'date']
    result = insertion_sort(collection)
    assert result == ['apple', 'banana', 'cherry', 'date']


def test_insertion_sort_mutates_in_place():
    collection = [3, 2, 1]
    res = insertion_sort(collection)
    assert collection == [1, 2, 3]
    assert res is collection


def test_insertion_sort_stability_and_duplicates():
    # Tests stability and ensures duplicate elements don't shift unnecessarily (killing <= vs < mutants)
    class Item:
        def __init__(self, value, original_index):
            self.value = value
            self.original_index = original_index

        def __lt__(self, other):
            return self.value < other.value

        def __eq__(self, other):
            return self.value == other.value

        def __repr__(self):
            return f"Item({self.value}, {self.original_index})"

    item1 = Item(2, 1)
    item2 = Item(2, 2)
    collection = [item1, item2]
    result = insertion_sort(collection)
    # If <= is used instead of <, stable sort might reorder or behave incorrectly on equal elements
    assert result[0].original_index == 1
    assert result[1].original_index == 2


def test_insertion_sort_range_start_mutant():
    # Kills mutant where range(1, len(collection)) is mutated to range(len(collection))
    # When insert_index starts at 0, collection[0] < collection[-1] (wrapping around in Python)
    # can trigger incorrect behavior or mutations if not careful.
    # Specifically, a custom object that tracks if __lt__ is called when index is 0.
    class CheckLt:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            return self.val < other.val

    collection = [CheckLt(1)]
    # If range starts at 0, the loop tries to compare collection[0] with collection[-1] (itself)
    # or perform logic on insert_index = 0.
    result = insertion_sort(collection)
    assert len(result) == 1
    assert result[0].val == 1