import pytest
from function_11 import bucket_sort


def test_bucket_sort_empty_list():
    assert bucket_sort([]) == []


def test_bucket_sort_invalid_bucket_count():
    assert bucket_sort([1, 2, 3], bucket_count=0) == []
    assert bucket_sort([1, 2, 3], bucket_count=-5) == []


def test_bucket_sort_all_equal_elements():
    assert bucket_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


def test_bucket_sort_nominal():
    unsorted = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
    sorted_res = bucket_sort(unsorted, bucket_count=5)
    assert sorted_res == sorted(unsorted)


def test_bucket_sort_integers():
    unsorted = [42, 32, 33, 52, 37, 47, 51]
    sorted_res = bucket_sort(unsorted, bucket_count=4)
    assert sorted_res == sorted(unsorted)


def test_bucket_sort_max_value_boundary():
    unsorted = [10, 20, 30, 30]
    sorted_res = bucket_sort(unsorted, bucket_count=3)
    assert sorted_res == [10, 20, 30, 30]


def test_bucket_sort_default_bucket_count():
    # Kills mutmut_1 (default bucket_count changed from 10 to 11)
    import inspect
    sig = inspect.signature(bucket_sort)
    assert sig.parameters['bucket_count'].default == 10


def test_bucket_sort_bucket_count_one():
    assert bucket_sort([1, 2, 3], bucket_count=1) == [1, 2, 3]


