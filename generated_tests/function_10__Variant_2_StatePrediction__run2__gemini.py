from function_10 import bubble_sort_iterative, bubble_sort_recursive


def test_bubble_sort_iterative_empty():
    col = []
    res = bubble_sort_iterative(col)
    assert res == []
    assert res is col


def test_bubble_sort_iterative_single():
    col = [42]
    res = bubble_sort_iterative(col)
    assert res == [42]
    assert res is col


def test_bubble_sort_iterative_sorted():
    col = [1, 2, 3, 4, 5]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 3, 4, 5]
    assert res is col


def test_bubble_sort_iterative_reverse():
    col = [5, 4, 3, 2, 1]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 3, 4, 5]
    assert res is col


def test_bubble_sort_iterative_duplicates():
    col = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = bubble_sort_iterative(col)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    assert res is col


# Mutant mutmut_4/mutmut_5/mutmut_7: checking sorted list terminates early or fails stability/comparisons with duplicates
def test_bubble_sort_iterative_already_sorted_with_duplicates():
    # If swapped = True initially, an already sorted list with duplicates might incorrectly enter swap logic or break early incorrectly.
    # If swapped = None, `if not swapped` fails TypeError or evaluates truthiness incorrectly.
    # If >= operator is used instead of >, duplicates will trigger swaps, which changes stability or unnecessary work.
    col = [1, 2, 2, 3]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 2, 3]
    assert res is col


def test_bubble_sort_recursive_empty():
    col = []
    res = bubble_sort_recursive(col)
    assert res == []
    assert res is col


def test_bubble_sort_recursive_single():
    col = [42]
    res = bubble_sort_recursive(col)
    assert res == [42]
    assert res is col


def test_bubble_sort_recursive_sorted():
    col = [1, 2, 3, 4, 5]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 3, 4, 5]
    assert res is col


def test_bubble_sort_recursive_reverse():
    col = [5, 4, 3, 2, 1]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 3, 4, 5]
    assert res is col


def test_bubble_sort_recursive_duplicates():
    col = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = bubble_sort_recursive(col)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    assert res is col


# Mutant mutmut_2 for recursive: swapped = None causes TypeError on `if not swapped else ...`
def test_bubble_sort_recursive_sorted_no_swap():
    col = [1, 2, 3]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 3]
    assert res is col