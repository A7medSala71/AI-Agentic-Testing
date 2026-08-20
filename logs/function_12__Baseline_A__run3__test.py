from function_12 import circle_sort


def test_empty_collection():
    collection = []
    assert circle_sort(collection) == []


def test_single_element():
    collection = [42]
    assert circle_sort(collection) == [42]


def test_already_sorted():
    collection = [1, 2, 3, 4, 5]
    assert circle_sort(collection) == [1, 2, 3, 4, 5]


def test_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert circle_sort(collection) == [1, 2, 3, 4, 5]


def test_unsorted_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    assert circle_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]


def test_negative_numbers():
    collection = [-3, 5, 0, -1, 2]
    assert circle_sort(collection) == [-3, -1, 0, 2, 5]
