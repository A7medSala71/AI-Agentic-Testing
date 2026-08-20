from function_16 import odd_even_sort


def test_odd_even_sort_nominal():
    arr = [4, 3, 2, 1, 5]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
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


def test_odd_even_sort_negatives():
    arr = [-3, 5, 0, -1, 2]
    res = odd_even_sort(arr)
    assert res == [-3, -1, 0, 2, 5]


def test_odd_even_sort_in_place():
    arr = [3, 1, 2]
    res = odd_even_sort(arr)
    assert res is arr
