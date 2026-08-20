import pytest
from function_24 import binary_search_by_recursion
from function_24 import exponential_search


def test_binary_search_nominal():
    collection = [1, 3, 5, 7, 9, 11, 13]
    assert binary_search_by_recursion(collection, 7) == 3
    assert binary_search_by_recursion(collection, 1) == 0
    assert binary_search_by_recursion(collection, 13) == 6


def test_binary_search_not_found():
    collection = [2, 4, 6, 8, 10]
    assert binary_search_by_recursion(collection, 5) == -1
    assert binary_search_by_recursion(collection, 1) == -1
    assert binary_search_by_recursion(collection, 11) == -1


def test_binary_search_empty_collection():
    assert binary_search_by_recursion([], 5) == -1


def test_binary_search_explicit_bounds():
    collection = [10, 20, 30, 40, 50]
    assert binary_search_by_recursion(collection, 30, left=1, right=3) == 2
    assert binary_search_by_recursion(collection, 10, left=1, right=3) == -1


def test_binary_search_unsorted_raises():
    with pytest.raises(ValueError):
        binary_search_by_recursion([3, 1, 2], 2)


def test_exponential_search_nominal():
    collection = [2, 3, 4, 10, 40, 50, 60, 70, 80, 90]
    assert exponential_search(collection, 10) == 3
    assert exponential_search(collection, 2) == 0
    assert exponential_search(collection, 90) == 9
    assert exponential_search(collection, 50) == 5


def test_exponential_search_not_found():
    collection = [2, 3, 4, 10, 40]
    assert exponential_search(collection, 5) == -1
    assert exponential_search(collection, 1) == -1
    assert exponential_search(collection, 50) == -1


def test_exponential_search_single_element():
    collection = [42]
    assert exponential_search(collection, 42) == 0
    assert exponential_search(collection, 7) == -1


def test_exponential_search_empty():
    assert exponential_search([], 5) == -1


def test_exponential_search_unsorted_raises():
    with pytest.raises(ValueError):
        exponential_search([5, 4, 3, 2, 1], 4)
