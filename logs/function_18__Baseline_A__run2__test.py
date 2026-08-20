import pytest
from function_18 import signature, anagram, word_by_signature


def test_signature_nominal():
    assert signature("banana") == "a3b1n2"


def test_signature_empty():
    assert signature("") == ""


def test_signature_single_char():
    assert signature("a") == "a1"


def test_signature_all_unique():
    assert signature("abc") == "a1b1c1"


def test_anagram_nominal():
    res = anagram("silent")
    assert "silent" in res
    assert "listen" in res
    assert sorted(res) == sorted(["silent", "listen", "enlist", "tinsel", "inlets", "elints"])


def test_anagram_no_match():
    res = anagram("zzzzzzzzzz")
    assert res == []
