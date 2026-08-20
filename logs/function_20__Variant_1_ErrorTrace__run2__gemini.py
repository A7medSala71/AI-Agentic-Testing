from function_20 import is_palindrome
from function_20 import is_palindrome_traversal
from function_20 import is_palindrome_recursive
from function_20 import is_palindrome_slice
from function_20 import benchmark_function


def test_is_palindrome_nominal(): assert is_palindrome("rotor") is True; assert is_palindrome("python") is False; assert is_palindrome("a") is True; assert is_palindrome("") is True


def test_is_palindrome_traversal_nominal(): assert is_palindrome_traversal("level") is True; assert is_palindrome_traversal("abc") is False; assert is_palindrome_traversal("bb") is True; assert is_palindrome_traversal("") is True


def test_is_palindrome_recursive_nominal(): assert is_palindrome_recursive("MALAYALAM") is True; assert is_palindrome_recursive("AB") is False; assert is_palindrome_recursive("a") is True; assert is_palindrome_recursive("") is True


def test_is_palindrome_slice_nominal(): assert is_palindrome_slice("amanaplanacanalpanama") is True; assert is_palindrome_slice("abcdba") is False; assert is_palindrome_slice("x") is True; assert is_palindrome_slice("") is True


def test_benchmark_function_valid(capsys): benchmark_function("is_palindrome"); captured = capsys.readouterr(); assert "finished" in captured.out
