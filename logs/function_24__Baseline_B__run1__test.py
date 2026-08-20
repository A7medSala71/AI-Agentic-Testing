import pytest
from function_24 import binary_search_by_recursion
from function_24 import exponential_search


def test_binary_search_nominal_found():
    collection = [1, 3, 5, 7, 9, 11]
    assert binary_search_by_recursion(collection, 7) == 3
    assert binary_search_by_recursion(collection, 1) == 0
    assert binary_search_by_recursion(collection, 11) == 5


def test_binary_search_nominal_not_found():
    collection = [1, 3, 5, 7, 9, 11]
    assert binary_search_by_recursion(collection, 4) == -1
    assert binary_search_by_recursion(collection, 0) == -1
    assert binary_search_by_recursion(collection, 15) == -1


def test_binary_search_boundaries_and_empty():
    assert binary_search_by_recursion([], 5) == -1
    assert binary_search_by_recursion([42], 42) == 0
    assert binary_search_by_recursion([42], 10) == -1


def test_binary_search_explicit_bounds():
    collection = [10, 20, 30, 40, 50, 60]
    assert binary_search_by_recursion(collection, 30, left=1, right=4) == 2
    assert binary_search_by_recursion(collection, 50, left=4, right=5) == 4
    assert binary_search_by_recursion(collection, 10, left=2, right=5) == -1


def test_binary_search_unsorted_error():
    with pytest.raises(ValueError):
        binary_search_by_recursion([3, 1, 2], 2)


def test_exponential_search_nominal_found():
    collection = [2, 3, 4, 10, 40, 78, 99, 105]
    assert exponential_search(collection, 2) == 0
    assert exponential_search(collection, 10) == 3
    assert exponential_search(collection, 105) == 7
    assert exponential_search(collection, 40) == 4


def test_exponential_search_nominal_not_found():
    collection = [2, 3, 4, 10, 40, 78, 99, 105]
    assert exponential_search(collection, 1) == -1
    assert exponential_search(collection, 5) == -1
    assert exponential_search(collection, 200) == -1


def test_exponential_search_boundaries_and_empty():
    assert exponential_search([], 5) == -1
    assert exponential_search([7], 7) == 0
    assert exponential_search([7], 3) == -1


def test_exponential_search_unsorted_error():
    with pytest.raises(ValueError):
        exponential_search([10, 5, 20], 5)
