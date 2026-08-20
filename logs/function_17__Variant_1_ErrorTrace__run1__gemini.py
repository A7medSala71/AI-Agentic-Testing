from function_17 import quick_sort


def test_quick_sort_empty():
    collection = []
    assert quick_sort(collection) == []


def test_quick_sort_single_element():
    collection = [42]
    assert quick_sort(collection) == [42]


def test_quick_sort_sorted_list():
    collection = [1, 2, 3, 4, 5]
    assert quick_sort(collection) == [1, 2, 3, 4, 5]


def test_quick_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert quick_sort(collection) == [1, 2, 3, 4, 5]


def test_quick_sort_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    assert quick_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_quick_sort_negative_numbers():
    collection = [-3, -1, -4, 0, 2, 1]
    assert quick_sort(collection) == [-4, -3, -1, 0, 1, 2]
