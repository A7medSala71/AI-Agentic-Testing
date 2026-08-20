from function_15 import merge_sort
import pytest


def test_merge_sort_empty_and_single():
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]


def test_merge_sort_already_sorted():
    assert merge_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_merge_sort_reverse_sorted():
    assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_merge_sort_unsorted_duplicates():
    assert merge_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_merge_sort_negative_numbers():
    assert merge_sort([-3, -1, -4, 0, 2, -2]) == [-4, -3, -2, -1, 0, 2]


def test_merge_sort_strings():
    assert merge_sort(["banana", "apple", "cherry", "date"]) == ["apple", "banana", "cherry", "date"]


def test_merge_sort_conditional_boundary_duplicates():
    # Mutant changes <= to < in merge; duplicate elements must remain stable (left comes before right)
    assert merge_sort([2, 2, 1]) == [1, 2, 2]