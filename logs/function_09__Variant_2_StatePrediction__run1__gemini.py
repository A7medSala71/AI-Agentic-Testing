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


def test_binary_insertion_sort_strings():
    collection = ["banana", "apple", "cherry", "date"]
    res = binary_insertion_sort(collection)
    assert res == ["apple", "banana", "cherry", "date"]


def test_binary_insertion_sort_mutates_in_place():
    collection = [3, 1, 2]
    res = binary_insertion_sort(collection)
    assert res is collection
    assert res == [1, 2, 3]


def test_binary_insertion_sort_range_starts_at_zero():
    # Mutant mutmut_4: if range starts at 0, i=0 does value_to_insert = collection[0] and tries to insert it, shifting collection[0] incorrectly.
    # State divergence: collection[0] might be overwritten or duplicated incorrectly if i=0 runs.
    collection = [10, 5]
    res = binary_insertion_sort(collection)
    assert res == [5, 10]


def test_binary_insertion_sort_conditional_boundary_duplicates():
    # Mutant mutmut_18: value_to_insert <= collection[mid] instead of <.
    # State divergence: when value_to_insert equals collection[mid], it treats it as smaller and inserts to the left, breaking stability for duplicates.
    # We can check stability by inserting an object or struct, or simply verifying duplicate order stability.
    # Let's use a list of objects or tuples where the second element distinguishes equal keys.
    # E.g., sorting by first element: (2, 'a'), (2, 'b') should stay (2, 'a'), (2, 'b').
    collection = [(2, 'a'), (2, 'b')]
    res = binary_insertion_sort(collection)
    assert res == [(2, 'a'), (2, 'b')]