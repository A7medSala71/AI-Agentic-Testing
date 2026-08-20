import pytest
from function_19 import is_pangram
from function_19 import is_pangram_faster
from function_19 import is_pangram_fastest


def test_is_pangram_default():
    assert is_pangram() is True


def test_is_pangram_true():
    assert is_pangram('Pack my box with five dozen liquor jugs') is True


def test_is_pangram_false():
    assert is_pangram('The quick brown fox jumps over the lazy do') is False


def test_is_pangram_boundary_25():
    assert is_pangram('abcdefghijklmnopqrstuvwxy') is False


def test_is_pangram_faster_default():
    assert is_pangram_faster() is True


def test_is_pangram_faster_true():
    assert is_pangram_faster('ABCDEFGHIJKLMNOPQRSTUVWXYZ') is True


def test_is_pangram_faster_false():
    assert is_pangram_faster('abcdefghijklmnopqrstuvwx') is False


def test_is_pangram_fastest_default():
    assert is_pangram_fastest() is True


def test_is_pangram_fastest_true():
    assert is_pangram_fastest('Sphinx of black quartz, judge my vow.') is True


def test_is_pangram_fastest_false():
    assert is_pangram_fastest('abc') is False


def test_is_pangram_default_argument_check():
    # Kills mutmut_1, mutmut_2, mutmut_3 by explicitly asserting the default parameter value
    import inspect
    sig = inspect.signature(is_pangram)
    assert sig.parameters['input_str'].default == 'The quick brown fox jumps over the lazy dog'


def test_is_pangram_replace_behavior():
    # Kills mutmut_10, mutmut_11 by testing a string where spaces matter or multiple spaces are handled
    assert is_pangram('The quick brown fox jumps over the lazy dog') is True


def test_is_pangram_lower_bounds():
    # Kills mutmut_12, mutmut_13, mutmut_20 by testing non-alpha / boundary characters like digits or symbols
    # If 'a' is mutated to 'A' or 'XXaXX', behavior on strings with lowercase letters might change.
    # Also frequency.add(alpha.upper()) would store uppercase letters and fail len(frequency) == 26 check
    # if we pass an all-lowercase pangram containing 26 letters.
    alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    assert is_pangram(alphabet_lower) is True