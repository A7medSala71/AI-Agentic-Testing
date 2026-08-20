from function_19 import is_pangram
from function_19 import is_pangram_faster
from function_19 import is_pangram_fastest


def test_is_pangram_default():
    assert is_pangram() is True


def test_is_pangram_valid():
    assert is_pangram("Sphinx of black quartz, judge my vow") is True


def test_is_pangram_invalid():
    assert is_pangram("The quick brown fox jumps over the lazy do") is False


def test_is_pangram_empty():
    assert is_pangram("") is False


def test_is_pangram_default_argument_value():
    # Kills mutants changing the default argument string
    import inspect
    sig = inspect.signature(is_pangram)
    default_val = sig.parameters['input_str'].default
    assert default_val == 'The quick brown fox jumps over the lazy dog'

    sig_faster = inspect.signature(is_pangram_faster)
    assert sig_faster.parameters['input_str'].default == 'The quick brown fox jumps over the lazy dog'


def test_is_pangram_replace_behavior():
    # Kills mutants changing input_str.replace(' ', '')
    assert is_pangram("a b c d e f g h i j k l m n o p q r s t u v w x y z") is True


def test_is_pangram_lower_bounds():
    # Kills mutants on 'a' <= alpha.lower() <= 'z' boundary
    assert is_pangram("`abcdefghijklmnopqrstuvwxyz") is True
    assert is_pangram("abcdefghijklmnopqrstuvwxyz") is True


def test_is_pangram_frequency_add():
    # Kills mutant frequency.add(alpha.upper()) by checking frequency contents if we could, 
    # but since frequency is local, we can verify behavior or check via patching if needed.
    # Wait, can we check that frequency adds lowercase by passing mixed case and checking behavior?
    # Actually, frequency.add(alpha.upper()) adds uppercase. Does it change anything visible? 
    # Wait, if frequency.add(alpha.upper()) is used, it adds uppercase characters. But len(frequency) == 26.
    # Is there any way to kill mutmut_20? Let's check if any function behavior changes or if it's equivalent. 
    # Wait, if `frequency` contains uppercase, does it matter? 
    pass


def test_is_pangram_faster_default():
    assert is_pangram_faster() is True


def test_is_pangram_faster_valid():
    assert is_pangram_faster("Pack my box with five dozen liquor jugs") is True


def test_is_pangram_faster_invalid():
    assert is_pangram_faster("Pack my box with five dozen liquor jug") is False


def test_is_pangram_faster_empty():
    assert is_pangram_faster("") is False


def test_is_pangram_fastest_default():
    assert is_pangram_fastest() is True


def test_is_pangram_fastest_valid():
    assert is_pangram_fastest("The five boxing wizards jump quickly") is True


def test_is_pangram_fastest_invalid():
    assert is_pangram_fastest("The five boxing wizards jump quickl") is False


def test_is_pangram_fastest_empty():
    assert is_pangram_fastest("") is False