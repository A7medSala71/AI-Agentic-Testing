import pytest
from function_24 import binary_search_by_recursion
from function_24 import exponential_search


def test_binary_search_nominal():
    collection = [1, 3, 5, 7, 9, 11]
    assert binary_search_by_recursion(collection, 7) == 3
    assert binary_search_by_recursion(collection, 1) == 0
    assert binary_search_by_recursion(collection, 11) == 5
    assert binary_search_by_recursion(collection, 2) == -1


def test_binary_search_boundaries():
    collection = [10, 20, 30]
    assert binary_search_by_recursion(collection, 10, 0, 2) == 0
    assert binary_search_by_recursion(collection, 30, 0, 2) == 2
    assert binary_search_by_recursion(collection, 15, 0, 2) == -1
    assert binary_search_by_recursion([], 10) == -1


def test_binary_search_unsorted_raises():
    with pytest.raises(ValueError):
        binary_search_by_recursion([3, 1, 2], 2)


def test_exponential_search_nominal():
    collection = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    assert exponential_search(collection, 2) == 0
    assert exponential_search(collection, 10) == 4
    assert exponential_search(collection, 20) == 9
    assert exponential_search(collection, 5) == -1


def test_exponential_search_boundaries_and_unsorted():
    assert exponential_search([42], 42) == 0
    assert exponential_search([42], 10) == -1
    with pytest.raises(ValueError):
        exponential_search([5, 4, 3], 4)
