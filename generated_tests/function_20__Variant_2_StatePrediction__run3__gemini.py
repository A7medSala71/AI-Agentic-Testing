import pytest
from function_20 import is_palindrome
from function_20 import is_palindrome_traversal
from function_20 import is_palindrome_recursive
from function_20 import is_palindrome_slice
from function_20 import benchmark_function


def test_is_palindrome_nominal_true(): assert is_palindrome("MALAYALAM") is True; assert is_palindrome("rotor") is True; assert is_palindrome("A") is True; assert is_palindrome("BB") is True


def test_is_palindrome_nominal_false(): assert is_palindrome("String") is False; assert is_palindrome("ABC") is False; assert is_palindrome("abcdba") is False; assert is_palindrome("AB") is False


def test_is_palindrome_empty(): assert is_palindrome("") is True


def test_is_palindrome_traversal_nominal_true(): assert is_palindrome_traversal("MALAYALAM") is True; assert is_palindrome_traversal("rotor") is True; assert is_palindrome_traversal("level") is True


def test_is_palindrome_traversal_nominal_false(): assert is_palindrome_traversal("String") is False; assert is_palindrome_traversal("ABC") is False


def test_is_palindrome_traversal_empty(): assert is_palindrome_traversal("") is True


def test_is_palindrome_recursive_nominal_true(): assert is_palindrome_recursive("MALAYALAM") is True; assert is_palindrome_recursive("rotor") is True; assert is_palindrome_recursive("A") is True


def test_is_palindrome_recursive_nominal_false(): assert is_palindrome_recursive("String") is False; assert is_palindrome_recursive("ABC") is False


def test_is_palindrome_recursive_empty(): assert is_palindrome_recursive("") is True


def test_is_palindrome_slice_nominal_true(): assert is_palindrome_slice("MALAYALAM") is True; assert is_palindrome_slice("rotor") is True; assert is_palindrome_slice("level") is True


def test_is_palindrome_slice_nominal_false(): assert is_palindrome_slice("String") is False; assert is_palindrome_slice("ABC") is False


def test_is_palindrome_slice_empty(): assert is_palindrome_slice("") is True


def test_benchmark_function_execution(): benchmark_function("is_palindrome")
