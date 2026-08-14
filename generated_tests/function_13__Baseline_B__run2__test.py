from function_13 import heapify
from function_13 import heap_sort


def test_heapify_left_larger():
    arr = [1, 3, 2]
    heapify(arr, 0, 3)
    assert arr == [3, 1, 2]


def test_heapify_right_larger():
    arr = [1, 2, 3]
    heapify(arr, 0, 3)
    assert arr == [3, 2, 1]


def test_heapify_recursive_call():
    arr = [1, 3, 2, 0, 0]
    heapify(arr, 0, 3)
    assert arr == [3, 1, 2, 0, 0]


def test_heapify_boundary_heap_size():
    arr = [1, 3, 5]
    heapify(arr, 0, 2)
    assert arr == [3, 1, 5]


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


def test_heap_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    res = heap_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_heap_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
    res = heap_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_heap_sort_duplicates():
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    res = heap_sort(arr)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]


def test_heapify_no_swap_needed():
    arr = [5, 3, 2]
    heapify(arr, 0, 3)
    assert arr == [5, 3, 2]


def test_heap_sort_negative_numbers():
    arr = [-3, 5, -1, 0, 2]
    res = heap_sort(arr)
    assert res == [-3, -1, 0, 2, 5]


def test_heapify_recursive_deep():
    arr = [1, 2, 3, 4, 5]
    heapify(arr, 0, 5)
    assert arr == [5, 4, 3, 1, 2]
