import pytest
from function_19 import is_pangram, is_pangram_faster, is_pangram_fastest


def test_is_pangram_default():
    assert is_pangram() is True
    # Kill default value mutants (mutmut_1, mutmut_2, mutmut_3) by inspecting the function signature default
    assert is_pangram.__defaults__[0] == 'The quick brown fox jumps over the lazy dog'


def test_is_pangram_valid():
    assert is_pangram('abcdefghijklmnopqrstuvwxyz') is True
    assert is_pangram('Pack my box with five dozen liquor jugs.') is True


def test_is_pangram_invalid():
    assert is_pangram('The quick brown fox jumps over the lazy do') is False
    assert is_pangram('') is False


def test_is_pangram_replace_and_bounds():
    # Kill mutmut_10 (replace 'XX XX') and mutmut_11 (replace ' ', 'XXXX')
    # If spaces aren't replaced correctly, extra spaces would be counted as characters or mess up length
    assert is_pangram('abcdefghijklmnopqrstuvwxyz ') is True
    # Kill mutmut_12 ('XXaXX' <= ...) and mutmut_13 ('A' <= ...) and mutmut_20 (frequency.add(alpha.upper()))
    # Test uppercase and boundary characters like 'a'
    assert is_pangram('ABCDEFGHIJKLMNOPQRSTUVWXYZ') is True
    assert is_pangram('a bcdefghijklmnopqrstuvwxyz') is True


def test_is_pangram_faster_default():
    assert is_pangram_faster() is True


def test_is_pangram_faster_valid():
    assert is_pangram_faster('abcdefghijklmnopqrstuvwxyz') is True
    assert is_pangram_faster('ABCDEFGHIJKLMNOPQRSTUVWXYZ') is True


def test_is_pangram_faster_invalid():
    assert is_pangram_faster('abcdefghijklmnopqrstuvwxy') is False
    assert is_pangram_faster('') is False


def test_is_pangram_fastest_default():
    assert is_pangram_fastest() is True


def test_is_pangram_fastest_valid():
    assert is_pangram_fastest('abcdefghijklmnopqrstuvwxyz') is True
    assert is_pangram_fastest('Sphinx of black quartz, judge my vow.') is True


def test_is_pangram_fastest_invalid():
    assert is_pangram_fastest('abc') is False
    assert is_pangram_fastest('') is False