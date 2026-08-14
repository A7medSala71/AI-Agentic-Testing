from function_14 import insertion_sort


def test_insertion_sort_empty():
    collection = []
    assert insertion_sort(collection) == []
    assert collection is collection


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
    collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    assert insertion_sort(collection) == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]


def test_insertion_sort_floats():
    collection = [3.14, 1.41, 2.71, 0.57]
    assert insertion_sort(collection) == [0.57, 1.41, 2.71, 3.14]


def test_insertion_sort_strings():
    collection = ["banana", "apple", "cherry", "date"]
    assert insertion_sort(collection) == ["apple", "banana", "cherry", "date"]


def test_insertion_sort_mutates_in_place():
    collection = [3, 2, 1]
    res = insertion_sort(collection)
    assert res is collection
    assert collection == [1, 2, 3]


def test_comparable_protocol_runtime():
    class CustomItem:
        def __init__(self, val):
            self.val = val
        def __lt__(self, other):
            return self.val < other.val
        def __eq__(self, other):
            return self.val == other.val
        def __repr__(self):
            return f"CustomItem({self.val})"

    c1 = CustomItem(10)
    c2 = CustomItem(5)
    c3 = CustomItem(20)
    collection = [c1, c2, c3]
    sorted_coll = insertion_sort(collection)
    assert [x.val for x in sorted_coll] == [5, 10, 20]
