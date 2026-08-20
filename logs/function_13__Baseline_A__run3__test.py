import pytest
from function_13 import heapify, heap_sort


def test_heapify_left_larger():
    arr = [1, 5, 3]
    heapify(arr, 0, 3)
    assert arr == [5, 1, 3]


def test_heapify_right_larger():
    arr = [1, 3, 5]
    heapify(arr, 0, 3)
    assert arr == [5, 3, 1]


def test_heapify_recursive_down():
    arr = [1, 10, 5, 2, 3]
    heapify(arr, 0, 5)
    assert arr == [10, 3, 5, 2, 1]


def test_heapify_already_heap():
    arr = [10, 5, 3]
    heapify(arr, 0, 3)
    assert arr == [10, 5, 3]


def test_heapify_out_of_bounds_size():
    arr = [1, 10, 20]
    heapify(arr, 0, 1)
    assert arr == [1, 10, 20]


def test_heap_sort_nominal():
    arr = [4, 10, 3, 5, 1]
    res = heap_sort(arr)
    assert res == [1, 3, 4, 5, 10]


def test_heap_sort_empty():
    arr = []
    res = heap_sort(arr)
    assert res == []


def test_heap_sort_single_element():
    arr = [42]
    res = heap_sort(arr)
    assert res == [42]


def test_heap_sort_duplicates_and_negatives():
    arr = [-3, 5, 2, -3, 0, 5, 1]
    res = heap_sort(arr)
    assert res == [-3, -3, 0, 1, 2, 5, 5]
