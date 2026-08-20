import pytest
from function_22 import sentinel_linear_search


def test_sentinel_linear_search_found_beginning():
    seq = [10, 20, 30, 40]
    assert sentinel_linear_search(seq, 10) == 0
    assert seq == [10, 20, 30, 40]


def test_sentinel_linear_search_found_middle():
    seq = [5, 15, 25, 35]
    assert sentinel_linear_search(seq, 25) == 2
    assert seq == [5, 15, 25, 35]


def test_sentinel_linear_search_found_end():
    seq = [1, 2, 3, 4]
    assert sentinel_linear_search(seq, 4) == 3
    assert seq == [1, 2, 3, 4]


def test_sentinel_linear_search_not_found():
    seq = [1, 2, 3, 4]
    assert sentinel_linear_search(seq, 99) is None
    assert seq == [1, 2, 3, 4]


def test_sentinel_linear_search_empty_sequence():
    seq = []
    assert sentinel_linear_search(seq, 5) is None
    assert seq == []


def test_sentinel_linear_search_duplicate_elements():
    seq = [7, 3, 7, 5]
    assert sentinel_linear_search(seq, 7) == 0
    assert seq == [7, 3, 7, 5]


def test_sentinel_linear_search_string_sequence():
    seq = ['apple', 'banana', 'cherry']
    assert sentinel_linear_search(seq, 'banana') == 1
    assert seq == ['apple', 'banana', 'cherry']
