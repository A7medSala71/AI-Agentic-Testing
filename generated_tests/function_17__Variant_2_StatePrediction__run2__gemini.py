from function_17 import quick_sort


def test_quick_sort_empty():
    assert quick_sort([]) == []


def test_quick_sort_single_element():
    assert quick_sort([42]) == [42]


def test_quick_sort_two_elements_sorted():
    assert quick_sort([1, 2]) == [1, 2]


def test_quick_sort_two_elements_reversed():
    assert quick_sort([2, 1]) == [1, 2]


def test_quick_sort_nominal():
    assert quick_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]


def test_quick_sort_negative_numbers():
    assert quick_sort([-5, -1, -3, 0, 2, -2]) == [-5, -3, -2, -1, 0, 2]


def test_quick_sort_all_identical():
    assert quick_sort([7, 7, 7, 7]) == [7, 7, 7, 7]
