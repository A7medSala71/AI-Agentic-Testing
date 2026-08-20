import pytest
from function_19 import is_pangram, is_pangram_faster, is_pangram_fastest
import inspect


def test_is_pangram_default():
    assert is_pangram() is True


def test_is_pangram_explicit_true():
    assert is_pangram('Pack my box with five dozen liquor jugs.') is True


def test_is_pangram_false():
    assert is_pangram('The quick brown fox jumps over the lazy do') is False


def test_is_pangram_boundary_25_letters():
    assert is_pangram('abcdefghijklmnopqrstuvwxy') is False


def test_is_pangram_faster_default():
    assert is_pangram_faster() is True


def test_is_pangram_faster_explicit_true():
    assert is_pangram_faster('Sphinx of black quartz, judge my vow.') is True


def test_is_pangram_faster_false():
    assert is_pangram_faster('Hello World') is False


def test_is_pangram_fastest_default():
    assert is_pangram_fastest() is True


def test_is_pangram_fastest_explicit_true():
    assert is_pangram_fastest('The five boxing wizards jump quickly.') is True


def test_is_pangram_fastest_false():
    assert is_pangram_fastest('abcdefghijklmnopqrstuvwx') is False


def test_is_pangram_default_argument_mutations():
    # Mutant mutmut_1/2/3: signature default string for is_pangram is mutated, so inspect default must match original exactly.
    assert inspect.signature(is_pangram).parameters['input_str'].default == 'The quick brown fox jumps over the lazy dog'


def test_is_pangram_replace_space_mutations():
    # Mutant mutmut_10/11: replace(' ', '') mutated to replace 'XX XX' or 'XXXX', so spaces are retained and counted or replaced incorrectly, affecting length when spaces are present.
    assert is_pangram('the quick brown fox jumps over the lazy dog') is True


def test_is_pangram_lower_boundary_mutations():
    # Mutant mutmut_12/13: 'a' changed to 'XXaXX' or 'A' in the range check.
    assert is_pangram('`bcdefghijklmnopqrstuvwxyz') is False
    assert is_pangram('Abcdefghijklmnopqrstuvwxyz') is True


def test_is_pangram_frequency_add_case():
    # Mutant mutmut_20: frequency.add(alpha.upper()) adds uppercase chars instead of lowercase, which can be observed by inspecting frequency if we could, but since we cannot, let's make sure the set contains lowercase letters by monkeypatching or verifying behavior if possible. Wait, does frequency contain uppercase? Since len(frequency) == 26 and we can check if it returns true, wait, does mutmut_20 change the return value? No, but let's see if we can check internal set by passing a custom dict/set if accessible, or if any other function uses it. Since it's local, we can test that calling it works. Wait, to kill mutmut_20 where frequency.add(alpha.upper()) is used, does it make any difference to len()? No. But wait, is there any test for mutmut_20? Let's keep it or add a test that checks exact behavior if applicable.
    assert is_pangram('The quick brown fox jumps over the lazy dog') is True


def test_is_pangram_faster_default_argument_mutations():
    # Mutant is_pangram_faster mutmut_1/2: signature default string for is_pangram_faster is mutated, so inspect default must match original exactly.
    assert inspect.signature(is_pangram_faster).parameters['input_str'].default == 'The quick brown fox jumps over the lazy dog'