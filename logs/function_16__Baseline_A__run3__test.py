from function_16 import odd_even_sort


def test_odd_even_sort_nominal():
    arr = [4, 3, 2, 1, 5]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]
    assert arr == [1, 2, 3, 4, 5]


def test_odd_even_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_empty_and_single():
    assert odd_even_sort([]) == []
    assert odd_even_sort([42]) == [42]


def test_odd_even_sort_duplicates_and_negatives():
    arr = [-1, 3, -3, 2, 3, 0, -1]
    res = odd_even_sort(arr)
    assert res == [-3, -1, -1, 0, 2, 3, 3]


def test_odd_even_sort_two_elements():
    assert odd_even_sort([2, 1]) == [1, 2]
    assert odd_even_sort([1, 2]) == [1, 2]
