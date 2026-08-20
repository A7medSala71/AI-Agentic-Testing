import pytest
from function_22 import sentinel_linear_search


def test_sentinel_linear_search_found_beginning():
    seq = [10, 20, 30, 40]
    assert sentinel_linear_search(seq, 10) == 0
    assert seq == [10, 20, 30, 40]


def test_sentinel_linear_search_found_middle():
    seq = [5, 3, 8, 6, 2]
    assert sentinel_linear_search(seq, 8) == 2
    assert seq == [5, 3, 8, 6, 2]


def test_sentinel_linear_search_found_end():
    seq = ['a', 'b', 'c']
    assert sentinel_linear_search(seq, 'c') == 2
    assert seq == ['a', 'b', 'c']


def test_sentinel_linear_search_not_found():
    seq = [1, 2, 3, 4]
    assert sentinel_linear_search(seq, 99) is None
    assert seq == [1, 2, 3, 4]


def test_sentinel_linear_search_empty_sequence():
    seq = []
    assert sentinel_linear_search(seq, 5) is None
    assert seq == []


def test_sentinel_linear_search_duplicates():
    seq = [4, 1, 4, 2, 4]
    assert sentinel_linear_search(seq, 4) == 0
    assert seq == [4, 1, 4, 2, 4]


def test_sentinel_linear_search_adjacent_elements():
    # Targets an index step of +1 vs +2 by ensuring elements right next to each other are correctly found
    seq = [1, 2, 3, 4, 5]
    assert sentinel_linear_search(seq, 2) == 1
    assert sentinel_linear_search(seq, 3) == 2
    assert sentinel_linear_search(seq, 4) == 3
    assert seq == [1, 2, 3, 4, 5]