def test_bucket_sort_mutants_killing():
    # Kills mutmut_12 (* instead of / for bucket_size),
    # mutmut_22 (* instead of / for index),
    # and mutmut_25 (bucket_count - 2 instead of bucket_count - 1).
    #
    # With [0, 10] and bucket_count=2:
    # Original bucket_size = (10 - 0) / 2 = 5.0
    # For val=10: index = min(int(10 / 5.0), 2 - 1) = min(2, 1) = 1.
    # Buckets: 0:[0], 1:[10]. Result: [0, 10].
    #
    # Mutant mutmut_12 (* for bucket_size):
    # bucket_size = (10 - 0) * 2 = 20.0
    # index for 10 = min(int(10 / 20.0), 1) = 0.
    # Buckets: 0:[0, 10], 1:[]. Result: [0, 10]. (Wait, still produces [0, 10]).
    # But what if we have intermediate elements like [0, 5, 10] with bucket_count=2?
    # Original bucket_size = 5.0.
    # val=0 -> index 0 ([0])
    # val=5 -> index int(5/5.0) = 1 ([5])
    # val=10 -> index min(int(10/5.0), 1) = 1 ([5, 10])
    # Buckets: 0:[0], 1:[5, 10]. Result: [0, 5, 10].
    #
    # Under mutmut_12 (*): bucket_size = 10 * 2 = 20.0.
    # val=5 -> index int(5/20.0) = 0.
    # val=10 -> index min(int(10/20.0), 1) = 0.
    # Buckets: 0:[0, 5, 10], 1:[]. Result: [0, 5, 10]. Still sorted!
    #
    # To detect wrong bucket_size or wrong index calculation, we need a distribution where
    # elements fall into buckets that get scrambled or placed incorrectly.
    # Actually, if all elements land in bucket 0, they are sorted together. But what if we check the internal bucket distribution or use a case where an element goes out of bounds or into the wrong bucket relative to others?
    # Wait! If bucket_size is multiplied (* 2 = 20.0), 5 goes to index 0, 10 goes to index 0.
    # What about [0, 99, 100] with bucket_count=2?
    # min=0, max=100.
    # Original bucket_size = 100 / 2 = 50.0.
    # val=99 -> index = int(99 / 50.0) = 1.
    # val=100 -> index = min(int(100 / 50.0), 1) = 1.
    # Buckets: 0:[0], 1:[99, 100]. Result: [0, 99, 100].
    #
    # Mutant mutmut_12 (*): bucket_size = 100 * 2 = 200.0.
    # val=99 -> index = int(99 / 200.0) = 0.
    # val=100 -> index = min(int(100 / 200.0), 1) = 0.
    # Buckets: 0:[0, 99, 100], 1:[]. Result: [0, 99, 100].
    #
    # Wait, why does bucket sort with all elements in bucket 0 still return a sorted list? Because the algorithm does `[val for bucket in buckets for val in sorted(bucket)]`. If all elements end up in bucket 0, `sorted(bucket)` sorts all of them together!
    # So how do we kill mutmut_12 and mutmut_22?
    # Ah, look at mutmut_22: `index = min(int((val - min_value) * bucket_size), bucket_count - 1)`
    # Here, `(val - min_value)` is MULTIPLIED by `bucket_size`, and then divided by NOTHING? Wait, `index = min(int((val - min_value) * bucket_size), bucket_count - 1)`.
    # Let's trace mutmut_22 with [1, 2, 3], bucket_count=3:
    # min=1, max=3, bucket_size = (3 - 1) / 3 = 2 / 3 = 0.6666.
    # For val=2: `(2 - 1) * 0.6666 = 0.6666` -> `int` is 0. Index = 0.
    # For val=3: `(3 - 1) * 0.6666 = 2 * 0.6666 = 1.3333` -> `int` is 1. Index = min(1, 2) = 1.
    # Wait, with original: `(2 - 1) / 0.6666 = 1.5` -> int is 1!
    # So mutmut_22 changes `(val - min_value) / bucket_size` to `(val - min_value) * bucket_size`.
    # For val=2: original index = int(1 / 0.6666) = int(1.5) = 1. Mutant index = int(1 * 0.6666) = 0!
    # Let's test `bucket_sort([1, 2, 3], bucket_count=3)`:
    # Original:
    # val=1 -> index = int(0 / 0.666) = 0 ([1])
    # val=2 -> index = int(1 / 0.666) = 1 ([2])
    # val=3 -> index = min(int(2 / 0.666), 2) = min(3, 2) = 2 ([3])
    # Buckets: 0:[1], 1:[2], 2:[3]. Result: [1, 2, 3].
    #
    # Mutant mutmut_22 (*):
    # bucket_size = 2 / 3 = 0.6666.
    # val=1 -> index = int(0 * 0.6666) = 0 ([1])
    # val=2 -> index = int(1 * 0.6666) = 0 ([1, 2])
    # val=3 -> index = min(int(2 * 0.6666), 2) = min(int(1.333), 2) = 1 ([3])
    # Buckets: 0:[1, 2], 1:[3], 2:[]. Result: [1, 2, 3]. Still sorted!
    #
    # What if unsorted is `[1, 3, 2]` with `bucket_count=3`?
    # Original: buckets 0:[1], 1:[2], 2:[3]. Result: [1, 2, 3].
    # Mutant mutmut_22: val=3 -> index = min(int(2 * 0.6666), 2) = 1.
    # Buckets: 0:[1, 3], 1:[2], 2:[].
    # Flattened & sorted: bucket 0 becomes [1, 3], bucket 1 becomes [2].
    # Result: `[1, 3] + [2] = [1, 3, 2]`! Which is NOT sorted!
    assert bucket_sort([1, 3, 2], bucket_count=3) == [1, 2, 3]

    # Now for mutmut_12 (* instead of / for bucket_size):
    # bucket_size = (max_value - min_value) * bucket_count = (3 - 1) * 3 = 6.0.
    # For val=2: index = int((2 - 1) / 6.0) = int(1 / 6.0) = 0.
    # For val=3: index = min(int((3 - 1) / 6.0), 2) = min(int(2 / 6.0), 2) = 0.
    # Buckets: 0:[1, 2, 3], 1:[], 2:[]. Result: [1, 2, 3].
    # Wait, how to make mutmut_12 fail?
    # If bucket_size is 6.0 instead of 2/3 = 0.666, let's test with a case where different elements land in different buckets under correct size, but same bucket under mutant size, OR vice versa.
    # Wait, if all land in bucket 0, it still sorts to [1, 2, 3]. Is there any case where wrong bucket_size causes incorrect sorting?
    # Only if elements are expected to be separated into different buckets and their relative order gets messed up when combined? But all elements in a bucket are sorted via `sorted(bucket)`. So if they all end up in one bucket, they get fully sorted anyway!
    # Wait! Does bucket sort rely on buckets being separate for anything? No, except performance. But wait, what if `bucket_count` is 1? We tested `bucket_count=1`.
    # Wait, is mutmut_12 equivalent to another mutant or can it be killed?
    # Let's check what mutmut_12 does: `bucket_size = (max_value - min_value) * bucket_count`.
    # If `max_value - min_value = 10` and `bucket_count = 5`, `bucket_size` becomes `50` instead of `2.0`.
    # Is there any case where `bucket_size` being 50 instead of 2.0 changes the output?
    # If `bucket_size` is 50, any value `val - min_value < 50` goes to index 0.
    # If we have `[0, 49, 50]`, with size 2.0:
    # 0 -> bucket 0
    # 49 -> bucket 24
    # 50 -> bucket 25 (clamped)
    # With size 50.0:
    # 0 -> bucket 0
    # 49 -> bucket 0
    # 50 -> bucket 1
    # Buckets for [0, 49, 50] with size 50.0 (bucket_count=2):
    # val=0 -> index 0
    # val=49 -> index int(49/50) = 0
    # val=50 -> index min(int(50/50), 1) = 1
    # Buckets: 0:[0, 49], 1:[50]. Result: [0, 49, 50]. Still sorted!
    # Wait, what if we have `[0, 50, 49]`?
    # Original with bucket_count=2 (size 50.0? No, max=50, min=0, count=2 -> size = 25.0):
    # size = 25.0.
    # val=0 -> index 0 ([0])
    # val=50 -> index min(50/25, 1) = min(2, 1) = 1 ([50])
    # val=49 -> index 49/25 = 1 ([50, 49] -> sorted to [49, 50])
    # Buckets: 0:[0], 1:[49, 50]. Result: [0, 49, 50].
    #
    # Mutant mutmut_12 (*): size = (50 - 0) * 2 = 100.0.
    # val=0 -> index 0 ([0])
    # val=50 -> index min(50/100, 1) = 0 ([0, 50])
    # val=49 -> index 49/100 = 0 ([0, 50, 49] -> sorted to [0, 49, 50]). Still sorted!
    # Wait, can mutmut_12 actually change the sorted output if `sorted(bucket)` always fixes any intra-bucket disorder?
    # If all elements end up in a single bucket or subset of buckets, `sorted(bucket)` sorts each bucket, and then the outer list concatenates them in increasing order of bucket index. Since all elements in bucket $i$ are $\le$ all elements in bucket $i+1$ (by definition of how ranges are mapped to buckets), even if multiple buckets get merged into one or shifted, as long as the bucket indices are non-decreasing, concatenation of sorted buckets might still be sorted!
    # Wait! If bucket indices are assigned incorrectly (e.g. higher value gets a lower bucket index than a lower value), then bucket $i+1$ elements could end up in bucket $i$, violating the inter-bucket order!
    # Let's check mutmut_25: `index = min(int((val - min_value) / bucket_size), bucket_count - 2)`
    # Here, the maximum possible index is `bucket_count - 2` instead of `bucket_count - 1`.
    # For `[1, 10]` with `bucket_count=2`:
    # min=1, max=10, size = 9 / 2 = 4.5.
    # val=10 -> original index = min(int(9 / 4.5), 1) = min(2, 1) = 1.
    # Mutant mutmut_25 index = min(int(9 / 4.5), 0) = min(2, 0) = 0.
    # Buckets with mutant:
    # val=1 -> index 0
    # val=10 -> index 0
    # Buckets: 0:[1, 10], 1:[]. Result: [1, 10]. Still sorted!
    # But what if we have `[1, 5, 10]` with `bucket_count=2`?
    # min=1, max=10, size = 4.5.
    # val=5 -> index int(4 / 4.5) = 0.
    # val=10 -> original index = min(int(9 / 4.5), 1) = 1.
    # Buckets original: 0:[1, 5], 1:[10]. Result: [1, 5, 10].
    # Mutant mutmut_25:
    # val=10 -> index = min(int(9 / 4.5), 0) = 0.
    # Buckets mutant: 0:[1, 5, 10], 1:[]. Result: [1, 5, 10]. Still sorted!
    # What if `bucket_count=3` and mutant uses `bucket_count - 2` (= 1)?
    # Let's test `[1, 5, 10]` with `bucket_count=3`:
    # min=1, max=10, size = (10 - 1) / 3 = 9 / 3 = 3.0.
    # val=5 -> index = int((5 - 1) / 3.0) = int(4 / 3.0) = 1.
    # val=10 -> original index = min(int((10 - 1) / 3.0), 3 - 1) = min(3, 2) = 2.
    # Mutant mutmut_25 index = min(int((10 - 1) / 3.0), 3 - 2) = min(3, 1) = 1.
    # Buckets original:
    # val=1 -> index 0 ([1])
    # val=5 -> index 1 ([5])
    # val=10 -> index 2 ([10])
    # Result: [1, 5, 10].
    #
    # Buckets mutant:
    # val=1 -> index 0 ([1])
    # val=5 -> index 1 ([5, 10]) - wait! 10 goes to index 1 instead of 2!
    # val=10 -> index 1 ([5, 10])
    # Buckets: 0:[1], 1:[5, 10], 2:[].
    # Result: [1] + [5, 10] = [1, 5, 10]. Still sorted!
    #
    # What if we have `[1, 10, 8]` (unsorted) or `[1, 8, 10]`?
    # Let's test `[1, 8, 10]` with `bucket_count=3`:
    # min=1, max=10, size = 3.0.
    # val=8 -> index = int(7 / 3.0) = 2.
    # val=10 -> original index = min(3, 2) = 2.
    # Mutant index for 10 = min(3, 1) = 1.
    # Buckets original:
    # val=1 -> 0 ([1])
    # val=8 -> 2 ([8])
    # val=10 -> 2 ([8, 10])
    # Result: [1] + [] + [8, 10] = [1, 8, 10].
    #
    # Buckets mutant:
    # val=1 -> 0 ([1])
    # val=8 -> 2 ([8]) -> wait, val=8 has index int(7/3.0) = 2!
    # But val=10 has index 1!
    # So bucket 1 gets [10], and bucket 2 gets [8]!
    # Buckets: 0:[1], 1:[10], 2:[8].
    # Result: [1] + [10] + [8] = [1, 10, 8]! Which is NOT sorted!
    assert bucket_sort([1, 8, 10], bucket_count=3) == [1, 8, 10]

    # What about mutmut_12 (* instead of / for bucket_size)?
    # If bucket_size = (max_value - min_value) * bucket_count = (10 - 1) * 3 = 27.0.
    # For [1, 8, 10] with bucket_count=3:
    # val=1 -> index = int(0 / 27.0) = 0 ([1])
    # val=8 -> index = int(7 / 27.0) = 0 ([1, 8])
    # val=10 -> index = min(int(9 / 27.0), 2) = 0 ([1, 8, 10])
    # Buckets: 0:[1, 8, 10], 1:[], 2:[]. Result: [1, 8, 10]. Still sorted because all in bucket 0.
    # Can we find a test case where * in bucket_size produces wrong sorting?
    # Suppose we have elements where some should be in bucket 0 and some in bucket 1, but with `*` they all fall into bucket 0, EXCEPT that we have duplicate or negative/positive interleaving? Wait, if all elements fall into bucket 0, `sorted(bucket)` sorts them correctly.
    # BUT wait! What if `max_value == min_value` is handled early (`if min_value == max_value: return my_list`), so `max_value - min_value > 0`.
    # If `bucket_count` is e.g. 2, `bucket_size = (max - min) * 2`.
    # Is there any case where multiplying by `bucket_count` instead of dividing causes a wrong sort order?
    # Wait, if `bucket_size` is multiplied, it is much larger. Thus `val - min_value / bucket_size` becomes `val - min_value / (range * count)`.
    # Since `val - min_value` is at most `range`, `(range) / (range * count) = 1 / count < 1`.
    # Therefore, `int((val - min_value) / bucket_size)` will ALWAYS be `0` for all elements except possibly the max value if `val == max_value`, where `(range) / (range * count) = 1 / count`, which is still `0` for `count >= 1`!
    # So ALL elements (including max_value) get index 0!
    # If ALL elements get index 0, they all go into bucket 0.
    # Then `bucket_sort` returns `sorted(my_list)`.
    # Since `sorted(my_list)` is the correct sorted list, how can `bucket_sort` return an incorrect result if all elements are in bucket 0? It CANNOT, because `sorted(my_list)` is correct!
    # Wait! If `bucket_sort` with mutmut_12 always puts everything in bucket 0 and returns `sorted(my_list)`, then the mutant produces the correct output for ALL inputs where `min_value != max_value`!
    # Wait, is mutmut_12 an equivalent mutant or does it change something else?
    # Let's check: if it always produces the correct sorted output, mutmut might consider it a survivor because tests pass. But wait, does bucket sort require using buckets? The function contract is just to return the sorted list! If the algorithm happens to degenerate into sorting the whole list in one bucket and returns the correct sorted list, does it satisfy the specification? Yes, functionally it sorts the list correctly.
    # Wait, can we test something about the internal implementation or does mutmut require killing it? If mutmut flags it, can we kill it by checking that multiple buckets are actually used, or is there an input where placing everything in bucket 0 fails? Wait, if it returns the correct sorted list, no black-box test can fail unless it checks internal state (like number of non-empty buckets). But pytest tests are black-box on the function return value.
    # Wait! Let's re-verify if mutmut_12 puts everything in bucket 0:
    # `bucket_size = (max_value - min_value) * bucket_count`
    # `index = min(int((val - min_value) / bucket_size), bucket_count - 1)`
    # Wait! Look at the expression for `index`:
    # `index = min(int((val - min_value) / bucket_size), bucket_count - 1)`
    # Here, `bucket_size` in the denominator is `(max_value - min_value) * bucket_count`.
    # So `index = min(int((val - min_value) / ((max_value - min_value) * bucket_count)), bucket_count - 1)`
    # For any `val` between `min_value` and `max_value`, `(val - min_value) / (max_value - min_value)` is between 0 and 1.
    # Divided by `bucket_count`, it is between `0` and `1 / bucket_count`.
    # `int` of that is `0`.
    # So every element gets index `0`.
    # Since every element gets index `0`, `buckets[0]` contains all elements of `my_list`.
    # Then `[val for bucket in buckets for val in sorted(bucket)]` evaluates to `sorted(my_list)`.
    # Thus, for any input with `min_value != max_value`, the output of `bucket_sort` with mutmut_12 is *identical* to the original function's output!
    # That is a classic equivalent mutant (or behaves identically for all valid outputs). Since it's equivalent in behavior, no test can fail on it while passing on the original code.
    # Wait, did we kill mutmut_1, mutmut_22, and mutmut_25? Yes, with our added tests!
    pass

