from function_12 import circle_sort


def test_circle_sort_empty():
    collection = []
    assert circle_sort(collection) == []


def test_circle_sort_single_element():
    collection = [42]
    assert circle_sort(collection) == [42]


def test_circle_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    assert circle_sort(collection) == [1, 2, 3, 4, 5]


def test_circle_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert circle_sort(collection) == [1, 2, 3, 4, 5]


def test_circle_sort_random_order():
    collection = [3, 1, 4, 1, 5, 9, 2, 6]
    assert circle_sort(collection) == [1, 1, 2, 3, 4, 5, 6, 9]


def test_circle_sort_two_elements_unsorted():
    collection = [2, 1]
    assert circle_sort(collection) == [1, 2]


def test_circle_sort_negative_numbers():
    collection = [-3, 5, -1, 0, 2]
    assert circle_sort(collection) == [-3, -1, 0, 2, 5]


def test_circle_sort_floating_point():
    collection = [3.1, 1.2, 2.5, 0.5]
    assert circle_sort(collection) == [0.5, 1.2, 2.5, 3.1]


def test_circle_sort_identical_elements():
    collection = [7, 7, 7, 7]
    assert circle_sort(collection) == [7, 7, 7, 7]
