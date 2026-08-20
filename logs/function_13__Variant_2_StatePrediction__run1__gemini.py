import pytest
from function_13 import heapify, heap_sort


def test_heapify_basic():
    arr = [3, 9, 2, 1, 4, 5]
    heapify(arr, 0, len(arr))
    assert arr == [9, 3, 2, 1, 4, 5]


def test_heapify_right_child_larger():
    arr = [3, 2, 9, 1, 4, 5]
    heapify(arr, 0, len(arr))
    assert arr == [9, 2, 3, 1, 4, 5]


def test_heapify_recursive_down():
    arr = [1, 9, 2, 3, 4, 5]
    heapify(arr, 0, len(arr))
    assert arr == [9, 4, 5, 3, 1, 2]


def test_heapify_out_of_bounds_heap_size():
    arr = [1, 9, 2]
    heapify(arr, 0, 2)
    assert arr == [9, 1, 2]


def test_heap_sort_standard():
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


def test_heap_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    res = heap_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_heap_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
    res = heap_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_heap_sort_duplicates():
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = heap_sort(arr)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
