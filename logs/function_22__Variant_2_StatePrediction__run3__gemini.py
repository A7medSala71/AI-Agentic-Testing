from function_22 import sentinel_linear_search
import pytest


def test_sentinel_linear_search_found_first():
    seq = [10, 20, 30, 40]
    assert sentinel_linear_search(seq, 10) == 0
    assert seq == [10, 20, 30, 40]


def test_sentinel_linear_search_found_middle():
    seq = [10, 20, 30, 40]
    assert sentinel_linear_search(seq, 30) == 2
    assert seq == [10, 20, 30, 40]


def test_sentinel_linear_search_found_last():
    seq = [10, 20, 30, 40]
    assert sentinel_linear_search(seq, 40) == 3
    assert seq == [10, 20, 30, 40]


def test_sentinel_linear_search_not_found():
    seq = [10, 20, 30, 40]
    assert sentinel_linear_search(seq, 99) is None
    assert seq == [10, 20, 30, 40]


def test_sentinel_linear_search_empty_sequence():
    seq = []
    assert sentinel_linear_search(seq, 5) is None
    assert seq == []


def test_sentinel_linear_search_duplicates():
    seq = [1, 2, 2, 3]
    assert sentinel_linear_search(seq, 2) == 1
    assert seq == [1, 2, 2, 3]
