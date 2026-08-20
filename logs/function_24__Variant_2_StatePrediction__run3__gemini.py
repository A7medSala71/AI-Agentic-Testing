import pytest
from function_24 import binary_search_by_recursion
from function_24 import exponential_search


def test_binary_search_by_recursion_nominal():
    col = [1, 3, 5, 7, 9, 11]
    assert binary_search_by_recursion(col, 1) == 0
    assert binary_search_by_recursion(col, 7) == 3
    assert binary_search_by_recursion(col, 11) == 5


def test_binary_search_by_recursion_not_found():
    col = [1, 3, 5, 7, 9, 11]
    assert binary_search_by_recursion(col, 0) == -1
    assert binary_search_by_recursion(col, 6) == -1
    assert binary_search_by_recursion(col, 12) == -1


def test_binary_search_by_recursion_empty():
    assert binary_search_by_recursion([], 5) == -1


def test_binary_search_by_recursion_unsorted_raises():
    with pytest.raises(ValueError):
        binary_search_by_recursion([3, 1, 2], 2)


def test_binary_search_by_recursion_explicit_bounds():
    col = [10, 20, 30, 40, 50]
    assert binary_search_by_recursion(col, 30, left=1, right=3) == 2
    assert binary_search_by_recursion(col, 10, left=1, right=3) == -1


def test_exponential_search_nominal():
    col = [2, 3, 4, 10, 40, 44, 55, 60, 70, 80]
    assert exponential_search(col, 2) == 0
    assert exponential_search(col, 10) == 3
    assert exponential_search(col, 80) == 9


def test_exponential_search_not_found():
    col = [2, 3, 4, 10, 40]
    assert exponential_search(col, 1) == -1
    assert exponential_search(col, 5) == -1
    assert exponential_search(col, 50) == -1


def test_exponential_search_single_element():
    assert exponential_search([42], 42) == 0
    assert exponential_search([42], 10) == -1


def test_exponential_search_unsorted_raises():
    with pytest.raises(ValueError):
        exponential_search([5, 4, 3, 2, 1], 4)


def test_exponential_search_empty():
    assert exponential_search([], 5) == -1
