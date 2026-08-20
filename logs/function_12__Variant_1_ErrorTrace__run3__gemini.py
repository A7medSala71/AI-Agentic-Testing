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
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    assert circle_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_two_elements_unsorted():
    collection = [2, 1]
    assert circle_sort(collection) == [1, 2]


def test_requires_multiple_passes_and_middle_swap():
    # This test ensures that:
    # 1. Swaps are correctly detected (killing swapped = None/False mutants)
    # 2. The middle comparison swap `collection[left] > collection[right + 1]` is exercised and necessary
    # 3. The `swapped or left_swap or right_swap` logic requires `right_swap` to be able to propagate upward via `or` rather than `and`.
    collection = [3, 4, 2, 1]
    assert circle_sort(collection) == [1, 2, 3, 4]