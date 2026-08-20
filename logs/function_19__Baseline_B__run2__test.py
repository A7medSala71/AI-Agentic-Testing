import pytest
from function_19 import is_pangram
from function_19 import is_pangram_faster
from function_19 import is_pangram_fastest


def test_is_pangram_default():
    assert is_pangram() is True


def test_is_pangram_true():
    assert is_pangram("The quick brown fox jumps over the lazy dog") is True


def test_is_pangram_false():
    assert is_pangram("The quick brown fox jumps over the lazy do") is False


def test_is_pangram_boundary_length():
    assert is_pangram("abcdefghijklmnopqrstuvwxy") is False


def test_is_pangram_faster_default():
    assert is_pangram_faster() is True


def test_is_pangram_faster_true():
    assert is_pangram_faster("abcdefghijklmnopqrstuvwxyz") is True


def test_is_pangram_faster_uppercase():
    assert is_pangram_faster("BCDEFGHIJKLMNOPQRSTUVWXYZA") is True


def test_is_pangram_faster_with_spaces():
    assert is_pangram_faster("abcdefghijklmnopqrstuvwx yz") is True


def test_is_pangram_fastest_default():
    assert is_pangram_fastest() is True


def test_is_pangram_fastest_true():
    assert is_pangram_fastest("Pack my box with five dozen liquor jugs.") is True


def test_is_pangram_fastest_false():
    assert is_pangram_fastest("Pack my box with five dozen liquor jug") is False


def test_is_pangram_with_numbers_and_symbols():
    assert is_pangram("The quick brown fox jumps over the lazy dog 123!@#") is True
    assert is_pangram_faster("The quick brown fox jumps over the lazy dog 123!@#") is True
    assert is_pangram_fastest("The quick brown fox jumps over the lazy dog 123!@#") is True
