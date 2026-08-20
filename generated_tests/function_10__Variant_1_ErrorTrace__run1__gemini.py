from function_10 import bubble_sort_iterative, bubble_sort_recursive


def test_bubble_sort_iterative_nominal():
    col = [5, 1, 4, 2, 8]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 4, 5, 8]


def test_bubble_sort_iterative_already_sorted():
    col = [1, 2, 3, 4, 5]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_iterative_reverse_sorted():
    col = [5, 4, 3, 2, 1]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_iterative_empty_and_single():
    assert bubble_sort_iterative([]) == []
    assert bubble_sort_iterative([42]) == [42]


def test_bubble_sort_iterative_duplicates():
    col = [2, 2, 1, 1]
    res = bubble_sort_iterative(col)
    assert res == [1, 1, 2, 2]


def test_bubble_sort_iterative_with_equal_elements():
    # Kills mutant that changes `>` to `>=` (ConditionalBoundary)
    # If `>=` is used, stable sort characteristics or unnecessary swaps/breaks might affect sorting or optimization,
    # but more directly, with duplicates or equal elements, `>=` causes unstable swaps of equal elements.
    col = [2, 2, 1]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 2]


def test_bubble_sort_recursive_nominal():
    col = [5, 1, 4, 2, 8]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 4, 5, 8]


def test_bubble_sort_recursive_already_sorted():
    col = [1, 2, 3, 4, 5]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_recursive_reverse_sorted():
    col = [3, 2, 1]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 3]


def test_bubble_sort_recursive_empty_and_single():
    assert bubble_sort_recursive([]) == []
    assert bubble_sort_recursive([7]) == [7]


def test_bubble_sort_recursive_duplicates():
    col = [2, 2, 1, 1]
    res = bubble_sort_recursive(col)
    assert res == [1, 1, 2, 2]