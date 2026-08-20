import pytest
from function_29 import perfect_square, perfect_square_binary_search


def test_perfect_square_nominal():
    assert perfect_square(0) is True
    assert perfect_square(1) is True
    assert perfect_square(4) is True
    assert perfect_square(9) is True
    assert perfect_square(16) is True
    assert perfect_square(25) is True


def test_perfect_square_non_squares():
    assert perfect_square(2) is False
    assert perfect_square(3) is False
    assert perfect_square(5) is False
    assert perfect_square(15) is False
    assert perfect_square(26) is False


def test_perfect_square_negative():
    with pytest.raises(ValueError):
        perfect_square(-1)
    with pytest.raises(ValueError):
        perfect_square(-4)


def test_perfect_square_binary_search_nominal():
    assert perfect_square_binary_search(0) is True
    assert perfect_square_binary_search(1) is True
    assert perfect_square_binary_search(4) is True
    assert perfect_square_binary_search(9) is True
    assert perfect_square_binary_search(16) is True
    assert perfect_square_binary_search(100) is True


def test_perfect_square_binary_search_non_squares():
    assert perfect_square_binary_search(2) is False
    assert perfect_square_binary_search(3) is False
    assert perfect_square_binary_search(5) is False
    assert perfect_square_binary_search(24) is False
    assert perfect_square_binary_search(26) is False


def test_perfect_square_binary_search_negative():
    assert perfect_square_binary_search(-1) is False
    assert perfect_square_binary_search(-9) is False
