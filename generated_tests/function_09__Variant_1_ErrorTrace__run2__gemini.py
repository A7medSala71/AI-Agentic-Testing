import pytest
from function_09 import binary_insertion_sort


def test_binary_insertion_sort_empty():
    collection = []
    res = binary_insertion_sort(collection)
    assert res == []


def test_binary_insertion_sort_single():
    collection = [42]
    res = binary_insertion_sort(collection)
    assert res == [42]


def test_binary_insertion_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    res = binary_insertion_sort(collection)
    assert res == [1, 2, 3, 4, 5]


def test_binary_insertion_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    res = binary_insertion_sort(collection)
    assert res == [1, 2, 3, 4, 5]


def test_binary_insertion_sort_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = binary_insertion_sort(collection)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_binary_insertion_sort_negative_numbers():
    collection = [-3, 5, 0, -1, 2]
    res = binary_insertion_sort(collection)
    assert res == [-3, -1, 0, 2, 5]


def test_binary_insertion_sort_mutates_in_place():
    collection = [3, 1, 2]
    res = binary_insertion_sort(collection)
    assert res is collection
    assert collection == [1, 2, 3]


def test_binary_insertion_sort_stability():
    # Tests stability and equality condition (value_to_insert <= collection[mid])
    # If the comparison is changed from < to <=, stability or correct insertion index with duplicates might be affected.
    # Let's use custom objects or pairs to check stable sorting of duplicates.
    class Item:
        def __init__(self, val, idx):
            self.val = val
            self.idx = idx
        def __lt__(self, other):
            return self.val < other.val
        def __le__(self, other):
            return self.val <= other.val
        def __eq__(self, other):
            return self.val == other.val and self.idx == other.idx
        def __repr__(self):
            return f"Item({self.val}, {self.idx})"

    # [Item(2, 0), Item(1, 0), Item(2, 1)] already sorted by primary value, but different index
    # With strict <, duplicates go to the right of existing elements, preserving stability.
    # With <=, duplicates might shift incorrectly.
    items = [Item(2, 0), Item(1, 0), Item(2, 1)]
    res = binary_insertion_sort(items)
    # Expected stable order:
    # 1st: Item(1, 0)
    # 2nd: Item(2, 0)
    # 3rd: Item(2, 1)
    assert res[0].val == 1
    assert res[1].val == 2
    assert res[1].idx == 0
    assert res[2].val == 2
    assert res[2].idx == 1


def test_binary_insertion_sort_immutable_elements():
    # Adding a check with elements that are immutable or mock objects to ensure range(1, n) starts properly
    # If range(0, n) runs, for i=0, value_to_insert = collection[0], low = 0, high = -1,
    # then while low <= high does not run, range(0, 0, -1) is empty, collection[0] = collection[0],
    # which usually passes for simple lists, but can be caught if we track mutations or calls,
    # or we can test with a type where assignment or operation at index 0 behaves strictly.
    # Wait, if range starts at 0, collection[0] = collection[0] is a no-op for a standard list,
    # but let's see why range(n) vs range(1, n) matters.
    # If i=0, value_to_insert = collection[0], low=0, high=-1. while loop skipped.
    # for j in range(0, 0, -1): (empty). collection[0] = collection[0].
    # So it doesn't crash on standard lists. However, if we pass a custom list class that tracks assignments or if we assert something specific.
    class TrackingList(list):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.assignments = 0
        def __setitem__(self, key, value):
            self.assignments += 1
            super().__setitem__(key, value)

    tl = TrackingList([10, 5])
    binary_insertion_sort(tl)
    # For [10, 5], n=2.
    # Correct (range(1, 2)): i=1 (value 5). low=0, high=0. mid=0. 5 < 10 -> high=-1.
    # range(1, 0, -1) -> j=1. collection[1] = collection[0] (10). collection[0] = 5.
    # Total assignments for i=1: one for shift, one for insertion = 2 assignments (or more depending on implementation).
    # If range(0, 2) runs: i=0 runs first. value=10, low=0, high=-1. range(0, 0, -1) empty. collection[0] = 10 (1 assignment).
    # Then i=1 runs normally.
    # Let's verify if assignment count or exact behavior differs.
    # Actually, even simpler: if collection contains an object that raises an error or if we check that index 0 is not redundantly processed.
    # Let's test a custom list where __setitem__ raises an error if index 0 is assigned when it's already in place, or similar.
    class StrictList(list):
        def __setitem__(self, key, value):
            if key == 0 and value == self[key]:
                raise ValueError("Should not reassign index 0")
            super().__setitem__(key, value)

    sl = StrictList([10, 5])
    res = binary_insertion_sort(sl)
    assert res == [5, 10]