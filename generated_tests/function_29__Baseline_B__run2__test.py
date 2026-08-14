from function_29 import perfect_square
from function_29 import perfect_square_binary_search
import pytest


def test_perfect_square_nominal_true():
    assert perfect_square(0) is True
    assert perfect_square(1) is True
    assert perfect_square(4) is True
    assert perfect_square(9) is True
    assert perfect_square(16) is True
    assert perfect_square(25) is True


def test_perfect_square_nominal_false():
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


def test_perfect_square_binary_search_nominal_true():
    assert perfect_square_binary_search(0) is True
    assert perfect_square_binary_search(1) is True
    assert perfect_square_binary_search(4) is True
    assert perfect_square_binary_search(9) is True
    assert perfect_square_binary_search(16) is True
    assert perfect_square_binary_search(10000) is True


def test_perfect_square_binary_search_nominal_false():
    assert perfect_square_binary_search(2) is False
    assert perfect_square_binary_search(3) is False
    assert perfect_square_binary_search(8) is False
    assert perfect_square_binary_search(10) is False
    assert perfect_square_binary_search(99) is False


def test_perfect_square_binary_search_negative():
    assert perfect_square_binary_search(-1) is False
    assert perfect_square_binary_search(-9) is False
