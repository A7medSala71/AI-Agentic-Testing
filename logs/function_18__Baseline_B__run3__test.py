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


def test_signature_duplicate_chars():
    assert signature("aaaaa") == "a5"


def test_anagram_nominal():
    result = anagram("listen")
    assert "silent" in result
    assert "listen" in result


def test_anagram_missing():
    res = anagram("zzzzzzzzzzzz")
    assert res == []
