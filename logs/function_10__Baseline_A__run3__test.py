from function_10 import bubble_sort_iterative, bubble_sort_recursive


def test_bubble_sort_iterative_nominal():
    coll = [5, 2, 9, 1, 5, 6]
    res = bubble_sort_iterative(coll)
    assert res == [1, 2, 5, 5, 6, 9]


def test_bubble_sort_iterative_empty():
    coll = []
    res = bubble_sort_iterative(coll)
    assert res == []


def test_bubble_sort_iterative_single():
    coll = [42]
    res = bubble_sort_iterative(coll)
    assert res == [42]


def test_bubble_sort_iterative_already_sorted():
    coll = [1, 2, 3, 4, 5]
    res = bubble_sort_iterative(coll)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_iterative_reverse_sorted():
    coll = [5, 4, 3, 2, 1]
    res = bubble_sort_iterative(coll)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_recursive_nominal():
    coll = [5, 2, 9, 1, 5, 6]
    res = bubble_sort_recursive(coll)
    assert res == [1, 2, 5, 5, 6, 9]


def test_bubble_sort_recursive_empty():
    coll = []
    res = bubble_sort_recursive(coll)
    assert res == []


def test_bubble_sort_recursive_single():
    coll = [42]
    res = bubble_sort_recursive(coll)
    assert res == [42]


def test_bubble_sort_recursive_already_sorted():
    coll = [1, 2, 3, 4, 5]
    res = bubble_sort_recursive(coll)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_recursive_reverse_sorted():
    coll = [5, 4, 3, 2, 1]
    res = bubble_sort_recursive(coll)
    assert res == [1, 2, 3, 4, 5]
