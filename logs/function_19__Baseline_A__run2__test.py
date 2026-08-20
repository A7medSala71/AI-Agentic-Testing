from function_19 import is_pangram
from function_19 import is_pangram_faster
from function_19 import is_pangram_fastest
import pytest


def test_is_pangram_default():
    assert is_pangram() is True


def test_is_pangram_valid():
    assert is_pangram("The quick brown fox jumps over the lazy dog") is True


def test_is_pangram_invalid():
    assert is_pangram("The quick brown fox jumps over the lazy do") is False


def test_is_pangram_boundary_empty():
    assert is_pangram("") is False


def test_is_pangram_faster_default():
    assert is_pangram_faster() is True


def test_is_pangram_faster_valid():
    assert is_pangram_faster("abcdefghijklmnopqrstuvwxyz") is True


def test_is_pangram_faster_invalid():
    assert is_pangram_faster("abcdefghijklmnopqrstuvwxy") is False


def test_is_pangram_faster_boundary_empty():
    assert is_pangram_faster("") is False


def test_is_pangram_fastest_default():
    assert is_pangram_fastest() is True


def test_is_pangram_fastest_valid():
    assert is_pangram_fastest("Pack my box with five dozen liquor jugs.") is True


def test_is_pangram_fastest_invalid():
    assert is_pangram_fastest("pack my box with five dozen liquor jug") is False


def test_is_pangram_fastest_boundary_empty():
    assert is_pangram_fastest("") is False
