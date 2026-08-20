import pytest
from function_13 import heapify, heap_sort


def test_heapify_basic_left_largest():
    arr = [1, 5, 3]
    heapify(arr, 0, 3)
    assert arr == [5, 1, 3]


def test_heapify_basic_right_largest():
    arr = [1, 3, 5]
    heapify(arr, 0, 3)
    assert arr == [5, 3, 1]


def test_heapify_recursive_step():
    arr = [1, 10, 5, 20, 2]
    # index 0, left is 10 (idx 1), right is 5 (idx 2). Left is largest (10).
    # After swap: [10, 1, 5, 20, 2], then heapify called on index 1.
    # At index 1, left is 20 (idx 3), right is 2 (idx 4). Left is largest (20).
    # After swap: [10, 20, 5, 1, 2]
    heapify(arr, 0, 5)
    assert arr == [10, 20, 5, 1, 2]


def test_heapify_boundary_heap_size():
    arr = [1, 10, 5]
    # heap_size = 2 means only indices 0 and 1 are considered. Left is 10, right is out of bounds.
    heapify(arr, 0, 2)
    assert arr == [10, 1, 5]


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


def test_heap_sort_negative_numbers():
    arr = [-3, 5, 0, -1, 2, -5]
    res = heap_sort(arr)
    assert res == [-5, -3, -1, 0, 2, 5]
