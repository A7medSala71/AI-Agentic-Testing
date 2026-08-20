import pytest
from function_18 import signature, anagram, word_by_signature


def test_signature_nominal():
    assert signature("banana") == "a3b1n2"


def test_signature_empty():
    assert signature("") == ""


def test_signature_single_char():
    assert signature("z") == "z1"


def test_signature_order():
    assert signature("cba") == "a1b1c1"


def test_anagram_nominal():
    results = anagram("silent")
    assert "silent" in results
    assert "listen" in results
    assert sorted(results) == results


def test_anagram_nonexistent():
    assert anagram("xyzzyqazfoo") == []


def test_word_by_signature_structure():
    sig = signature("test")
    assert sig in word_by_signature
    assert "test" in word_by_signature[sig]
