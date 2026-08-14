from function_29 import perfect_square
from function_29 import perfect_square_binary_search
import pytest


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
    assert perfect_square(8) is False
    assert perfect_square(15) is False
    assert perfect_square(26) is False


def test_perfect_square_negative():
    assert perfect_square(-1) is False
    assert perfect_square(-4) is False


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
    assert perfect_square_binary_search(99) is False
    assert perfect_square_binary_search(101) is False


def test_perfect_square_binary_search_negative():
    assert perfect_square_binary_search(-1) is False
    assert perfect_square_binary_search(-9) is False


def test_perfect_square_binary_search_boundaries():
    assert perfect_square_binary_search(1000000) is True
    assert perfect_square_binary_search(1000001) is False
