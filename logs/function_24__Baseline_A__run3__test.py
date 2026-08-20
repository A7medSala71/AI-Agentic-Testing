import pytest
from function_24 import binary_search_by_recursion
from function_24 import exponential_search


def test_binary_search_nominal_found():
    col = [1, 3, 5, 7, 9, 11]
    assert binary_search_by_recursion(col, 7) == 3
    assert binary_search_by_recursion(col, 1) == 0
    assert binary_search_by_recursion(col, 11) == 5


def test_binary_search_nominal_not_found():
    col = [1, 3, 5, 7, 9, 11]
    assert binary_search_by_recursion(col, 4) == -1
    assert binary_search_by_recursion(col, 0) == -1
    assert binary_search_by_recursion(col, 12) == -1


def test_binary_search_empty_collection():
    assert binary_search_by_recursion([], 5) == -1


def test_binary_search_explicit_bounds():
    col = [10, 20, 30, 40, 50]
    assert binary_search_by_recursion(col, 30, left=1, right=3) == 2
    assert binary_search_by_recursion(col, 10, left=1, right=3) == -1


def test_binary_search_unsorted_raises():
    col = [5, 1, 3]
    with pytest.raises(ValueError):
        binary_search_by_recursion(col, 3)


def test_exponential_search_nominal_found():
    col = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    assert exponential_search(col, 2) == 0
    assert exponential_search(col, 10) == 4
    assert exponential_search(col, 20) == 9


def test_exponential_search_nominal_not_found():
    col = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    assert exponential_search(col, 1) == -1
    assert exponential_search(col, 11) == -1
    assert exponential_search(col, 21) == -1


def test_exponential_search_single_element():
    col = [42]
    assert exponential_search(col, 42) == 0
    assert exponential_search(col, 10) == -1


def test_exponential_search_unsorted_raises():
    col = [10, 5, 20]
    with pytest.raises(ValueError):
        exponential_search(col, 5)
