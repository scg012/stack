#!/usr/bin/env python3

"""
Stack is a python program which works as a fifth interpreter.
Each line of input to the program represents a single fifth command.

The result of each command is output to the terminal.
"""
import operator

from fifth import Fifth
from fifth import COMMAND
from fifth import OPERATORS
from fifth import commands
from fifth import operators
from fifth import InsufficientStackItemsError


class InvalidCommandError(Exception):
    """For commands that caused an error."""


class InvalidOperationError(Exception):
    """For operations that caused an error."""


class Stack:
    """An interpreter for the Fifth stack-based language.
    """

    def __init__(self):
        self.fifth = Fifth()

        # A dict mapping input commands to functions
        self.command_func = {
            COMMAND.PUSH: self.fifth.push,
            COMMAND.POP: self.fifth.pop,
            COMMAND.SWAP: self.fifth.swap,
            COMMAND.DUP: self.fifth.dup,
        }

        # A dict mapping input operators to functions
        self.operator_func = {
            OPERATORS.ADD: operator.add,
            OPERATORS.SUBTRACT: operator.sub,
            OPERATORS.MULTIPLY: operator.mul,
            OPERATORS.DIVIDE: operator.floordiv,
        }

    def __str__(self):
        return str(self.fifth)

    @staticmethod
    def __validate_command_args_count(cmd: list = None, required_args: int = 0):
        if len(cmd) != required_args:
            if required_args == 1:
                raise InvalidCommandError(f"ERROR: expected {required_args} argument.")

            if required_args != 1:
                raise InvalidCommandError(f"ERROR: expected {required_args} arguments.")

    def interpret(self, command_line: str) -> str:
        """Interprets the Fifth commands and operators.

        :param command_line The command line input.
        :raises InvalidCommandError If a command cannot be performed.
        :raises InvalidOperationError If an operation cannot be performed.
        """
        if not command_line:
            raise InvalidCommandError("ERROR: no command specified.")

        command_line_split = command_line.split()
        command = command_line_split[0]

        if command not in commands and command not in operators:
            raise InvalidCommandError("ERROR: unknown command/operator.")

        if command in commands:
            cmd_func = self.command_func.get(command)
            # Handle any specific arguments to functions
            command_args = command_line_split[1:]
            if command == COMMAND.PUSH:
                self.__validate_command_args_count(command_args, 1)
                first_argument = command_line_split.pop()
                if not first_argument.isdigit():
                    raise InvalidCommandError("ERROR: an integer argument expected.")
                cmd_func(int(first_argument))
            else:
                self.__validate_command_args_count(command_args, 0)
                cmd_func()
        else:
            first_operand = self.fifth.pop()
            try:
                # The second item from the top of the stack acts as
                # the summend or multiplier or dividend or minuend
                second_operand = self.fifth.pop()
            except InsufficientStackItemsError as error:
                # reset the stack to its original state
                self.fifth.push(first_operand)
                raise error

            if command == OPERATORS.DIVIDE and first_operand == 0:
                # reset the stack to its original state
                self.fifth.push(second_operand)
                self.fifth.push(first_operand)
                raise InvalidOperationError("ERROR: cannot divide by zero.")

            op_func = self.operator_func.get(command)
            # The order of operands affects division and subtraction arithmetic
            result = op_func(second_operand, first_operand)
            self.fifth.push(result)

        return str(self.fifth)

    def main(self):
        """Reads in supported commands and operators from stdin until EOF."""
        print(str(self))

        try:
            while command_line := input():
                try:
                    print(f"stack is {self.interpret(command_line)}")
                except (InvalidCommandError,
                        InvalidOperationError,
                        InsufficientStackItemsError) as error:
                    print(error)
        except EOFError:
            pass


if __name__ == "__main__":
    app = Stack()
    app.main()
