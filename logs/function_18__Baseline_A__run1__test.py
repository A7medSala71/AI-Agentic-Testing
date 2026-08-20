import pytest
from function_18 import signature
from function_18 import anagram
from function_18 import word_by_signature


def test_signature_nominal():
    assert signature("banana") == "a3b1n2"


def test_signature_empty():
    assert signature("") == ""


def test_signature_sorted_order():
    assert signature("cba") == "a1b1c1"


def test_anagram_nominal():
    result = anagram("silent")
    assert isinstance(result, list)
    assert "silent" in result
    assert "listen" in result


def test_anagram_missing():
    result = anagram("zzzzzzzzzzzzz")
    assert result == []
