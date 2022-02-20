import pytest

from fifth import Fifth
from stack import Stack


@pytest.fixture
def fifth_is_empty():
    yield Fifth()


@pytest.fixture
def fifth_has_one_item():
    fifth = Fifth(data=[1])
    assert str(fifth) == str([1])
    yield fifth


@pytest.fixture
def fifth_has_two_items():
    fifth = Fifth([1, 2])
    assert str(fifth) == str([1, 2])
    yield fifth


@pytest.fixture
def empty_stack():
    yield Stack()


@pytest.fixture()
def single_item_stack(empty_stack):
    empty_stack.fifth._stack.extend([1])
    assert str(empty_stack) == str([1])
    yield empty_stack


@pytest.fixture
def double_item_stack(empty_stack):
    empty_stack.fifth._stack.extend([1, 2])
    assert str(empty_stack) == str([1, 2])
    yield empty_stack


@pytest.fixture
def double_item_stack_push_0_push_2(empty_stack):
    empty_stack.fifth._stack.extend([0, 2])
    assert str(empty_stack) == str([0, 2])
    yield empty_stack


@pytest.fixture
def double_item_stack_push_2_push_0(empty_stack):
    empty_stack.fifth._stack.extend([2, 0])
    assert str(empty_stack) == str([2, 0])
    yield empty_stack


@pytest.fixture
def double_item_stack_push_2_push_5(empty_stack):
    empty_stack.fifth._stack.extend([2, 5])
    assert str(empty_stack) == str([2, 5])
    yield empty_stack


@pytest.fixture
def double_item_stack_two_non_zero_integers_first_operand_is_larger(empty_stack):
    empty_stack.fifth._stack.extend([2, 4])
    assert str(empty_stack) == str([2, 4])
    yield empty_stack


@pytest.fixture
def double_item_stack_two_non_zero_integers_first_operand_is_smaller(empty_stack):
    empty_stack.fifth._stack.extend([4, 2])
    assert str(empty_stack) == str([4, 2])
    yield empty_stack
