from function_12 import circle_sort


def test_circle_sort_empty():
    assert circle_sort([]) == []


def test_circle_sort_single():
    assert circle_sort([1]) == [1]


def test_circle_sort_already_sorted():
    assert circle_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_circle_sort_reverse_sorted():
    assert circle_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_circle_sort_duplicates():
    assert circle_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_circle_sort_negative_numbers():
    assert circle_sort([-3, 5, 0, -1, 2]) == [-3, -1, 0, 2, 5]


def test_circle_sort_two_elements():
    assert circle_sort([2, 1]) == [1, 2]


def test_circle_sort_floats():
    assert circle_sort([3.1, 1.2, 2.5, 0.5]) == [0.5, 1.2, 2.5, 3.1]


def test_circle_sort_strings():
    assert circle_sort(["banana", "apple", "cherry"]) == ["apple", "banana", "cherry"]
