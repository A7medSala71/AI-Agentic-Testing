from function_10 import bubble_sort_iterative, bubble_sort_recursive


def test_bubble_sort_iterative_nominal():
    coll = [5, 2, 9, 1, 5, 6]
    res = bubble_sort_iterative(coll)
    assert res == [1, 2, 5, 5, 6, 9]


def test_bubble_sort_iterative_already_sorted():
    coll = [1, 2, 3, 4, 5]
    res = bubble_sort_iterative(coll)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_iterative_reverse_sorted():
    coll = [5, 4, 3, 2, 1]
    res = bubble_sort_iterative(coll)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_iterative_empty_and_single():
    assert bubble_sort_iterative([]) == []
    assert bubble_sort_iterative([42]) == [42]


def test_bubble_sort_recursive_nominal():
    coll = [5, 2, 9, 1, 5, 6]
    res = bubble_sort_recursive(coll)
    assert res == [1, 2, 5, 5, 6, 9]


def test_bubble_sort_recursive_already_sorted():
    coll = [1, 2, 3, 4, 5]
    res = bubble_sort_recursive(coll)
    assert res == [1, 2, 3, 4, 5]


def test_bubble_sort_recursive_reverse_sorted():
    coll = [3, 2, 1]
    res = bubble_sort_recursive(coll)
    assert res == [1, 2, 3]


def test_bubble_sort_recursive_empty_and_single():
    assert bubble_sort_recursive([]) == []
    assert bubble_sort_recursive([7]) == [7]


def test_bubble_sort_iterative_swapped_false_mutants():
    # Mutants 4 and 5 change swapped = False to None or True, affecting early break when collection is already sorted.
    coll = [1, 2, 3]
    res = bubble_sort_iterative(coll)
    assert res == [1, 2, 3]


def test_bubble_sort_iterative_conditional_boundary():
    # Mutant 7 changes collection[j] > collection[j + 1] to >=, which would unnecessarily swap equal elements.
    coll = [2, 2, 1]
    res = bubble_sort_iterative(coll)
    assert res == [1, 2, 2]


def test_bubble_sort_recursive_swapped_false_mutant():
    # Mutant 2 changes swapped = False to None in recursive sort, altering the return condition when already sorted.
    coll = [1, 2, 3]
    res = bubble_sort_recursive(coll)
    assert res == [1, 2, 3]