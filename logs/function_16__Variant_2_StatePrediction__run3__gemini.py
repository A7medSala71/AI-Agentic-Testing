from function_16 import odd_even_sort


def test_odd_even_sort_nominal():
    arr = [4, 3, 2, 1]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4]


def test_odd_even_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_empty():
    arr = []
    res = odd_even_sort(arr)
    assert res == []


def test_odd_even_sort_single_element():
    arr = [42]
    res = odd_even_sort(arr)
    assert res == [42]


def test_odd_even_sort_duplicates():
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = odd_even_sort(arr)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_odd_even_sort_mutation_check():
    arr = [2, 1]
    res = odd_even_sort(arr)
    assert res == [1, 2]


def test_odd_even_sort_mutmut_5_and_12_and_25_and_26_and_32():
    # Mutants 5/25/26 mutate is_sorted to None/True or 12/32 alter range step, causing an unsorted list like [2, 1, 3] to fail or loop infinitely if is_sorted stays True/None.
    arr = [2, 1, 3]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3]