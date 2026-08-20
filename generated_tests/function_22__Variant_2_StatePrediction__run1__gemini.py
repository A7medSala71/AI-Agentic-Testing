from function_22 import sentinel_linear_search
import pytest


def test_sentinel_linear_search_found_first():
    seq = [10, 20, 30, 40]
    assert sentinel_linear_search(seq, 10) == 0
    assert seq == [10, 20, 30, 40]


def test_sentinel_linear_search_found_middle():
    seq = [1, 5, 9, 2, 6]
    assert sentinel_linear_search(seq, 9) == 2
    assert seq == [1, 5, 9, 2, 6]


def test_sentinel_linear_search_found_last():
    seq = [7, 8, 9]
    assert sentinel_linear_search(seq, 9) == 2
    assert seq == [7, 8, 9]


def test_sentinel_linear_search_not_found():
    seq = [4, 5, 6]
    assert sentinel_linear_search(seq, 10) is None
    assert seq == [4, 5, 6]


def test_sentinel_linear_search_empty_sequence():
    seq = []
    assert sentinel_linear_search(seq, 5) is None
    assert seq == []


def test_sentinel_linear_search_duplicate_elements():
    seq = [3, 1, 4, 1, 5]
    assert sentinel_linear_search(seq, 1) == 1
    assert seq == [3, 1, 4, 1, 5]


def test_sentinel_linear_search_string_sequence():
    seq = ['apple', 'banana', 'cherry']
    assert sentinel_linear_search(seq, 'banana') == 1
    assert seq == ['apple', 'banana', 'cherry']
