import pytest
from function_18 import signature, anagram, word_by_signature


def test_signature_basic():
    assert signature('apple') == 'a1e1l1p2'


def test_signature_empty():
    assert signature('') == ''


def test_signature_single_char():
    assert signature('z') == 'z1'


def test_signature_duplicates():
    assert signature('aaaaa') == 'a5'


def test_anagram_found():
    results = anagram('listen')
    assert 'silent' in results
    assert 'listen' in results


def test_anagram_nonexistent():
    results = anagram('zzzzzzzzzz')
    assert results == []
