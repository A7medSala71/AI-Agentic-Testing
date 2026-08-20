import pytest
from function_22 import sentinel_linear_search


def test_sentinel_linear_search_found_beginning():
    seq = [10, 20, 30, 40]
    assert sentinel_linear_search(seq, 10) == 0
    assert seq == [10, 20, 30, 40]


def test_sentinel_linear_search_found_middle():
    seq = [10, 20, 30, 40]
    assert sentinel_linear_search(seq, 30) == 2
    assert seq == [10, 20, 30, 40]


def test_sentinel_linear_search_found_end():
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


def test_sentinel_linear_search_single_element_found():
    seq = [42]
    assert sentinel_linear_search(seq, 42) == 0
    assert seq == [42]


def test_sentinel_linear_search_single_element_not_found():
    seq = [42]
    assert sentinel_linear_search(seq, 7) is None
    assert seq == [42]


def test_sentinel_linear_search_duplicates():
    seq = [5, 1, 5, 2]
    assert sentinel_linear_search(seq, 5) == 0
    assert seq == [5, 1, 5, 2]
