from function_19 import is_pangram
from function_19 import is_pangram_faster
from function_19 import is_pangram_fastest


def test_is_pangram_default():
    assert is_pangram() is True


def test_is_pangram_valid():
    assert is_pangram('Pack my box with five dozen liquor jugs') is True


def test_is_pangram_invalid():
    assert is_pangram('The quick brown fox jumps over the lazy do') is False


def test_is_pangram_empty():
    assert is_pangram('') is False


def test_is_pangram_faster_default():
    assert is_pangram_faster() is True


def test_is_pangram_faster_valid():
    assert is_pangram_faster('Sphinx of black quartz, judge my vow') is True


def test_is_pangram_faster_invalid():
    assert is_pangram_faster('abcdefghijklmnopqrstuvwxy') is False


def test_is_pangram_faster_empty():
    assert is_pangram_faster('') is False


def test_is_pangram_fastest_default():
    assert is_pangram_fastest() is True


def test_is_pangram_fastest_valid():
    assert is_pangram_fastest('The five boxing wizards jump quickly') is True


def test_is_pangram_fastest_invalid():
    assert is_pangram_fastest('abcdefghijklmnopqrstuvwx') is False


def test_is_pangram_fastest_empty():
    assert is_pangram_fastest('') is False


def test_pangram_with_numbers_and_punctuation():
    pangram_with_extras = 'Pack my box with 5 dozen liquor jugs!?'
    assert is_pangram(pangram_with_extras) is True
    assert is_pangram_faster(pangram_with_extras) is True
    assert is_pangram_fastest(pangram_with_extras) is True
