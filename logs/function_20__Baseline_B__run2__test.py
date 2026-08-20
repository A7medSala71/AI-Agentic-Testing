from function_20 import is_palindrome
from function_20 import is_palindrome_traversal
from function_20 import is_palindrome_recursive
from function_20 import is_palindrome_slice
from function_20 import benchmark_function


def test_is_palindrome():
    assert is_palindrome("rotor") is True
    assert is_palindrome("MALAYALAM") is True
    assert is_palindrome("amanaplanacanalpanama") is True
    assert is_palindrome("String") is False
    assert is_palindrome("ABC") is False
    assert is_palindrome("abcdba") is False
    assert is_palindrome("") is True
    assert is_palindrome("A") is True
    assert is_palindrome("AB") is False
    assert is_palindrome("BB") is True


def test_is_palindrome_traversal():
    assert is_palindrome_traversal("rotor") is True
    assert is_palindrome_traversal("MALAYALAM") is True
    assert is_palindrome_traversal("String") is False
    assert is_palindrome_traversal("AB") is False
    assert is_palindrome_traversal("") is True
    assert is_palindrome_traversal("A") is True
    assert is_palindrome_traversal("BB") is True
    assert is_palindrome_traversal("amanaplanacanalpanama") is True
    assert is_palindrome_traversal("abcdba") is False


def test_is_palindrome_recursive():
    assert is_palindrome_recursive("rotor") is True
    assert is_palindrome_recursive("level") is True
    assert is_palindrome_recursive("ABC") is False
    assert is_palindrome_recursive("abcdba") is False
    assert is_palindrome_recursive("") is True
    assert is_palindrome_recursive("A") is True
    assert is_palindrome_recursive("AB") is False
    assert is_palindrome_recursive("MALAYALAM") is True
    assert is_palindrome_recursive("stringnotpal") is False


def test_is_palindrome_slice():
    assert is_palindrome_slice("rotor") is True
    assert is_palindrome_slice("MALAYALAM") is True
    assert is_palindrome_slice("String") is False
    assert is_palindrome_slice("AB") is False
    assert is_palindrome_slice("") is True
    assert is_palindrome_slice("A") is True
    assert is_palindrome_slice("BB") is True


def test_benchmark_function():
    benchmark_function("is_palindrome")
    benchmark_function("is_palindrome_traversal")
    benchmark_function("is_palindrome_recursive")
    benchmark_function("is_palindrome_slice")
