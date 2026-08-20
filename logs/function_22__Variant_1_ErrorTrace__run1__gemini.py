from function_22 import sentinel_linear_search
import pytest


def test_sentinel_linear_search_found_first():
    seq = [10, 20, 30, 40]
    assert sentinel_linear_search(seq, 10) == 0
    assert seq == [10, 20, 30, 40]


def test_sentinel_linear_search_found_middle():
    seq = [5, 3, 8, 1, 9]
    assert sentinel_linear_search(seq, 8) == 2
    assert seq == [5, 3, 8, 1, 9]


def test_sentinel_linear_search_found_last():
    seq = [1, 2, 3, 4]
    assert sentinel_linear_search(seq, 4) == 3
    assert seq == [1, 2, 3, 4]


def test_sentinel_linear_search_not_found():
    seq = [1, 2, 3]
    assert sentinel_linear_search(seq, 99) is None
    assert seq == [1, 2, 3]


def test_sentinel_linear_search_empty_sequence():
    seq = []
    assert sentinel_linear_search(seq, 5) is None
    assert seq == []


def test_sentinel_linear_search_duplicates():
    seq = [4, 1, 4, 2]
    assert sentinel_linear_search(seq, 4) == 0
    assert seq == [4, 1, 4, 2]


def test_sentinel_linear_search_string_sequence():
    seq = ['apple', 'banana', 'cherry']
    assert sentinel_linear_search(seq, 'banana') == 1
    assert seq == ['apple', 'banana', 'cherry']
