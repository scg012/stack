import pytest
from fifth import InsufficientStackItemsError


class TestPush:
    def test_without_arg(self, fifth_is_empty):
        with pytest.raises(TypeError) as exc_info:
            fifth_is_empty.push()
        assert exc_info.type is TypeError
        assert exc_info.value.args[0] == "Fifth.push() missing 1 required positional argument: 'number'"

        with pytest.raises(TypeError, match=r".*missing 1 required positional argument"):
            fifth_is_empty.push()

    def test_on_empty(self, fifth_is_empty):
        fifth_is_empty.push(2)
        assert str(fifth_is_empty) == str([2])

    def test_on_non_empty(self, fifth_has_one_item):
        fifth_has_one_item.push(2)
        assert str(fifth_has_one_item) == str([1, 2])

    def test_twice(self, fifth_is_empty):
        fifth_is_empty.push(1)
        assert str(fifth_is_empty) == str([1])
        fifth_is_empty.push(2)
        assert str(fifth_is_empty) == str([1, 2])


class TestReversePush:
    def test_none_on_empty(self, fifth_is_empty):
        with pytest.raises(TypeError):
            fifth_is_empty.reverse_push(None)
        assert str(fifth_is_empty) == str([])

    def test_on_empty(self, fifth_is_empty):
        fifth_is_empty.reverse_push(2)
        assert str(fifth_is_empty) == str([2])

    def test_on_non_empty(self, fifth_has_one_item):
        fifth_has_one_item.reverse_push(2)
        assert str(fifth_has_one_item) == str([2, 1])

    def test_twice(self, fifth_is_empty):
        fifth_is_empty.reverse_push(1)
        assert str(fifth_is_empty) == str([1])
        fifth_is_empty.reverse_push(2)
        assert str(fifth_is_empty) == str([2, 1])



class TestPop:
    def test_on_empty_stack(self, fifth_is_empty):
        with pytest.raises(InsufficientStackItemsError):
            fifth_is_empty.pop()

    def test_on_single_item_stack(self, fifth_has_one_item):
        fifth_has_one_item.pop()
        assert str(fifth_has_one_item) == str([])

    def test_on_double_item_stack(self, fifth_has_two_items):
        fifth_has_two_items.pop()
        assert str(fifth_has_two_items) == str([1])
        fifth_has_two_items.pop()
        assert str(fifth_has_two_items) == str([])


class TestDup:
    def test_on_empty_stack(self, fifth_is_empty):
        with pytest.raises(InsufficientStackItemsError):
            fifth_is_empty.dup()

    def test_on_single_item_stack(self, fifth_has_one_item):
        fifth_has_one_item.dup()
        assert str(fifth_has_one_item) == str([1, 1])

    def test_on_double_item_stack(self, fifth_has_two_items):
        fifth_has_two_items.dup()
        assert str(fifth_has_two_items) == str([1, 2, 2])


class TestSwap:
    def test_on_empty_stack(self, fifth_is_empty):
        with pytest.raises(InsufficientStackItemsError):
            fifth_is_empty.swap()

    def test_on_single_item_stack(self, fifth_has_one_item):
        with pytest.raises(InsufficientStackItemsError):
            fifth_has_one_item.swap()

    def test_on_double_item_stack(self, fifth_has_two_items):
        fifth_has_two_items.swap()
        assert str(fifth_has_two_items) == str([2, 1])
        fifth_has_two_items.swap()
        assert str(fifth_has_two_items) == str([1, 2])
