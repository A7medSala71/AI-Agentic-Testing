from function_20 import is_palindrome
from function_20 import is_palindrome_traversal
from function_20 import is_palindrome_recursive
from function_20 import is_palindrome_slice
from function_20 import benchmark_function


assert is_palindrome("rotor") is True
assert is_palindrome("String") is False


assert is_palindrome("") is True
assert is_palindrome("A") is True
assert is_palindrome("AB") is False


assert is_palindrome_traversal("MALAYALAM") is True
assert is_palindrome_traversal("abcba") is True
assert is_palindrome_traversal("abcdba") is False


assert is_palindrome_traversal("") is True
assert is_palindrome_traversal("X") is True
assert is_palindrome_traversal("XY") is False


assert is_palindrome_recursive("level") is True
assert is_palindrome_recursive("amanaplanacanalpanama") is True
assert is_palindrome_recursive("ABC") is False


assert is_palindrome_recursive("") is True
assert is_palindrome_recursive("Z") is True
assert is_palindrome_recursive("ZZZ") is True
assert is_palindrome_recursive("ZZX") is False


assert is_palindrome_slice("rotor") is True
assert is_palindrome_slice("BB") is True
assert is_palindrome_slice("AB") is False


assert is_palindrome_slice("") is True
assert is_palindrome_slice("a") is True


benchmark_function("is_palindrome_slice")
benchmark_function("is_palindrome")
benchmark_function("is_palindrome_traversal")
benchmark_function("is_palindrome_recursive")
