from function_12 import circle_sort


def test_circle_sort_empty():
    collection = []
    assert circle_sort(collection) == []


def test_circle_sort_single_element():
    collection = [42]
    assert circle_sort(collection) == [42]


def test_circle_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    assert circle_sort(collection) == [1, 2, 3, 4, 5]


def test_circle_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert circle_sort(collection) == [1, 2, 3, 4, 5]


def test_circle_sort_random_order():
    collection = [3, 1, 4, 1, 5, 9, 2, 6]
    assert circle_sort(collection) == [1, 1, 2, 3, 4, 5, 6, 9]


def test_circle_sort_two_elements():
    collection = [2, 1]
    assert circle_sort(collection) == [1, 2]


def test_circle_sort_odd_length_comparisons():
    # Targets specific branches in circle_sort_util involving odd lengths,
    # mid calculations, middle element comparisons (left == right / right + 1 / right - 1),
    # logical operators in return (or vs and), and multiple iterations (swapped = False / None).
    collection = [3, 1, 2]
    assert circle_sort(collection) == [1, 2, 3]


def test_circle_sort_with_duplicates_triggering_mid_swaps():
    # Targets equality conditions (>= vs >) and specific indexing offsets during center checks.
    collection = [2, 2, 1, 3]
    assert circle_sort(collection) == [1, 2, 2, 3]