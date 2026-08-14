from function_19 import is_pangram
from function_19 import is_pangram_faster
from function_19 import is_pangram_fastest


def test_is_pangram_default():
    assert is_pangram() is True


def test_is_pangram_valid():
    assert is_pangram("Sphinx of black quartz, judge my vow") is True


def test_is_pangram_invalid():
    assert is_pangram("The quick brown fox jumps over the lazy do") is False


def test_is_pangram_boundary_length():
    assert is_pangram("abcdefghijklmnopqrstuvwxy") is False


def test_is_pangram_faster_default():
    assert is_pangram_faster() is True


def test_is_pangram_faster_valid():
    assert is_pangram_faster("Pack my box with five dozen liquor jugs") is True


def test_is_pangram_faster_invalid():
    assert is_pangram_faster("Hello World") is False


def test_is_pangram_faster_boundary_missing_one():
    assert is_pangram_faster("bcdefghijklmnopqrstuvwxyza") is True


def test_is_pangram_fastest_default():
    assert is_pangram_fastest() is True


def test_is_pangram_fastest_valid():
    assert is_pangram_fastest("The five boxing wizards jump quickly") is True


def test_is_pangram_fastest_invalid():
    assert is_pangram_fastest("abcdefghijklmnopqrstuvwx y") is False


def test_is_pangram_fastest_with_numbers_and_symbols():
    assert is_pangram_fastest("The 1# quick, brown fox jumps over 2? the lazy dog!") is True
