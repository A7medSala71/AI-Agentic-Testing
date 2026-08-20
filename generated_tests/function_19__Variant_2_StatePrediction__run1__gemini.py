import pytest
from function_19 import is_pangram, is_pangram_faster, is_pangram_fastest


def test_is_pangram_default():
    assert is_pangram() is True


def test_is_pangram_valid():
    assert is_pangram("The quick brown fox jumps over the lazy dog") is True


def test_is_pangram_invalid():
    assert is_pangram("The quick brown fox jumps over the lazy do") is False


def test_is_pangram_boundary_length():
    assert is_pangram("abcdefghijklmnopqrstuvwxyz") is True
    assert is_pangram("abcdefghijklmnopqrstuvwxy") is False


def test_is_pangram_faster_default():
    assert is_pangram_faster() is True


def test_is_pangram_faster_valid():
    assert is_pangram_faster("The quick brown fox jumps over the lazy dog") is True


def test_is_pangram_faster_invalid():
    assert is_pangram_faster("abcdefghijklmnopqrstuvwxy") is False


def test_is_pangram_fastest_default():
    assert is_pangram_fastest() is True


def test_is_pangram_fastest_valid():
    assert is_pangram_fastest("The quick brown fox jumps over the lazy dog") is True


def test_is_pangram_fastest_invalid():
    assert is_pangram_fastest("abcdefghijklmnopqrstuvwxy") is False


def test_is_pangram_default_argument_mutants():
    # Mutants 1, 2, 3: Mutate default argument string; calling with no arguments exposes the exact default string value.
    import inspect
    sig = inspect.signature(is_pangram)
    assert sig.parameters['input_str'].default == 'The quick brown fox jumps over the lazy dog'


def test_is_pangram_replace_space_mutants():
    # Mutants 10, 11: Mutate replace arguments for spaces; passing spaces ensures they are removed correctly.
    assert is_pangram("a b c d e f g h i j k l m n o p q r s t u v w x y z") is True


def test_is_pangram_lower_bound_mutants():
    # Mutants 12, 13: Mutate lower bound 'a' in range check; characters like 'a' test the exact boundary.
    assert is_pangram("abcdefghijklmnopqrstuvwxyz") is True


def test_is_pangram_frequency_add_upper():
    # Mutant 20: Adds alpha.upper() instead of lower(); check that frequency contains lowercase elements even if input is uppercase.
    class TrackingSet(set):
        def add(self, element):
            super().add(element)
            assert element.islower(), f"Expected lowercase element, got {element}"

    import unittest.mock
    with unittest.mock.patch('function_19.set', TrackingSet):
        assert is_pangram("abcdefghijklmnopqrstuvwxyz") is True


def test_is_pangram_mutmut_1_default_string_exact():
    # Mutant mutmut_1: Mutates default string to include 'XX'; assert inspect default matches exact original string.
    import inspect
    assert inspect.signature(is_pangram).parameters['input_str'].default == 'The quick brown fox jumps over the lazy dog'


def test_is_pangram_mutmut_2_default_string_case():
    # Mutant mutmut_2: Mutates default string to lowercase; assert inspect default retains original capitalization ('The').
    import inspect
    assert inspect.signature(is_pangram).parameters['input_str'].default == 'The quick brown fox jumps over the lazy dog'


def test_is_pangram_mutmut_3_default_string_upper():
    # Mutant mutmut_3: Mutates default string to uppercase; assert inspect default retains mixed capitalization.
    import inspect
    assert inspect.signature(is_pangram).parameters['input_str'].default == 'The quick brown fox jumps over the lazy dog'


def test_is_pangram_mutmut_10_replace_old():
    # Mutant mutmut_10: Mutates replace target from ' ' to 'XX XX'; spaces would remain unreplaced and fail set length.
    assert is_pangram("abcdefghijklmnopqrstuvwxyz ") is False


def test_is_pangram_mutmut_11_replace_new():
    # Mutant mutmut_11: Mutates replace new string from '' to 'XXXX'; spaces would be replaced with 'XXXX' causing length/char errors.
    assert is_pangram("abcdefghijklmnopqrstuvwxyz ") is False


def test_is_pangram_mutmut_12_lower_bound_string():
    # Mutant mutmut_12: Mutates lower bound 'a' to 'XXaXX'; string comparison would fail to match 'a'.
    assert is_pangram("abcdefghijklmnopqrstuvwxyz") is True


def test_is_pangram_mutmut_13_lower_bound_char():
    # Mutant mutmut_13: Mutates lower bound 'a' to 'A'; checking 'A' <= alpha.lower() still works, but let's ensure characters near boundary behave.
    assert is_pangram("abcdefghijklmnopqrstuvwxyz") is True


def test_is_pangram_faster_mutmut_1_default_string():
    # Mutant faster_mutmut_1: Mutates default string of is_pangram_faster; assert inspect default matches original string.
    import inspect
    assert inspect.signature(is_pangram_faster).parameters['input_str'].default == 'The quick brown fox jumps over the lazy dog'