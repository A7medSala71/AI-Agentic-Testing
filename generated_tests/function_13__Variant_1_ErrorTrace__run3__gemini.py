from function_13 import heapify, heap_sort
import pytest


def test_heapify_left_largest():
    arr = [2, 5, 3]
    heapify(arr, 0, 3)
    assert arr == [5, 2, 3]


def test_heapify_right_largest():
    arr = [2, 3, 5]
    heapify(arr, 0, 3)
    assert arr == [5, 3, 2]


def test_heapify_root_largest():
    arr = [5, 2, 3]
    heapify(arr, 0, 3)
    assert arr == [5, 2, 3]


def test_heapify_recursive_call():
    arr = [1, 3, 5, 7, 9]
    heapify(arr, 0, 5)
    assert arr[0] == 9


def test_heapify_boundary_heap_size():
    arr = [1, 10, 2]
    heapify(arr, 0, 2)
    assert arr == [10, 1, 2]


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
    arr = [-3, -1, -4, 0, 5, 2]
    res = heap_sort(arr)
    assert res == [-4, -3, -1, 0, 2, 5]
