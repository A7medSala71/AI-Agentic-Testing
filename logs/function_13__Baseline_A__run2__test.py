from function_13 import heapify
from function_13 import heap_sort


def test_heapify_nominal():
    arr = [3, 9, 2, 1, 4, 5]
    heapify(arr, 0, len(arr))
    assert arr == [9, 4, 2, 1, 3, 5]


def test_heapify_boundary_left_larger():
    arr = [1, 5, 2]
    heapify(arr, 0, 3)
    assert arr == [5, 1, 2]


def test_heapify_boundary_right_larger():
    arr = [1, 2, 5]
    heapify(arr, 0, 3)
    assert arr == [5, 2, 1]


def test_heapify_recursive_step():
    arr = [1, 9, 2, 10, 4, 5]
    heapify(arr, 0, len(arr))
    assert arr[0] == 10
    assert arr[3] == 1


def test_heapify_out_of_bounds_heap_size():
    arr = [10, 9, 2]
    heapify(arr, 0, 1)
    assert arr == [10, 9, 2]


def test_heap_sort_nominal():
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = heap_sort(arr)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


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
