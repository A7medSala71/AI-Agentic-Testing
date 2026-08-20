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
    collection = [-3, 5, 0, -1, 2, 4]
    assert merge_sort(collection) == [-3, -1, 0, 2, 4, 5]


def test_merge_sort_duplicate_elements_stability_or_order():
    # Mutant 7 changes <= to < when comparing left[0] and right[0]. For equal elements, left[0] < right[0] is False, so it incorrectly takes right.pop(0) instead of left.pop(0).
    # This specifically changes the stability/interleaving when duplicate elements exist across the split, e.g. merging [2] and [2].
    collection = [2, 2]
    assert merge_sort(collection) == [2, 2]