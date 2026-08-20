from function_20 import is_palindrome, is_palindrome_traversal, is_palindrome_recursive, is_palindrome_slice, benchmark_function


def test_is_palindrome_nominal_true(): assert is_palindrome("MALAYALAM") is True


def test_is_palindrome_nominal_false(): assert is_palindrome("String") is False


def test_is_palindrome_even_true(): assert is_palindrome("BB") is True


def test_is_palindrome_single_char(): assert is_palindrome("A") is True


def test_is_palindrome_empty(): assert is_palindrome("") is True


def test_is_palindrome_mismatch_at_edges(): assert is_palindrome("abcdba") is False


def test_is_palindrome_traversal_true(): assert is_palindrome_traversal("rotor") is True


def test_is_palindrome_traversal_false(): assert is_palindrome_traversal("AB") is False


def test_is_palindrome_traversal_empty(): assert is_palindrome_traversal("") is True


def test_is_palindrome_recursive_true(): assert is_palindrome_recursive("level") is True


def test_is_palindrome_recursive_false(): assert is_palindrome_recursive("ABC") is False


def test_is_palindrome_recursive_base_cases(): assert is_palindrome_recursive("X") is True and is_palindrome_recursive("") is True


def test_is_palindrome_slice_true(): assert is_palindrome_slice("amanaplanacanalpanama") is True


def test_is_palindrome_slice_false(): assert is_palindrome_slice("abcdba") is False


def test_benchmark_function(): benchmark_function("is_palindrome_slice")
