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


def test_circle_sort_unsorted_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    assert circle_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_circle_sort_two_elements():
    collection = [2, 1]
    assert circle_sort(collection) == [1, 2]


def test_circle_sort_odd_length():
    collection = [7, 2, 5, 1, 9]
    assert circle_sort(collection) == [1, 2, 5, 7, 9]


def test_circle_sort_even_length():
    collection = [10, 3, 5, 1, 8, 2]
    assert circle_sort(collection) == [1, 2, 3, 5, 8, 10]


def test_circle_sort_mutmut_3_swapped_false_init():
    # Mutating swapped=False to None causes TypeError when evaluating return expression if any sorting pass triggers a boolean or operation.
    assert circle_sort([1, 2]) == [1, 2]


def test_circle_sort_mutmut_11_and_12_swapped_true_mid_compare():
    # Mutating swapped=True to swapped=None or False when a swap occurs in the while loop causes the outer loop to exit prematurely on collections requiring a second pass.
    assert circle_sort([3, 2, 1, 4]) == [1, 2, 3, 4]


def test_circle_sort_mutmut_29_and_30_swapped_true_odd_middle():
    # Mutating swapped=True to None/False at line 25 causes left_swap/right_swap to return incorrect truthiness on odd middle swaps, stopping iteration early.
    assert circle_sort([2, 1, 3]) == [1, 2, 3]


def test_circle_sort_mutmut_53_logical_operator_and():
    # Mutating 'swapped or left_swap or right_swap' to 'swapped or left_swap and right_swap' causes right_swap to be ignored/falsified if left_swap is True, failing to sort.
    assert circle_sort([3, 1, 4, 2]) == [1, 2, 3, 4]