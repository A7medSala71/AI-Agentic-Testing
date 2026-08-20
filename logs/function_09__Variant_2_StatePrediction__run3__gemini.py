import pytest
from function_09 import binary_insertion_sort


def test_binary_insertion_sort_empty():
    collection = []
    res = binary_insertion_sort(collection)
    assert res == []
    assert res is collection


def test_binary_insertion_sort_single_element():
    collection = [42]
    res = binary_insertion_sort(collection)
    assert res == [42]
    assert res is collection


def test_binary_insertion_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    res = binary_insertion_sort(collection)
    assert res == [1, 2, 3, 4, 5]
    assert res is collection


def test_binary_insertion_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    res = binary_insertion_sort(collection)
    assert res == [1, 2, 3, 4, 5]
    assert res is collection


def test_binary_insertion_sort_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = binary_insertion_sort(collection)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    assert res is collection


def test_binary_insertion_sort_negative_numbers():
    collection = [-3, 5, 0, -1, 2]
    res = binary_insertion_sort(collection)
    assert res == [-3, -1, 0, 2, 5]
    assert res is collection


def test_binary_insertion_sort_strings():
    collection = ["banana", "apple", "cherry", "date"]
    res = binary_insertion_sort(collection)
    assert res == ["apple", "banana", "cherry", "date"]
    assert res is collection


def test_binary_insertion_sort_range_zero_start():
    # Mutator mutmut_4 changes range(1, n) to range(n); for a single element list [1], range(n) starts at i=0 causing collection[0] to be re-assigned to itself unnecessarily or break assumptions.
    # State divergence: range starts at 0 instead of 1, but with collection=[1], value_to_insert = collection[0] (1), low=0, high=-1, loop doesn't run, shifts nothing, but mutating range(n) on e.g. a list or verifying strict execution or side-effects. Wait, if i=0, value_to_insert = collection[0], high = -1, low = 0, inner shifts can trigger. Let's test with a simple collection where i=0 does something harmful or just returns correctly. Actually, for range(n), when i=0, value_to_insert=collection[0], low=0, high=-1, while loop low<=high (0 <= -1) is False, inner loop range(0, 0, -1) is empty, collection[0] = collection[0]. But wait, what if the collection has elements where i=0 affects things or we can check that it doesn't fail? Wait, mutmut_4 survived because no test failed. Let's make sure a test explicitly exercises it or fails if range starts at 0. Wait, if range starts at 0, for i=0, high = -1, low = 0, collection[0] = collection[0]. But what if collection has items? Does it change behavior? Let's check with a specific collection or mock/spy, or a collection where starting at 0 does something observable if not careful, or maybe it's equivalent for i=0? Wait! If i=0, high = i - 1 = -1. low = 0. while low <= high (0 <= -1) is False. for j in range(0, 0, -1) is empty. collection[0] = collection[0]. It's a no-op for i=0! But wait, does mutmut_4 survive because it's a no-op? If it's a no-op, how to kill it? Ah, if range(n) starts at 0, does it do something else? Wait, if i=0, `high = i - 1` is `-1`. If `collection` is mutated or if we assert something about the number of iterations or if we use an object with __lt__ / assignment tracking to count operations, we can catch it!
    class TrackedInt:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            return self.val < other.val
        def __repr__(self):
            return str(self.val)
    
    # If range starts at 1, for [TrackedInt(1)], range(1, 1) is empty (0 iterations).
    # If range starts at 0, for [TrackedInt(1)], range(1) gives i=0 (1 iteration).
    # Let's count how many times __lt__ or assignments happen, or simply check that sorting a list of length 1 doesn't perform comparisons/assignments for i=0.
    comparisons = []
    class CompTracked:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            comparisons.append((self.val, other.val))
            return self.val < other.val

    col = [CompTracked(1)]
    binary_insertion_sort(col)
    # Original: range(1, 1) is empty, so 0 comparisons. Mutated (range(1)): i=0 executes, 0 <= -1 is False, so 0 comparisons too? Wait, let's check if high = i - 1 makes high = -1. Yes.
    # What about a list of length 2? Original: range(1, 2) -> i=1 (1 iteration). Mutated: range(2) -> i=0, then i=1 (2 iterations).
    # For i=0 with [CompTracked(2), CompTracked(1)]:
    # i=0: value=2, low=0, high=-1, while loop doesn't run, low=0, inner loop range(0, 0, -1) empty, collection[0]=2.
    # So for i=0 it does a redundant self-assignment. But does it compare? No comparison for i=0.
    # How to catch range(n) vs range(1, n)? When n=0, range(0) is empty, range(1, 0) is empty. When n=1, range(1) has i=0, range(1, 1) is empty.
    # So for n=1, original does NOT execute the body for i=0, whereas mutated DOES execute the body for i=0!
    # Even though it's a self-assignment, we can detect it if collection items detect assignment!
    assignments = 0
    class AssignTracked:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            return self.val < other.val
        def __setitem__(self, idx, val):
            nonlocal assignments
            assignments += 1

    # Python lists don't allow overriding __setitem__ from instance, but we can subclass list or use a custom sequence, or check item mutation via a wrapper property if list stores objects.
    # Wait, collection is a list. Can we subclass list?
    class TrackedList(list):
        def __setitem__(self, index, value):
            nonlocal assignments
            assignments += 1
            super().__setitem__(index, value)

    t_col = TrackedList([10])
    binary_insertion_sort(t_col)
    # Original range(1, 1) -> 0 assignments. Mutated range(1) -> i=0 executes collection[0] = collection[0], which calls __setitem__!
    assert assignments == 0


def test_binary_insertion_sort_conditional_boundary():
    # Mutant mutmut_18 changes `value_to_insert < collection[mid]` to `value_to_insert <= collection[mid]`.
    # When value_to_insert equals collection[mid], original goes to `else:` (low = mid + 1), whereas mutated goes to `if` (high = mid - 1).
    # This places duplicate/equal elements to the wrong side (before instead of after/stable insertion).
    # We can detect this stability/duplicate insertion divergence:
    class Item:
        def __init__(self, val, original_index):
            self.val = val
            self.index = original_index
        def __lt__(self, other):
            return self.val < other.val
        def __repr__(self):
            return f"Item({self.val}, {self.index})"

    # Two equal values: Item(1, 0) and Item(1, 1). Stable sort must keep Item(1, 0) before Item(1, 1).
    a = Item(1, 0)
    b = Item(1, 1)
    collection = [a, b]
    res = binary_insertion_sort(collection)
    # With <=, when inserting b (val=1) with mid pointing to a (val=1), 1 <= 1 is True, so high = mid - 1 = -1, inserting b before a, making b.index < a.index in result or altering stability.
    assert res[0].index == 0
    assert res[1].index == 1