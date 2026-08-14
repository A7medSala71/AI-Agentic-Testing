from function_16 import odd_even_sort


def test_odd_even_sort_nominal():
    arr = [5, 2, 9, 1, 5, 6]
    res = odd_even_sort(arr)
    assert res == [1, 2, 5, 5, 6, 9]


def test_odd_even_sort_empty():
    arr = []
    res = odd_even_sort(arr)
    assert res == []


def test_odd_even_sort_single_element():
    arr = [42]
    res = odd_even_sort(arr)
    assert res == [42]


def test_odd_even_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_negative_numbers():
    arr = [-3, 5, 0, -1, 2]
    res = odd_even_sort(arr)
    assert res == [-3, -1, 0, 2, 5]


def test_odd_even_sort_in_place_mutation():
    arr = [3, 1, 2]
    res = odd_even_sort(arr)
    assert res is arr
    assert arr == [1, 2, 3]


def test_odd_even_sort_duplicates_and_floats():
    arr = [3.5, 1.1, 3.5, 2.0, 1.1]
    res = odd_even_sort(arr)
    assert res == [1.1, 1.1, 2.0, 3.5, 3.5]
