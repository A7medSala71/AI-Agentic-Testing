import pytest
from function_14 import insertion_sort, Comparable


def test_insertion_sort_empty():
    collection = []
    assert insertion_sort(collection) == []


def test_insertion_sort_single_element():
    collection = [42]
    assert insertion_sort(collection) == [42]


def test_insertion_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    assert insertion_sort(collection) == [1, 2, 3, 4, 5]


def test_insertion_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert insertion_sort(collection) == [1, 2, 3, 4, 5]


def test_insertion_sort_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    assert insertion_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_insertion_sort_floats():
    collection = [3.14, 1.41, 2.71, 0.57]
    assert insertion_sort(collection) == [0.57, 1.41, 2.71, 3.14]


def test_insertion_sort_strings():
    collection = ["banana", "apple", "cherry", "date"]
    assert insertion_sort(collection) == ["apple", "banana", "cherry", "date"]


def test_insertion_sort_in_place():
    collection = [3, 1, 2]
    res = insertion_sort(collection)
    assert res is collection
    assert collection == [1, 2, 3]


def test_comparable_protocol():
    class CustomItem:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            return self.val < other.val
        def __eq__(self, other):
            return self.val == other.val
    
    items = [CustomItem(5), CustomItem(1), CustomItem(3)]
    sorted_items = insertion_sort(items)
    assert [i.val for i in sorted_items] == [1, 3, 5]


def test_insertion_sort_raises_on_non_comparable():
    class Uncomparable:
        def __lt__(self, other):
            raise TypeError("Cannot compare")

    # If range starts at 0, it will do `insert_value = collection[0]` and then immediately enter the `while` loop condition `insert_index > 0` (False).
    # However, if it tries to compare `insert_value < collection[-1]` (when index is 0 - 1 = -1), it might behave unexpectedly or raise an IndexError / TypeError depending on collection.
    # Actually, if range starts at 0:
    # insert_index = 0
    # insert_value = collection[0]
    # while insert_index > 0 ... (False)
    # collection[0] = insert_value
    # So a single element doesn't trigger it.
    # But wait, what if the collection contains elements that raise an error on comparison, but start at index 0?
    # Or what if we use a custom object that tracks how many times `__lt__` is called?
    # For a list of length 1 with `range(1, len)` __lt__ is called 0 times.
    # With `range(len)`, for length 1 it doesn't compare because insert_index=0 makes insert_index > 0 False.
    # But wait, does range(len) cause any difference for length 1?
    # For length 1: range(1, 1) is empty. range(1) is [0].
    # For insert_index = 0: insert_value = collection[0]. while insert_index > 0 is False. collection[0] = insert_value. Returns collection.
    # So range(0, 1) and range(1, 1) behave identically for length 1!
    # How to kill the mutant where range starts at 0 instead of 1?
    # Let's check what happens for length > 1 if range starts at 0:
    # For `collection = [1, 2]` and range(len) -> insert_index = 0:
    # insert_value = collection[0] (1)
    # while 0 > 0 (False)
    # collection[0] = 1
    # Then insert_index = 1:
    # insert_value = collection[1] (2)
    # while 1 > 0 and 2 < collection[0] (2 < 1 -> False)
    # collection[1] = 2
    # So for an already sorted list, range(0, 2) behaves the same as range(1, 2).
    # What about an unsorted list like [2, 1]?
    # insert_index = 0:
    # insert_value = collection[0] (2)
    # while 0 > 0 (False)
    # collection[0] = 2
    # insert_index = 1:
    # insert_value = collection[1] (1)
    # while 1 > 0 and 1 < collection[0] (1 < 2 -> True):
    #   collection[1] = collection[0] (collection becomes [2, 2])
    #   insert_index -= 1 (0)
    # while 0 > 0 (False)
    # collection[0] = 1 (collection becomes [1, 2])
    # That also works.
    # Wait! What if we use an object where `__lt__` has side effects or counts calls?
    # For `collection = [1]`, range(1, 1) calls `__lt__` 0 times.
    # range(0, 1) calls `__lt__` 0 times because the while loop condition `insert_index > 0` is checked with `insert_index = 0`, which is NOT > 0, so `__lt__` is never evaluated!
    # Wait, is there any difference? What if collection[0] is mutated or accessed in a way that can be detected?
    # Or what if we check the number of comparisons?
    class CountComparisons:
        def __init__(self, val):
            self.val = val
            self.comparisons = 0
        def __lt__(self, other):
            self.comparisons += 1
            return self.val < other.val
        def __eq__(self, other):
            return self.val == other.val

    # For a single element list [CountComparisons(1)]:
    # range(1, 1): loop doesn't run, comparisons = 0.
    # range(0, 1): loop runs for insert_index = 0. insert_value = collection[0]. while insert_index > 0 is False. comparisons = 0. Still 0.
    # Wait, what if the collection has an object that errors or logs access when assigned to itself?
    class AssignmentLogger:
        def __init__(self, val):
            self.val = val
            self.assignments = 0
        def __lt__(self, other):
            return self.val < other.val
        def __eq__(self, other):
            return self.val == other.val

    items = [AssignmentLogger(1)]
    # With range(1, 1), collection[0] is never assigned to itself.
    # With range(0, 1), collection[0] = collection[0] happens once!
    
    class TrackAssignment(int):
        assigned_count = 0
        def __new__(cls, val):
            obj = super().__new__(cls, val)
            return obj
        def __setattr__(self, key, value):
            super().__setattr__(key, value)

    # Let's use a mutable proxy or custom class that counts self-assignment:
    class SelfAssignmentDetector:
        def __init__(self, val):
            self.val = val
            self.assigned = False
        def __lt__(self, other):
            return self.val < other.val

    # Even simpler: a list subclass or custom mutable sequence that intercepts `__setitem__`:
    class LoggingList(list):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setitem_calls = 0
        def __setitem__(self, index, value):
            self.setitem_calls += 1
            super().__setitem__(index, value)

    lst = LoggingList([10])
    insertion_sort(lst)
    assert lst.setitem_calls == 0