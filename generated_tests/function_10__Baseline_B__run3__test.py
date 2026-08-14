from function_10 import bubble_sort_iterative, bubble_sort_recursive


def test_bubble_sort_iterative_empty():
    col = []
    res = bubble_sort_iterative(col)
    assert res == []


def test_bubble_sort_iterative_single():
    col = [42]
    res = bubble_sort_iterative(col)
    assert res == [42]


def test_bubble_sort_iterative_already_sorted():
    col = [1, 2, 3, 4, 5]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_iterative_reverse_sorted():
    col = [5, 4, 3, 2, 1]
    res = bubble_sort_iterative(col)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_iterative_unsorted_duplicates():
    col = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = bubble_sort_iterative(col)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_bubble_sort_recursive_empty():
    col = []
    res = bubble_sort_recursive(col)
    assert res == []


def test_bubble_sort_recursive_single():
    col = [42]
    res = bubble_sort_recursive(col)
    assert res == [42]


def test_bubble_sort_recursive_already_sorted():
    col = [1, 2, 3, 4, 5]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_recursive_reverse_sorted():
    col = [5, 4, 3, 2, 1]
    res = bubble_sort_recursive(col)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_recursive_unsorted_duplicates():
    col = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = bubble_sort_recursive(col)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_bubble_sort_iterative_negative_and_floats():
    col = [3.5, -1.2, 0, 2.1, -5]
    res = bubble_sort_iterative(col)
    assert res == [-5, -1.2, 0, 2.1, 3.5]


def test_bubble_sort_recursive_negative_and_floats():
    col = [3.5, -1.2, 0, 2.1, -5]
    res = bubble_sort_recursive(col)
    assert res == [-5, -1.2, 0, 2.1, 3.5]
