import pytest
from function_24 import binary_search_by_recursion
from function_24 import exponential_search


def test_binary_search_nominal():
    collection = [1, 3, 5, 7, 9, 11, 13]
    assert binary_search_by_recursion(collection, 7) == 3
    assert binary_search_by_recursion(collection, 1) == 0
    assert binary_search_by_recursion(collection, 13) == 6


def test_binary_search_not_found():
    collection = [1, 3, 5, 7, 9]
    assert binary_search_by_recursion(collection, 4) == -1
    assert binary_search_by_recursion(collection, 0) == -1
    assert binary_search_by_recursion(collection, 10) == -1


def test_binary_search_unsorted_raises():
    collection = [5, 1, 3, 7]
    with pytest.raises(ValueError):
        binary_search_by_recursion(collection, 3)


def test_binary_search_empty():
    assert binary_search_by_recursion([], 5) == -1


def test_binary_search_custom_bounds():
    collection = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert binary_search_by_recursion(collection, 5, left=2, right=7) == 4
    assert binary_search_by_recursion(collection, 2, left=2, right=7) == -1


def test_exponential_search_nominal():
    collection = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    assert exponential_search(collection, 10) == 4
    assert exponential_search(collection, 2) == 0
    assert exponential_search(collection, 20) == 9


def test_exponential_search_not_found():
    collection = [2, 4, 6, 8, 10]
    assert exponential_search(collection, 5) == -1
    assert exponential_search(collection, 1) == -1
    assert exponential_search(collection, 15) == -1


def test_exponential_search_unsorted_raises():
    collection = [10, 5, 20]
    with pytest.raises(ValueError):
        exponential_search(collection, 5)


def test_exponential_search_empty():
    assert exponential_search([], 5) == -1


def test_exponential_search_single_element():
    collection = [42]
    assert exponential_search(collection, 42) == 0
    assert exponential_search(collection, 10) == -1
