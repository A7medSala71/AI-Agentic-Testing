from function_16 import odd_even_sort


def test_odd_even_sort_nominal():
    arr = [4, 3, 2, 1, 5]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]
    assert arr == [1, 2, 3, 4, 5]


def test_odd_even_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_empty():
    arr = []
    res = odd_even_sort(arr)
    assert res == []


def test_odd_even_sort_single_element():
    arr = [42]
    res = odd_even_sort(arr)
    assert res == [42]


def test_odd_even_sort_duplicates():
    arr = [3, 1, 2, 3, 1]
    res = odd_even_sort(arr)
    assert res == [1, 1, 2, 3, 3]


def test_odd_even_sort_requires_multiple_passes_even_and_odd():
    # Needs a permutation that specifically requires swaps in both the even-indexed pass 
    # and the odd-indexed pass to ensure `is_sorted` is correctly reset to False and 
    # that the loop step/range boundaries are fully exercised.
    arr = [2, 3, 4, 1]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4]


def test_odd_even_sort_needs_odd_pass_swap():
    # An array where the even phase does nothing or leaves things unsorted, 
    # forcing the odd phase to make a swap and set is_sorted = False.
    # [1, 3, 2] -> even phase compares indices (0,1) -> 1, 3 (ok).
    # odd phase compares indices (1,2) -> 3, 2 (swap to 2, 3).
    # If is_sorted was mutated to True or None incorrectly during the loop, 
    # it might exit early or fail to loop properly.
    arr = [1, 3, 2]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3]


def test_odd_even_sort_step_size_check():
    # To kill mutants changing `range(..., 2)` to missing step (default 1),
    # an array of length >= 4 with inversions at step 1 instead of step 2 will behave incorrectly.
    # e.g. [1, 4, 3, 2]
    # range(0, len-1, 2) checks indices 0 and 2.
    # index 0: (1, 4) ok
    # index 2: (3, 2) swap -> [1, 4, 2, 3]
    # If step was 1, it would check every adjacent pair in the first pass.
    # Specifically, we can use a sequence that needs multiple distinct iterations.
    arr = [4, 1, 2, 3]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4]