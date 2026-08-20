from function_12 import circle_sort


def test_circle_sort_empty():
    collection = []
    assert circle_sort(collection) == []


def test_circle_sort_single_element():
    collection = [42]
    assert circle_sort(collection) == [42]


def test_circle_sort_two_elements():
    collection = [2, 1]
    assert circle_sort(collection) == [1, 2]


def test_circle_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    assert circle_sort(collection) == [1, 2, 3, 4, 5]


def test_circle_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert circle_sort(collection) == [1, 2, 3, 4, 5]


def test_circle_sort_unsorted_even_length():
    collection = [3, 1, 4, 1, 5, 9, 2, 6]
    assert circle_sort(collection) == [1, 1, 2, 3, 4, 5, 6, 9]


def test_circle_sort_unsorted_odd_length():
    collection = [10, -1, 2, 5, 0, 7, 3]
    assert circle_sort(collection) == [-1, 0, 2, 3, 5, 7, 10]


def test_circle_sort_duplicate_middle_elements():
    collection = [2, 2]
    assert circle_sort(collection) == [2, 2]


def test_circle_sort_requires_middle_swap():
    collection = [3, 1, 2]
    assert circle_sort(collection) == [1, 2, 3]


def test_circle_sort_requires_exact_equality_at_middle_comparison():
    # Targets the condition: collection[left] > collection[right + 1] vs >=
    # When collection[left] == collection[right + 1], strict > should not swap and not set swapped=True,
    # whereas >= would swap and set swapped=True.
    collection = [1, 1]
    assert circle_sort(collection) == [1, 1]


def test_circle_sort_left_and_right_swap_combination():
    # Targets logical operator mutant on `return swapped or left_swap or right_swap`
    # We need a case where swapped is False, left_swap is True, but right_swap is False,
    # so that `or` vs `and` combination behaves differently.
    # [1, 4, 2, 3] -> calls circle_sort_util on halves, where one half needs a swap and the other doesn't.
    collection = [1, 4, 2, 3]
    assert circle_sort(collection) == [1, 2, 3, 4]