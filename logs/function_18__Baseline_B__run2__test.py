from function_18 import signature, anagram, word_by_signature


def test_signature_basic():
    assert signature('apple') == 'a1e1l1p2'


def test_signature_empty():
    assert signature('') == ''


def test_signature_single_char():
    assert signature('z') == 'z1'


def test_signature_duplicates():
    assert signature('banana') == 'a3b1n2'


def test_anagram_nominal():
    res = anagram('listen')
    assert isinstance(res, list)
    assert 'silent' in res
    assert 'listen' in res


def test_anagram_nonexistent():
    res = anagram('zzzzzzzzzz')
    assert res == []


def test_word_by_signature_mapping():
    sig = signature('silent')
    assert 'listen' in word_by_signature[sig]
    assert 'silent' in word_by_signature[sig]


def test_anagram_uppercase_input():
    res = anagram('LISTEN')
    assert isinstance(res, list)
    assert 'silent' in res
    assert 'listen' in res
