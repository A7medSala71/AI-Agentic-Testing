import pytest
from function_18 import signature, anagram, word_by_signature


def test_signature_nominal():
    assert signature("banana") == "a3b1n2"


def test_signature_empty():
    assert signature("") == ""


def test_signature_single_char():
    assert signature("z") == "z1"


def test_signature_ordering():
    assert signature("cba") == "a1b1c1"


def test_anagram_nominal():
    results = anagram("listen")
    assert isinstance(results, list)
    assert "silent" in results
    assert "listen" in results


def test_anagram_no_match():
    results = anagram("zzzzzzzzzz")
    assert results == []
