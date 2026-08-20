import pytest
from function_18 import signature
from function_18 import anagram


def test_signature_basic():
    assert signature('banana') == 'a3b1n2'
    assert signature('hello') == 'e1h1l2o1'


def test_signature_empty():
    assert signature('') == ''


def test_signature_single_char():
    assert signature('a') == 'a1'
    assert signature('z') == 'z1'


def test_signature_all_same():
    assert signature('aaaa') == 'a4'


def test_anagram_valid():
    res = anagram('silent')
    assert 'silent' in res
    assert 'listen' in res
    assert isinstance(res, list)


def test_anagram_unknown():
    res = anagram('xyzzyqwerty')
    assert res == []
