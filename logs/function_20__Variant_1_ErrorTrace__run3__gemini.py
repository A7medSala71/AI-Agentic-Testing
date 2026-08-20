from function_20 import is_palindrome, is_palindrome_traversal, is_palindrome_recursive, is_palindrome_slice, benchmark_function


def test_is_palindrome_nominal_true(): assert is_palindrome("MALAYALAM") is True
assert is_palindrome("rotor") is True
assert is_palindrome("level") is True


def test_is_palindrome_nominal_false(): assert is_palindrome("String") is False
assert is_palindrome("ABC") is False
assert is_palindrome("AB") is False


def test_is_palindrome_boundaries(): assert is_palindrome("") is True
assert is_palindrome("A") is True
assert is_palindrome("BB") is True
assert is_palindrome("abcdba") is False


def test_is_palindrome_traversal_nominal_true(): assert is_palindrome_traversal("MALAYALAM") is True
assert is_palindrome_traversal("rotor") is True


def test_is_palindrome_traversal_nominal_false(): assert is_palindrome_traversal("String") is False
assert is_palindrome_traversal("ABC") is False


def test_is_palindrome_traversal_boundaries(): assert is_palindrome_traversal("") is True
assert is_palindrome_traversal("A") is True
assert is_palindrome_traversal("BB") is True


def test_is_palindrome_recursive_nominal_true(): assert is_palindrome_recursive("MALAYALAM") is True
assert is_palindrome_recursive("amanaplanacanalpanama") is True


def test_is_palindrome_recursive_nominal_false(): assert is_palindrome_recursive("String") is False
assert is_palindrome_recursive("abcdba") is False


def test_is_palindrome_recursive_boundaries(): assert is_palindrome_recursive("") is True
assert is_palindrome_recursive("A") is True
assert is_palindrome_recursive("AB") is False


def test_is_palindrome_slice_nominal_true(): assert is_palindrome_slice("MALAYALAM") is True
assert is_palindrome_slice("rotor") is True


def test_is_palindrome_slice_nominal_false(): assert is_palindrome_slice("String") is False
assert is_palindrome_slice("ABC") is False


def test_is_palindrome_slice_boundaries(): assert is_palindrome_slice("") is True
assert is_palindrome_slice("A") is True
assert is_palindrome_slice("BB") is True


def test_benchmark_function_execution(): benchmark_function("is_palindrome")
