import pytest
from function_13 import heapify
from function_13 import heap_sort


def test_heapify_nominal_left():
    arr = [1, 5, 3]
    heapify(arr, 0, 3)
    assert arr == [5, 1, 3]


def test_heapify_nominal_right():
    arr = [1, 3, 5]
    heapify(arr, 0, 3)
    assert arr == [5, 3, 1]


def test_heapify_no_swap_needed():
    arr = [5, 1, 3]
    heapify(arr, 0, 3)
    assert arr == [5, 1, 3]


def test_heapify_boundary_heap_size():
    arr = [1, 5, 10]
    heapify(arr, 0, 2)
    assert arr == [5, 1, 10]


def test_heapify_recursive_step():
    arr = [1, 3, 5, 7, 9]
    heapify(arr, 0, 5)
    assert arr == [9, 3, 5, 7, 1]


def test_heap_sort_nominal():
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    res = heap_sort(arr)
    assert res == [1, 1, 2, 3, 4, 5, 6, 9]


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


def test_heap_sort_negative_numbers():
    arr = [-3, -1, -4, -1, -5, 0, 2]
    res = heap_sort(arr)
    assert res == [-5, -4, -3, -1, -1, 0, 2]
