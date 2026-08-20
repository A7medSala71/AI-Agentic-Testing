import pytest
from function_22 import sentinel_linear_search


def test_sentinel_linear_search_found_middle():
    seq = [4, 2, 1, 5, 3]
    assert sentinel_linear_search(seq, 1) == 2
    assert seq == [4, 2, 1, 5, 3]


def test_sentinel_linear_search_found_first():
    seq = [10, 20, 30]
    assert sentinel_linear_search(seq, 10) == 0
    assert seq == [10, 20, 30]


def test_sentinel_linear_search_found_last():
    seq = [10, 20, 30]
    assert sentinel_linear_search(seq, 30) == 2
    assert seq == [10, 20, 30]


def test_sentinel_linear_search_not_found():
    seq = [1, 2, 3]
    assert sentinel_linear_search(seq, 99) is None
    assert seq == [1, 2, 3]


def test_sentinel_linear_search_empty_sequence():
    seq = []
    assert sentinel_linear_search(seq, 5) is None
    assert seq == []


def test_sentinel_linear_search_duplicate_elements():
    seq = [1, 2, 2, 3]
    assert sentinel_linear_search(seq, 2) == 1
    assert seq == [1, 2, 2, 3]


def test_sentinel_linear_search_immutable_raises():
    seq = (1, 2, 3)
    with pytest.raises(AttributeError):
        sentinel_linear_search(seq, 2)
