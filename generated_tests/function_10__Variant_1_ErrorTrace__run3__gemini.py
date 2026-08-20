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


def test_bubble_sort_iterative_empty_and_single():
    col1 = []
    assert bubble_sort_iterative(col1) == []
    col2 = [42]
    assert bubble_sort_iterative(col2) == [42]


def test_bubble_sort_iterative_duplicates():
    # Kills MutMut 7: checks that equal elements do not trigger a swap/not-swapped break issue
    col = [2, 2, 1]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 2]


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


def test_bubble_sort_recursive_empty_and_single():
    col1 = []
    assert bubble_sort_recursive(col1) == []
    col2 = [42]
    assert bubble_sort_recursive(col2) == [42]