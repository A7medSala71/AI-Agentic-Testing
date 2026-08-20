from function_15 import merge_sort


def test_merge_sort_empty():
    collection = []
    assert merge_sort(collection) == []


def test_merge_sort_single_element():
    collection = [42]
    assert merge_sort(collection) == [42]


def test_merge_sort_already_sorted():
    collection = [1, 2, 3, 4, 5]
    assert merge_sort(collection) == [1, 2, 3, 4, 5]


def test_merge_sort_reverse_sorted():
    collection = [5, 4, 3, 2, 1]
    assert merge_sort(collection) == [1, 2, 3, 4, 5]


def test_merge_sort_unsorted_with_duplicates():
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    assert merge_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_merge_sort_negative_numbers():
    collection = [-3, 5, 0, -1, 2]
    assert merge_sort(collection) == [-3, -1, 0, 2, 5]


def test_merge_sort_duplicate_elements_stability_or_order():
    # Mutant mutmut_7 changes <= to < in merge comparison, altering stability for equal elements.
    collection = [2, 2, 1]
    # left[0] (2) <= right[0] (2) should pop from left first, preserving the left-first order.
    # With <, 2 < 2 is False, so it pops right (the second 2) before left (the first 2).
    # To check specifically, let's trace with objects or distinct items that compare equal, 
    # or just ensure standard stable merge on duplicates:
    assert merge_sort([2, 2]) == [2, 2]
    # More explicitly, let's use a list with duplicate values where stable sorting order matters:
    # If left has [2_a] and right has [2_b], left[0] <= right[0] picks left[0] first.
    # With <, left[0] < right[0] is False, picking right[0] first.
    # We can test this by passing two sublists that merge where equal elements occur.
    assert merge_sort([2, 2, 1]) == [1, 2, 2]
    # Let's target duplicate sorting explicitly with a custom object or simple equal values:
    # Actually, a list like [2, 2] is already tested, but let's test a merge where left[0] == right[0]:
    # left = [2], right = [2]. left[0] <= right[0] is True -> pops left. < is False -> pops right.
    # Since they are identical integers, the final list is [2, 2] either way, UNLESS we track stability.
    # Wait, does the function maintain stability? left.pop(0) if left[0] <= right[0] means left is preferred on equality.
    # Let's test with a structure or just rely on the fact that mutation changes the comparison boundary.
    # Since they are integers, let's ensure the mutation causes a failure if it behaves differently. 
    # Wait, if left[0] == right[0], popping left preserves original relative order. If < is used, right is popped first, 
    # which in this case might invert equal elements if they came from different sides.
    # Let's test with list where left=[2, 'a'] and right=[2, 'b']? But collection items must be comparable.
    # If we pass [2, 2, 2, 2], merge sort divides into [2, 2] and [2, 2].
    # Let's assert on a specific input that exercises the `left[0] <= right[0]` branch with equal elements.
    collection = [2, 2]
    assert merge_sort(collection) == [2, 2]
    # To strictly kill the mutant where <= becomes <, when left[0] == right[0], 
    # the original code evaluates True and pops from left. The mutant evaluates False and pops from right.
    # We can verify stability by using objects that compare equal but are distinct, or since items are just ints,
    # let's check if there's any observable difference or if standard tests cover it.
    # Wait, if all elements are integers, [2, 2] sorted is [2, 2]. Is there any observable difference for pure ints?
    # If left[0] == right[0], both are equal, so whether we take left or right, the appended value is the same integer!
    # But wait! `left.pop(0)` removes from `left`, whereas `right.pop(0)` removes from `right`.
    # If left=[2] and right=[2], left[0] <= right[0] is True -> `result.append(left.pop(0))`.
    # If left[0] < right[0] is False -> `result.append(right.pop(0))`.
    # In both cases, `result` gets 2, `left` becomes empty, `right` becomes empty.
    # Wait, does it really matter for primitive ints? If mutmut generates this mutant, does any test catch it?
    # If the mutant survives, it means for all existing tests, taking left vs right on equality yielded the exact same result.
    # To kill it, we need an input where taking from left vs right produces a different result or behavior, 
    # or perhaps it's an equivalent mutant if integers are indistinguishable?
    # But wait, `left.pop(0)` vs `right.pop(0)` consumes from different lists. If one list has more elements or different subsequent elements, 
    # popping from the wrong list changes which element is next at `[0]`!
    # Let's construct a case where left[0] == right[0], but left[1] < right[1] or similar.
    # Let left = [2, 3] and right = [2, 1].
    # Original: left[0] (2) <= right[0] (2) is True -> pops left[0] (2). Result has 2. Next left is 3, right is 2.
    # Mutated (<): left[0] (2) < right[0] (2) is False -> pops right[0] (2). Result has 2. Next left is 2, right is 1.
    # Look at that! The resulting stream of pops is completely different!
    # Original: left=[2,3], right=[2,1]
    # 1. left[0] (2) <= right[0] (2) -> True -> appends 2, left becomes [3], right becomes [2,1]
    # 2. left[0] (3) <= right[0] (2) -> False -> appends 2 (from right), left becomes [3], right becomes [1]
    # 3. left[0] (3) <= right[0] (1) -> False -> appends 1 (from right), left becomes [3], right becomes []
    # 4. left non-empty -> extends [3] -> result becomes [2, 2, 1, 3] (Wait, let's trace properly: 
    #    Let's use merge([2, 3], [2, 1]) directly via merge_sort).
    # If collection = [3, 2, 1, 2] -> split into [3, 2] -> [2, 3], and [1, 2] -> [1, 2].
    # Let's test `merge_sort([3, 2, 1, 2])`:
    # Left sorted: [2, 3], Right sorted: [1, 2].
    # Let's assert the exact output for a case where left[0] == right[0]:
    assert merge_sort([2, 1, 2, 3]) == [1, 2, 2, 3]
    assert merge_sort([3, 2, 2, 1]) == [1, 2, 2, 3]