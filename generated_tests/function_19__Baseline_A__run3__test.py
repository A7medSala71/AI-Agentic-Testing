import pytest
from function_19 import is_pangram, is_pangram_faster, is_pangram_fastest


def test_is_pangram_default():
    assert is_pangram() is True


def test_is_pangram_true():
    assert is_pangram("The quick brown fox jumps over the lazy dog") is True


def test_is_pangram_false():
    assert is_pangram("The quick brown fox jumps over the lazy do") is False


def test_is_pangram_boundary_less_than_26():
    assert is_pangram("abcdefghijklmnopqrstuvwxy") is False


def test_is_pangram_faster_default():
    assert is_pangram_faster() is True


def test_is_pangram_faster_true():
    assert is_pangram_faster("The quick brown fox jumps over the lazy dog") is True


def test_is_pangram_faster_false():
    assert is_pangram_faster("abcdefghijklmnopqrstuvwxz") is False


def test_is_pangram_faster_ascii_boundaries():
    assert is_pangram_faster("ABCDEFGHIJKLMNOPQRSTUVWXYZ") is True


def test_is_pangram_fastest_default():
    assert is_pangram_fastest() is True


def test_is_pangram_fastest_true():
    assert is_pangram_fastest("The quick brown fox jumps over the lazy dog") is True


def test_is_pangram_fastest_false():
    assert is_pangram_fastest("abc") is False
