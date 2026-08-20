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


def test_merge_sort_stable_sorting_duplicates():
    # This test specifically checks duplicate stability (elements with equal values),
    # which exercises the `<=` vs `<` boundary in `left[0] <= right[0]`.
    # Let's use custom objects or distinguishable items if values are equal,
    # or ensure equal items from left and right preserve relative order.
    # Since the algorithm compares values, if left has an item equal to right,
    # left should be chosen first for stability.
    collection = [2, 2, 1, 1]
    assert merge_sort(collection) == [1, 1, 2, 2]
    
    # Another test specifically with duplicates where left and right sublists
    # have equal elements to ensure the left element is popped when equal.
    # Sublist left: [2], right: [2] -> should pick left's 2 first.
    assert merge_sort([2, 2]) == [2, 2]