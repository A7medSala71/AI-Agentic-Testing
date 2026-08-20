import pytest
from function_18 import signature, anagram, word_by_signature


def test_signature_basic():
    assert signature("cat") == "a1c1t1"


def test_signature_duplicates():
    assert signature("banana") == "a3b1n2"


def test_signature_empty():
    assert signature("") == ""


def test_anagram_valid():
    res = anagram("cat")
    assert isinstance(res, list)
    assert "cat" in res
    assert "act" in res
    assert "tac" in res


def test_anagram_not_in_dict():
    res = anagram("zzzzzzzzz")
    assert res == []