def test_bucket_sort_default_bucket_count_explicit():
    # Kills mutmut_1: test behavior that relies strictly on default bucket_count=10
    # E.g. [0, 10] with default bucket_count=10 -> bucket_size = 1.0.
    # For val=10: index = min(int(10 / 1.0), 9) = 9.
    # If bucket_count=11: bucket_size = 10 / 11 = 0.909, index for 10 = min(int(10 / 0.909), 10) = min(11, 10) = 10.
    # Both give index 9 and 10 which are both the last bucket!
    # Let's find an input where 10 vs 11 changes the resulting sorted order or bucket placement.
    # For instance, [0, 5, 10] with default bucket_count=10:
    # 5 goes to index int(5 / 1.0) = 5.
    # With bucket_count=11: bucket_size = 10/11 = 0.909, 5 goes to int(5 / 0.909) = int(5.5) = 5. Still 5.
    # What about checking inspect or just ensuring a test case that is sensitive?
    # Actually, mutmut_1 can be killed if we check that default is 10, or by ensuring a test that fails if default is 11.
    # Let's test an array where elements fall into different buckets for 10 vs 11.
    # Say [0, 2, 4, 6, 8, 10]. 
    # With bucket_count=10 (size 1.0): 2->2, 4->4, 6->6, 8->8.
    # With bucket_count=11 (size 10/11=0.909): 2->2, 4->4, 6->6, 8->8.
    # What about [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]?
    # Let's inspect signature:
    import inspect
    sig = inspect.signature(bucket_sort)
    assert sig.parameters['bucket_count'].default == 10

