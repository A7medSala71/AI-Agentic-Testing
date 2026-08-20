from function_20 import is_palindrome
from function_20 import is_palindrome_traversal
from function_20 import is_palindrome_recursive
from function_20 import is_palindrome_slice
from function_20 import benchmark_function


def test_is_palindrome_nominal():
    assert is_palindrome("rotor") is True
    assert is_palindrome("String") is False


def test_is_palindrome_boundaries():
    assert is_palindrome("") is True
    assert is_palindrome("a") is True
    assert is_palindrome("ab") is False
    assert is_palindrome("aa") is True


def test_is_palindrome_traversal_nominal():
    assert is_palindrome_traversal("MALAYALAM") is True
    assert is_palindrome_traversal("abcdba") is False


def test_is_palindrome_traversal_boundaries():
    assert is_palindrome_traversal("") is True
    assert is_palindrome_traversal("A") is True
    assert is_palindrome_traversal("AB") is False


def test_is_palindrome_recursive_nominal():
    assert is_palindrome_recursive("level") is True
    assert is_palindrome_recursive("ABC") is False


def test_is_palindrome_recursive_boundaries():
    assert is_palindrome_recursive("") is True
    assert is_palindrome_recursive("BB") is True
    assert is_palindrome_recursive("AB") is False


def test_is_palindrome_slice_nominal():
    assert is_palindrome_slice("amanaplanacanalpanama") is True
    assert is_palindrome_slice("AB") is False


def test_is_palindrome_slice_boundaries():
    assert is_palindrome_slice("") is True
    assert is_palindrome_slice("a") is True


def test_benchmark_function_execution():
    benchmark_function("is_palindrome")
    benchmark_function("is_palindrome_traversal")
    benchmark_function("is_palindrome_recursive")
    benchmark_function("is_palindrome_slice")
