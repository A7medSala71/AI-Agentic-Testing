import pytest
from function_18 import signature, anagram, word_by_signature


def test_signature_basic():
    assert signature('apple') == 'a1e1l1p2'


def test_signature_empty():
    assert signature('') == ''


def test_signature_single_char():
    assert signature('z') == 'z1'


def test_signature_repeated_chars():
    assert signature('bbbb') == 'b4'


def test_anagram_nominal():
    res = anagram('listen')
    assert isinstance(res, list)
    assert 'silent' in res
    assert 'listen' in res


def test_anagram_missing():
    res = anagram('xzxzxzxzxzxz')
    assert res == []
