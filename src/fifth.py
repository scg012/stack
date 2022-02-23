"""
Fifth supports the following arithmetic operators:

+ - * /
which act upon the top of the stack.

Fifth also supports arithmetic operators that act upon the bottom of the stack, i.e. in the reverse manner:
r+
r-
r*
r/


Fifth also supports the following commands:

PUSH x - push x onto the top of the stack, where x is a valid integer
POP - remove the top element of the stack
SWAP - swap the top two elements of the stack
DUP - duplicate the top element of the stack

Fifth also supports arithmetic operators that act upon the bottom of the stack, i.e. in the reverse manner:
rPUSH x - push x onto the bottom of the stack, where x is a valid integer
rPOP - remove the bottom element of the stack
rSWAP - swap the bottom two elements of the stack
rDUP - duplicate bottom top element of the stack

"""

from enum import Enum, unique
from typing import List
from functools import wraps


class InsufficientStackItemsError(Exception):
    """When there are insufficient items on the stack to perform an operation."""


class InvalidOperationError(Exception):
    """For operations that caused an error."""


class BaseEnum(Enum):
    """An enum base class with a list() helper."""
    @classmethod
    def list(cls):
        """Get a list of enum values."""
        return list(map(lambda c: c.value, cls))


@unique
class COMMAND(str, BaseEnum):
    """Supported Commands."""
    PUSH = 'PUSH'
    POP = 'POP'
    SWAP = 'SWAP'
    DUP = 'DUP'
    REVERSE_PUSH = 'rPUSH'
    REVERSE_POP = 'rPOP'
    REVERSE_SWAP = 'rSWAP'
    REVERSE_DUP = 'rDUP'


@unique
class OPERATORS(str, BaseEnum):
    """Supported arithmetic operators."""
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    REVERSE_ADD = 'r+'
    REVERSE_SUBTRACT = 'r-'
    REVERSE_MULTIPLY = 'r*'
    REVERSE_DIVIDE = 'r/'


commands = COMMAND.list()
operators = OPERATORS.list()


class Fifth:
    """Fifth is a new stack-based language.
    A stack is a data structure which can only have elements added to the top.
    Fifth stores a stack of integers and supports commands to manipulate that stack.
    Operations always apply to the top of the stack.
    """
    def __init__(self, data: List[int] = None):
        if data:
            self._stack: List[int] = list(data)
        else:
            self._stack: List[int] = []

    def __str__(self):
        return str(self._stack)

    @staticmethod
    def validate_min_stack_size(minimum):
        """A decorator to validate the minimum stack size"""
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.size() < minimum:
                    raise InsufficientStackItemsError("ERROR: insufficient items on stack.")
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    def push(self, number: int):
        """Push a valid integer onto the top of the stack."""
        self._stack.append(int(number))

    @validate_min_stack_size(1)
    def pop(self) -> int:
        """Remove the top element of the stack."""
        return self._stack.pop()

    @validate_min_stack_size(2)
    def swap(self):
        """Swap the top two elements of the stack."""
        self._stack[-2], self._stack[-1] = self._stack[-1], self._stack[-2]

    @validate_min_stack_size(1)
    def dup(self):
        """Duplicate the top element of the stack."""
        self._stack.append(self._stack[-1])

    def size(self) -> int:
        """The number of items on the stack."""
        return len(self._stack)

    def reverse_push(self, number: int):
        """Push a valid integer onto the bottom of the stack."""
        self._stack.insert(0, int(number))

    @validate_min_stack_size(2)
    def reverse_swap(self):
        """Swap the top two elements of the stack."""
        self._stack[1], self._stack[2] = self._stack[0], self._stack[1]

    @validate_min_stack_size(1)
    def reverse_dup(self):
        """Duplicate the top element of the stack."""
        self._stack.insert(0, self._stack[1])

    @validate_min_stack_size(1)
    def reverse_pop(self) -> int:
        """Remove the top element of the stack."""
        return self._stack.pop(0)

    @validate_min_stack_size(2)
    def reverse_add(self):
        """Adds the bottom two integers of the stack"""
        self._stack[1] = self._stack[0] + self._stack[1]
        self._stack.pop(0)

    @validate_min_stack_size(2)
    def reverse_subtract(self):
        """Adds the bottom two integers of the stack"""
        self._stack[1] = self._stack[0] - self._stack[1]
        self._stack.pop(0)

    @validate_min_stack_size(2)
    def reverse_multiply(self):
        """Adds the bottom two integers of the stack"""
        self._stack[1] = self._stack[0] * self._stack[1]
        self._stack.pop(0)

    @validate_min_stack_size(2)
    def reverse_floordiv(self):
        """Adds the bottom two integers of the stack"""
        if self._stack[1] == 0:
            raise InvalidOperationError("ERROR: cannot divide by zero.")

        self._stack[1] = self._stack[0] // self._stack[1]
        self._stack.pop(0)
