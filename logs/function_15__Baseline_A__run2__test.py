from function_15 import merge_sort


def test_merge_sort_empty():
    collection = []
    assert merge_sort(collection) == []


def test_merge_sort_single_element():
    collection = [42]
    assert merge_sort(collection) == [42]


def test_merge_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    assert merge_sort(collection) == [1, 2, 3, 4, 5]


def test_merge_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert merge_sort(collection) == [1, 2, 3, 4, 5]


def test_merge_sort_unsorted_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    assert merge_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_merge_sort_negative_numbers():
    collection = [-3, 5, 0, -1, 2]
    assert merge_sort(collection) == [-3, -1, 0, 2, 5]


def test_merge_sort_strings():
    collection = ["banana", "apple", "cherry", "date"]
    assert merge_sort(collection) == ["apple", "banana", "cherry", "date"]
