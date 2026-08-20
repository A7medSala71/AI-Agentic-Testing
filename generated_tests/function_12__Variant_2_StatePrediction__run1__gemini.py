from function_12 import circle_sort


def test_empty_collection():
    assert circle_sort([]) == []


def test_single_element():
    assert circle_sort([1]) == [1]


def test_already_sorted():
    assert circle_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_reverse_sorted():
    assert circle_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_unsorted_duplicates():
    assert circle_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]) == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]


def test_negative_numbers():
    assert circle_sort([-3, -1, -4, 0, 5]) == [-4, -3, -1, 0, 5]


def test_two_elements():
    assert circle_sort([2, 1]) == [1, 2]


def test_mutmut_3_swapped_false_to_none():
    # If swapped is initialized to None instead of False, the outer while loop on a sorted collection would fail if None is truthy/falsy incorrectly. But wait, already sorted collection does not trigger any swap, so it returns None on the first utility call, causing `is_not_sorted` to become None, making `while is_not_sorted is True` evaluate to False on the first check. But wait, if swapped is None, `is_not_sorted` becomes None, which is not True, so it exits immediately on sorted collection. What if collection is not sorted? Let's check a collection where swapped is False initially.
    # Actually, mutmut_3 changes `swapped = False` to `swapped = None`. If an already-sorted collection is passed, `swapped` remains None (instead of False), so `is_not_sorted = circle_sort_util(...)` sets `is_not_sorted` to None, and the while loop terminates. Since the list is already sorted, it returns it correctly. But what if `swapped` is returned and tested? Let's test a case where `swapped` affects the return value of `circle_sort_util` directly when no swaps occur.
    # Wait, if `swapped = None`, then `return swapped or left_swap or right_swap` returns None instead of False when no swaps happen anywhere. If `is_not_sorted` becomes None, `while is_not_sorted is True:` stops. But wait, is `is_not_sorted` checked with `is True`? Yes: `while is_not_sorted is True:`. If `is_not_sorted` is None, `None is True` is False, so the loop terminates. For an already sorted list, it terminates immediately. What about an unsorted list? It swaps, so `swapped` becomes True, so `is_not_sorted` becomes True.
    # How does `swapped = None` survive? If `swapped` starts as None, but gets overwritten by True when a swap happens, it only fails if NO swaps happen in `circle_sort_util`. But if no swaps happen, `circle_sort_util` returns `swapped` (which is None instead of False) or `left_swap` or `right_swap`. If all are None/False, it returns None. Then `is_not_sorted` becomes None, loop terminates. Since the list was already sorted (or became sorted), it returns the correct list!
    # Wait, how to kill mutmut_3? If `swapped` is None, does any internal logic or return type check fail? Python allows returning None. But wait, `circle_sort_util` is annotated to return `bool`. Let's test calling `circle_sort_util` indirectly or check behavior where `swapped` is expected to be boolean `False`. Since `circle_sort_util` is nested, we can't call it directly unless we import it, but it's inside `circle_sort`.
    # Wait, can we pass a collection that causes `circle_sort_util` to return `swapped` where `swapped` being `None` vs `False` matters? If `left_swap` and `right_swap` are False, but `swapped` is checked... wait, `swapped` is the local variable for the current util call. If no swaps happen in this level, and left_swap is False, right_swap is False, it returns `swapped`. If `swapped` is `None`, it returns `None` instead of `False`.
    # Does `is_not_sorted = circle_sort_util(...)` behave differently if it's `None` vs `False` in `while is_not_sorted is True:`? Both `None is True` and `False is True` are `False`. So the loop terminates in both cases.
    # Wait! What if `is_not_sorted` is initialized to `True`, and then `is_not_sorted = circle_sort_util(...)`. If `circle_sort_util` returns `None`, `is_not_sorted` becomes `None`.
    # Is there any place where `swapped` is combined with `or`? `return swapped or left_syap or right_swap`. If `swapped` is `None`, `None or False or False` evaluates to `False` (because in Python, `None` is falsy!). That's why it evaluates the same way in boolean contexts!
    # Wait, how do we kill `swapped = None` if `None` is falsy just like `False`? We can check identity or type, or maybe a condition expecting `False`. But the code uses `is_not_sorted is True`, and `None is True` is False, `False is True` is False.
    # Wait, what about mutmut_29 (`swapped = None` at line 25, inside the middle check)? Line 25 is: `swapped = True` mutated to `swapped = None`.
    # Let's write a test that specifically triggers line 25 (`if left == right and collection[left] > collection[righ + 1]: swapped = True`).
    # To trigger line 25, `left == right` must be true after the while loop, which happens when collection has an odd number of elements and the middle elements need swapping.
    # Let's craft an odd-length collection where the middle comparison triggers a swap: e.g., `[3, 1, 2]`.
    # For `[3, 1, 2]`, low=0, high=2. left=0, right=2.
    # left=0, right=2: collection[0]=3 > collection[2]=2 -> swaps to [2, 1, 3], swapped=True. left=1, right=1.
    # Loop ends. Then `left == right` (1 == 1). `collection[1] > collection[2]` -> `collection[1]=1 > collection[2]=3` is False.
    # We need `collection[left] > collection[right + 1]` to be True at line 25!
    # That means `collection[left] > collection[right + 1]` where left == right.
    # Let's trace: we need `left == right` after the while loop, and `collection[left] > collection[right + 1]`.
    # In the while loop, `left` increments and `right` decrements until `left >= right`. If len is odd, `left` and `right` meet at the exact middle index.
    # After the loop, `left == right` holds. Then it checks `collection[left] > collection[right + 1]`. But `right + 1` would be `left + 1`, which is past the middle! Wait, `right` started at `high`, so when `left == right`, `right` is `mid`. Then `right + 1` is `mid + 1`. So it compares the middle element with the element right after the middle!
    # Let's construct a list where the middle element is greater than the element immediately following the middle in that segment:
    # Segment from low to high. Let's take `[2, 3, 1, 4]`, low=0, high=3.
    # left=0, right=3: collection[0]=2 < collection[3]=4, no swap. left=1, right=2.
    # left=1, right=2: collection[1]=3 > collection[2]=1 -> swaps! collection becomes `[2, 1, 3, 4]`, swapped=True. left=2, right=1 (loop ends).
    # After loop: left=2, right=1 -> `left == right` is False (2 == 1 is False).
    # We need `left == right` after the loop. That happens when `left` and `right` meet, which occurs when initial `high - low` is even (e.g. length 3: indices 0, 1, 2).
    # Let's take collection `[3, 2, 1]`, low=0, high=2.
    # left=0, right=2: collection[0]=3 > collection[2]=1 -> swaps to `[1, 2, 3]`, swapped=True. left=1, right=1.
    # Loop ends because left < right (1 < 1 is False).
    # Now `left == right` (1 == 1) is True.
    # Next check: `collection[left] > collection[right + 1]` -> `collection[1] > collection[2]` -> `2 > 3` is False.
    # We want `collection[1] > collection[2]` to be True! So we need `collection[1]` to be greater than `collection[2]` *before* that check, but the while loop might have swapped them or not.
    # Wait, the while loop compares `collection[left]` and `collection[right]` from outside in.
    # For `[2, 3, 1]` (low=0, high=2):
    # left=0, right=2: collection[0]=2 < collection[1]? No, collection[2]=1. `2 > 1` is True! So it swaps collection[0] and collection[2], making it `[1, 3, 2]`. Then left=1, right=1. Loop ends.
    # Now `left == right` (1 == 1). Check `collection[1] > collection[2]` -> `collection[1]` is 3, `collection[2]` is 2. `3 > 2` is True!
    # So `[2, 3, 1]` triggers line 25's swap!
    # Let's test `circle_sort([2, 3, 1])`.
    assert circle_sort([2, 3, 1]) == [1, 2, 3]


