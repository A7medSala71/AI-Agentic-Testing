from function_20 import is_palindrome, is_palindrome_traversal, is_palindrome_recursive, is_palindrome_slice, benchmark_function


def test_is_palindrome_nominal_and_boundaries(): assert is_palindrome("") is True; assert is_palindrome("a") is True; assert is_palindrome("aba") is True; assert is_palindrome("abba") is True; assert is_palindrome("abc") is False; assert is_palindrome("abca") is False


def test_is_palindrome_traversal_nominal_and_boundaries(): assert is_palindrome_traversal("") is True; assert is_palindrome_traversal("a") is True; assert is_palindrome_traversal("racecar") is True; assert is_palindrome_traversal("level") is True; assert is_palindrome_traversal("python") is False


def test_is_palindrome_recursive_nominal_and_boundaries(): assert is_palindrome_recursive("") is True; assert is_palindrome_recursive("a") is True; assert is_palindrome_recursive("malayalam") is True; assert is_palindrome_recursive("radar") is True; assert is_palindrome_recursive("hello") is False


def test_is_palindrome_slice_nominal_and_boundaries(): assert is_palindrome_slice("") is True; assert is_palindrome_slice("z") is True; assert is_palindrome_slice("rotor") is True; assert is_palindrome_slice("step on no pets") is True; assert is_palindrome_slice("slice") is False


def test_benchmark_function_execution(): benchmark_function("is_palindrome_slice")
