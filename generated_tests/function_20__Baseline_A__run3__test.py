from function_20 import is_palindrome, is_palindrome_traversal, is_palindrome_recursive, is_palindrome_slice, benchmark_function


def test_is_palindrome_nominal(): assert is_palindrome('MALAYALAM') is True; assert is_palindrome('String') is False; assert is_palindrome('rotor') is True


def test_is_palindrome_boundaries(): assert is_palindrome('') is True; assert is_palindrome('A') is True; assert is_palindrome('AB') is False; assert is_palindrome('BB') is True


def test_is_palindrome_traversal_nominal(): assert is_palindrome_traversal('level') is True; assert is_palindrome_traversal('ABC') is False; assert is_palindrome_traversal('amanaplanacanalpanama') is True


def test_is_palindrome_traversal_boundaries(): assert is_palindrome_traversal('') is True; assert is_palindrome_traversal('A') is True; assert is_palindrome_traversal('abcdba') is False


def test_is_palindrome_recursive_nominal(): assert is_palindrome_recursive('rotor') is True; assert is_palindrome_recursive('AB') is False; assert is_palindrome_recursive('MALAYALAM') is True


def test_is_palindrome_recursive_boundaries(): assert is_palindrome_recursive('') is True; assert is_palindrome_recursive('A') is True; assert is_palindrome_recursive('ABC') is False


def test_is_palindrome_slice_nominal(): assert is_palindrome_slice('level') is True; assert is_palindrome_slice('String') is False; assert is_palindrome_slice('amanaplanacanalpanama') is True


def test_is_palindrome_slice_boundaries(): assert is_palindrome_slice('') is True; assert is_palindrome_slice('A') is True; assert is_palindrome_slice('AB') is False


def test_benchmark_function_execution(): benchmark_function('is_palindrome_slice')
