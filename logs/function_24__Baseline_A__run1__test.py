import pytest
from function_24 import binary_search_by_recursion
from function_24 import exponential_search


def test_binary_search_nominal():
    collection = [1, 3, 5, 7, 9, 11]
    assert binary_search_by_recursion(collection, 7) == 3
    assert binary_search_by_recursion(collection, 1) == 0
    assert binary_search_by_recursion(collection, 11) == 5
    assert binary_search_by_recursion(collection, 2) == -1


def test_binary_search_explicit_bounds():
    collection = [10, 20, 30, 40, 50]
    assert binary_search_by_recursion(collection, 30, 1, 3) == 2
    assert binary_search_by_recursion(collection, 10, 1, 3) == -1


def test_binary_search_empty_and_unsorted():
    assert binary_search_by_recursion([], 5) == -1
    with pytest.raises(ValueError):
        binary_search_by_recursion([3, 1, 2], 2)


def test_exponential_search_nominal():
    collection = [2, 3, 4, 10, 40, 64, 128, 256, 512]
    assert exponential_search(collection, 10) == 3
    assert exponential_search(collection, 2) == 0
    assert exponential_search(collection, 512) == 8
    assert exponential_search(collection, 100) == -1


def test_exponential_search_boundaries_and_errors():
    assert exponential_search([42], 42) == 0
    assert exponential_search([42], 99) == -1
    with pytest.raises(ValueError):
        exponential_search([5, 1, 2], 5)
