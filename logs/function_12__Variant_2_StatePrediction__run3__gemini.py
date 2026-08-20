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


def test_circle_sort_reverse_order():
    collection = [5, 4, 3, 2, 1]
    assert circle_sort(collection) == [1, 2, 3, 4, 5]


def test_circle_sort_unsorted_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    assert circle_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_circle_sort_two_elements():
    # Mutants mutmut_1 and mutmut_2 change len(collection) < 2 boundary/constant, so a list of length 2 must be sorted correctly where length < 3 or <= 2 incorrectly bypasses/returns early.
    collection = [2, 1]
    assert circle_sort(collection) == [1, 2]


def test_circle_sort_swapped_false_initialization():
    # Mutant mutmut_3 changes swapped = False to None, causing a TypeError or incorrect return when no swaps occur.
    collection = [1, 2]
    assert circle_sort(collection) == [1, 2]


def test_circle_sort_single_swap_left_right():
    # Mutants mutmut_11 and mutmut_12 change swapped = True to None or False during the left < right loop, affecting loop continuation for collections requiring a swap.
    collection = [2, 1, 3]
    assert circle_sort(collection) == [1, 2, 3]


def test_circle_sort_middle_element_swap():
    # Mutants mutmut_29 and mutmut_30 change swapped = True to None or False when the middle comparison swaps elements.
    collection = [1, 3, 2]
    assert circle_sort(collection) == [1, 2, 3]


def test_circle_sort_logical_operator_return():
    # Mutant mutmut_53 changes return swapped or left_swap or right_swap to swapped or left_swap and right_swap, failing when one side is false and another is true.
    collection = [2, 1, 3, 4]
    assert circle_sort(collection) == [1, 2, 3, 4]


def test_circle_sort_mutmut_3_unswapped_return():
    # Mutating swapped=False to None causes an already sorted collection to return None or fail type checks if it were returned, but here it causes the outer while loop condition to behave unexpectedly if None is returned.
    # Specifically, circle_sort_util returns swapped (None), so is_not_sorted becomes None, which evaluates as falsy and terminates the while loop prematurely even if sorting wasn't finished.
    # Wait, an already-sorted list returns False (or None). If it returns None, 'is_not_sorted = None' breaks the while loop immediately. If the list needs sorting, it might fail or behave incorrectly.
    # Let's test a collection where circle_sort_util is called on a sorted sublist and returns swapped=False vs None.
    collection = [1, 2, 3]
    assert circle_sort(collection) == [1, 2, 3]


def test_circle_sort_mutmut_11_and_12_left_right_swap_tracking():
    # Mutating swapped=True to None/False in left<right loop makes circle_sort_util return None/False instead of True, causing the outer while loop to terminate prematurely when only left<right swaps occurred.
    collection = [3, 1]
    assert circle_sort(collection) == [1, 3]


def test_circle_sort_mutmut_29_and_30_mid_swap_tracking():
    # Mutating swapped=True to None/False in the mid comparison makes circle_sort_util return None/False instead of True, terminating the outer while loop prematurely.
    collection = [2, 3, 1]
    assert circle_sort(collection) == [1, 2, 3]


def test_circle_sort_mutmut_53_operator_precedence():
    # Mutating `swapped or left_swap or right_swap` to `swapped or left_swap and right_swap` changes the boolean expression result when swapped=False, left_swap=True, right_swap=False.
    # We need a collection where only one side (left or right half) performs a swap, so one of left_swap/right_swap is True and the other is False, and swapped is False.
    # In that case, `left_swap and right_swap` evaluates to False, whereas `left_swap or right_swap` is True, causing the sorting loop to terminate too early.
    collection = [1, 2, 4, 3]
    assert circle_sort(collection) == [1, 2, 3, 4]