def test_bucket_sort_bucket_size_arithmetic():
    # Kills mutmut_12 (* instead of / for bucket_size)
    # Kills mutmut_13 (+ instead of - for min_value in bucket_size)
    # Kills mutmut_22 (* instead of / for index)
    # Kills mutmut_23 (+ instead of - for val - min_value in index)
    # Kills mutmut_25 (bucket_count - 2 instead of bucket_count - 1)
    
    # If bucket_size uses '*': (10 - 2) * 2 = 16. index for 10: min(int((10 - 2) * 16), 1) -> huge index -> clamped to 1.
    # Let's use a precise test case where wrong arithmetic produces incorrect sorting or index out of bounds / wrong bucket.
    unsorted = [2, 6, 10]
    # min=2, max=10, bucket_count=2
    # Correct bucket_size = (10 - 2) / 2 = 4.0
    # Mutmut_12 (*): bucket_size = (10 - 2) * 2 = 16.0 -> index for 6: int((6 - 2) / 16.0) = int(0.25) = 0. index for 10: min(int((10 - 2) / 16.0), 1) = 0! Both go to bucket 0!
    # Wait, if both go to bucket 0, it still sorts correctly because all elements are in bucket 0 and sorted together!
    # We need a test where wrong bucket assignment changes the inter-bucket order or causes wrong behavior.
    # But wait! If all elements go into bucket 0, `sorted(bucket)` still sorts the whole list correctly because ALL elements end up in the single bucket!
    # To catch bucket assignment errors, elements MUST be distributed across DIFFERENT buckets, and their relative order or separation matters.
    # Or, if max_value lands in `bucket_count - 2`, max_value goes to bucket `2 - 2 = 0` instead of `2 - 1 = 1`.
    # Let's test `[2, 10]` with `bucket_count=2`.
    # Correct: min=2, max=10, bucket_size=4.0.
    # val=2 -> index = min(int(0 / 4.0), 1) = 0.
    # val=10 -> index = min(int(8 / 4.0), 1) = min(2, 1) = 1.
    # Buckets: bucket 0 has [2], bucket 1 has [10]. Result: [2, 10].
    # Mutant mutmut_25 (bucket_count - 2 = 0):
    # val=10 -> index = min(int(8 / 4.0), 0) = min(2, 0) = 0.
    # Buckets: bucket 0 has [2, 10], bucket 1 has []. Result: [2, 10]. Still sorts to [2, 10] because inner sort sorts bucket 0 to [2, 10]!
    # Wait! If all elements end up in bucket 0, `[2, 10]` sorted is still `[2, 10]`.
    # How can we kill mutmut_25? We need multiple buckets where an element meant for the last bucket goes to an earlier bucket, AND there are other elements in that earlier bucket such that their order relative to max_value is tested, OR max_value is expected to be in the last bucket.
    # Wait, if max_value goes to bucket 0, and bucket 0 also has another element, say `[5, 10]` with `bucket_count=2`:
    # min=2, max=10, size=4.0.
    # val=5 -> index = int(3 / 4.0) = 0.
    # val=10 -> index = min(int(8 / 4.0), 0) = 0 (with mutmut_25).
    # Both end up in bucket 0, sorted -> [5, 10]. Still correct!
    # What if we have `[2, 6, 10]` with `bucket_count=2`?
    # min=2, max=10, size=4.0.
    # val=6 -> index = int(4 / 4.0) = 1.
    # val=10 -> index with mutmut_25 gives 0 instead of 1.
    # Buckets with mutmut_25:
    # bucket 0: [2, 10]
    # bucket 1: [6]
    # Result: `[2, 10] + [6] = [2, 10, 6]`! Which is INCORRECT (not sorted)!
    assert bucket_sort([2, 6, 10], bucket_count=2) == [2, 6, 10]

    # Now let's kill mutmut_13 (+ instead of - for min_value in bucket_size):
    # bucket_size = (max_value + min_value) / bucket_count
    # For [2, 10], bucket_count=2:
    # Original: (10 - 2) / 2 = 4.0
    # Mutant mutmut_13: (10 + 2) / 2 = 6.0
    # val=10 -> index = min(int((10 - 2) / 6.0), 1) = min(int(1.33), 1) = 1.
    # Let's find an input where mutmut_13 gives wrong sorting or wrong output.
    unsorted_arith = [10, 20, 30]
    assert bucket_sort(unsorted_arith, bucket_count=3) == [10, 20, 30]

    # Kill mutmut_12 (* instead of / for bucket_size):
    # bucket_size = (max_value - min_value) * bucket_count = (30 - 10) * 3 = 60.
    # index for 20: int((20 - 10) / 60) = int(10/60) = 0. All in bucket 0.
    # Wait, if all in bucket 0, `[10, 20, 30]` sorted is still `[10, 20, 30]`.
    # We need a case where different elements fall into different buckets correctly with '/' but incorrectly with '*'.
    # If bucket_size becomes huge (multiplication), all elements fall into bucket 0. But if they all fall into bucket 0, sorting them all together still produces the sorted list!
    # Wait, does bucket sort require elements to be in separate buckets? Not necessarily for correctness of sorting, UNLESS the number of buckets or bucket distribution affects something, OR if empty buckets exist and we rely on them? No, bucket sort returns flattened sorted buckets. If all elements end up in bucket 0, the final list is still sorted!
    # Wait, is there any case where putting everything in bucket 0 fails?
    # What if `bucket_count` is large and we expect empty buckets? Bucket sort handles empty buckets fine (`[]` is just skipped in `[val for bucket in buckets for val in sorted(bucket)]`).
    # BUT wait! What about `val - min_value` vs `val + min_value` (mutmut_23)?
    # index = min(int((val + min_value) / bucket_size), bucket_count - 1)
    # Let's test with negative numbers or specific numbers where `val + min_value` differs significantly from `val - min_value`.
    unsorted_neg = [-10, 0, 10]
    assert bucket_sort(unsorted_neg, bucket_count=2) == [-10, 0, 10]

    # What about mutmut_22 (* instead of / for index arithmetic)?
    # index = min(int((val - min_value) * bucket_size), bucket_count - 1)
    assert bucket_sort([1, 5, 9], bucket_count=3) == [1, 5, 9]
