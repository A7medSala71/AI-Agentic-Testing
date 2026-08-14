from function_12 import circle_sort


def test_circle_sort_empty_and_single():
    assert circle_sort([]) == []
    assert circle_sort([1]) == [1]


def test_circle_sort_already_sorted():
    assert circle_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_circle_sort_reverse_sorted():
    assert circle_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_circle_sort_random_order():
    assert circle_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]


def test_circle_sort_negative_numbers():
    assert circle_sort([-3, -1, -4, 0, 2]) == [-4, -3, -1, 0, 2]


def test_circle_sort_identical_elements():
    assert circle_sort([2, 2, 2, 2]) == [2, 2, 2, 2]


def test_circle_sort_floats():
    assert circle_sort([3.1, 1.2, 2.2, 0.5]) == [0.5, 1.2, 2.2, 3.1]
