from function_13 import heapify
from function_13 import heap_sort


def test_heapify_nominal():
    arr = [3, 9, 2, 1, 4, 5]
    heapify(arr, 0, len(arr))
    assert arr == [9, 4, 2, 1, 3, 5]


def test_heapify_left_larger():
    arr = [1, 5, 2]
    heapify(arr, 0, 3)
    assert arr == [5, 1, 2]


def test_heapify_right_larger():
    arr = [1, 2, 5]
    heapify(arr, 0, 3)
    assert arr == [5, 2, 1]


def test_heapify_boundary_heap_size():
    arr = [1, 10, 20]
    heapify(arr, 0, 2)
    assert arr == [10, 1, 20]


def test_heapify_recursive_call():
    arr = [1, 3, 5, 7, 9]
    heapify(arr, 0, len(arr))
    assert arr == [9, 7, 5, 1, 3]


def test_heapify_already_heapified():
    arr = [9, 5, 2]
    heapify(arr, 0, 3)
    assert arr == [9, 5, 2]


def test_heap_sort_nominal():
    arr = [64, 34, 25, 12, 22, 11, 90]
    res = heap_sort(arr)
    assert res == [11, 12, 22, 25, 34, 64, 90]


def test_heap_sort_empty():
    arr = []
    res = heap_sort(arr)
    assert res == []


def test_heap_sort_single_element():
    arr = [42]
    res = heap_sort(arr)
    assert res == [42]


def test_heap_sort_duplicates():
    arr = [5, 1, 3, 5, 2, 1]
    res = heap_sort(arr)
    assert res == [1, 1, 2, 3, 5, 5]


def test_heap_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    res = heap_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_heap_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
    res = heap_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_heap_sort_negative_numbers():
    arr = [-3, -1, -5, 2, 0]
    res = heap_sort(arr)
    assert res == [-5, -3, -1, 0, 2]
