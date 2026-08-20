import pytest
from function_18 import signature
from function_18 import anagram
from function_18 import word_by_signature


def test_signature_nominal():
    assert signature("banana") == "a3b1n2"


def test_signature_empty():
    assert signature("") == ""


def test_signature_single_char():
    assert signature("z") == "z1"


def test_anagram_nominal():
    sig = signature("silent")
    result = anagram("silent")
    assert "silent" in result
    assert "listen" in result
    for word in result:
        assert signature(word) == sig


def test_anagram_missing_signature():
    # defaultdict returns empty list for missing keys
    assert anagram("zzzzzzzzzzzz") == []