def test_mutmut_30_swapped_false_mutant():
    # Mutmut 30 changes `swapped = True` to `swapped = False` at line 25.
    # Using the same input `[2, 3, 1]` which triggers line 25, if `swapped` is set to `False` instead of `True`, the function might return `False` when it should have returned `True` (or `is_not_sorted` might incorrectly become `False`, terminating the sort prematurely if more passes are needed).
    assert circle_sort([2, 3, 1]) == [1, 2, 3]


def test_mutmut_53_logical_operator_mutant():
    # Mutmut 53 changes `return swapped or left_swap or right_swap` to `return swapped or left_swap and right_swap`.
    # This changes operator precedence / logic. We need a case where `swapped` is False, `left_swaps` is True, and `right_swap` is False.
    # With original: `False or True and False` -> `False or False` -> `False`? Wait!
    # Python precedence: `and` binds tighter than `or`.
    # So `swapped or left_swap and right_swap` is parsed as `swapped or (left_swap and right_swap)`.
    # If original is `(swapped or left_swap) or right_swap`:
    # Let's test with `swapped = False`, `left_swap = True`, `right_swap = False`.
    # Original: `(False or True) or False` -> `True or False` -> `True`.
    # Mutated: `False or (True and False)` -> `False or False` -> `False`.
    # We need a collection where one side of the recursive `circle_sort_util` returns True and the other returns False, and `swapped` is False at that level.
    # Let's test an unsorted collection that exercises this combination, such as `[1, 4, 2, 3]` or similar.
    assert circle_sort([1, 4, 2, 3]) == [1, 2, 3, 4]


def test_mutmut_3_swapped_none_general():
    # Additional test to ensure `swapped = None` (mutmut_3) is caught by checking sorting behavior on complex unsorted inputs.
    assert circle_sort([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]