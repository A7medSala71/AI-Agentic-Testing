import pytest
from function_18 import signature
from function_18 import anagram


def test_signature_basic():
    assert signature("hello") == "e1h1l2o1"


def test_signature_empty():
    assert signature("") == ""


def test_signature_duplicates_and_order():
    assert signature("banana") == "a3b1n2"


def test_anagram_valid():
    res = anagram("silent")
    assert isinstance(res, list)
    assert "silent" in res
    assert "listen" in res


def test_anagram_no_match():
    res = anagram("zzzzzzzzzzzz")
    assert res == []
