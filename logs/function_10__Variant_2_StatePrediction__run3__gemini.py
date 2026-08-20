from function_10 import bubble_sort_iterative, bubble_sort_recursive


def test_bubble_sort_iterative_nominal():
    col = [5, 2, 9, 1, 5, 6]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 5, 5, 6, 9]
    assert res is col


def test_bubble_sort_iterative_already_sorted():
    col = [1, 2, 3, 4, 5]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 3, 4, 5]
    assert res is col


def test_bubble_sort_iterative_reverse_sorted():
    col = [5, 4, 3, 2, 1]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 3, 4, 5]
    assert res is col


def test_bubble_sort_iterative_edge_cases():
    assert bubble_sort_iterative([]) == []
    assert bubble_sort_iterative([42]) == [42]
    assert bubble_sort_iterative([2, 1]) == [1, 2]


def test_bubble_sort_recursive_nominal():
    col = [5, 2, 9, 1, 5, 6]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 5, 5, 6, 9]
    assert res is col


def test_bubble_sort_recursive_already_sorted():
    col = [1, 2, 3, 4, 5]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 3, 4, 5]
    assert res is col


def test_bubble_sort_recursive_reverse_sorted():
    col = [5, 4, 3, 2, 1]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 3, 4, 5]
    assert res is col


def test_bubble_sort_recursive_edge_cases():
    assert bubble_sort_recursive([]) == []
    assert bubble_sort_recursive([42]) == [42]
    assert bubble_sort_recursive([2, 1]) == [1, 2]


def test_bubble_sort_iterative_swapped_false_mutants():
    # If swapped is initialized to None or True on an already sorted list, early break behavior diverges.
    col = [1, 2, 3]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 3]


def test_bubble_sort_iterative_comparison_boundary():
    # If > is mutated to >=, duplicate elements trigger a swap (unstable/unnecessary sort changes or breaks).
    col = [2, 2, 1]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 2]


def test_bubble_sort_recursive_swapped_none():
    # If swapped is initialized to None instead of False, recursive return condition logic evaluates incorrectly on sorted collections.
    col = [1, 2, 3]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 3]