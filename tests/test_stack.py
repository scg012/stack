import pytest
from io import StringIO
from stack import COMMAND
from stack import OPERATORS
from stack import InvalidCommandError
from stack import InvalidOperationError
from stack import InsufficientStackItemsError


class TestStdInStdOut:
    def test_display_initial_output(self, capsys, monkeypatch, empty_stack):
        command_line = StringIO('')
        monkeypatch.setattr('sys.stdin', command_line)

        empty_stack.main()

        captured = capsys.readouterr()
        assert captured.out == '[]\n'

    def test_stdout_after_pushing(self, capsys, monkeypatch, empty_stack):
        command_line = StringIO('PUSH 1\nPUSH 2')
        monkeypatch.setattr('sys.stdin', command_line)

        empty_stack.main()
        assert str(empty_stack) == str([1, 2])

        captured = capsys.readouterr()
        assert captured.out == '[]\nstack is [1]\nstack is [1, 2]\n'

    def test_stdout_after_command_error(self, capsys, monkeypatch, empty_stack):
        command_line = StringIO('POP 123456')
        monkeypatch.setattr('sys.stdin', command_line)

        empty_stack.main()
        assert str(empty_stack) == str([])

        captured = capsys.readouterr()
        assert captured.out == '[]\nERROR: expected 0 arguments.\n'

    def test_stdout_after_operation_error(self, capsys, monkeypatch, double_item_stack_push_2_push_0):
        command_line = StringIO('/')
        monkeypatch.setattr('sys.stdin', command_line)

        double_item_stack_push_2_push_0.main()
        assert str(double_item_stack_push_2_push_0) == str([2, 0])

        captured = capsys.readouterr()
        assert captured.out == '[2, 0]\nERROR: cannot divide by zero.\n'

    def test_stdout_after_insufficient_items_error(self, capsys, monkeypatch, empty_stack):
        command_line = StringIO('+')
        monkeypatch.setattr('sys.stdin', command_line)

        empty_stack.main()
        assert str(empty_stack) == str([])

        captured = capsys.readouterr()
        assert captured.out == '[]\nERROR: insufficient items on stack.\n'


class TestInterpretInvalid:
    def test_empty_command_line(self, empty_stack):
        with pytest.raises(InvalidCommandError, match="ERROR: no command specified."):
            empty_stack.interpret("")

    def test_invalid_command_and_argument(self, empty_stack):
        with pytest.raises(InvalidCommandError, match="ERROR: unknown command/operator."):
            empty_stack.interpret("INVALID")

    @pytest.mark.parametrize("command_line,error_msg", [
            (f"{COMMAND.PUSH}", "ERROR: expected 1 argument."),
            (f"{COMMAND.PUSH} 1 2 3", "ERROR: expected 1 argument."),
            (f"{COMMAND.PUSH} A B C", "ERROR: expected 1 argument."),
            (f"{COMMAND.POP} 1", "ERROR: expected 0 arguments."),
            (f"{COMMAND.DUP} 1", "ERROR: expected 0 arguments."),
            (f"{COMMAND.SWAP} 1", "ERROR: expected 0 arguments."),
        ]
    )
    def test_with_invalid_argument_count(self, single_item_stack, command_line, error_msg):
        with pytest.raises(InvalidCommandError, match=error_msg):
            single_item_stack.interpret(command_line)


class TestInsufficientStackItemsError:
    @pytest.mark.parametrize(
        "command_line", [
            COMMAND.DUP,
            COMMAND.SWAP,
            OPERATORS.ADD,
            OPERATORS.SUBTRACT,
            OPERATORS.DIVIDE,
            OPERATORS.MULTIPLY,
        ]
    )
    def test_errors_on_empty_stack(self, empty_stack, command_line):
        with pytest.raises(InsufficientStackItemsError, match="ERROR: insufficient items on stack."):
            empty_stack.interpret(command_line)
        assert str(empty_stack) == str([])

    @pytest.mark.parametrize(
        "command_line", [
            COMMAND.SWAP,
            OPERATORS.ADD,
            OPERATORS.SUBTRACT,
            OPERATORS.DIVIDE,
            OPERATORS.MULTIPLY,
        ]
    )
    def test_errors_on_single_item_stack(self, single_item_stack, command_line):
        with pytest.raises(InsufficientStackItemsError, match="ERROR: insufficient items on stack."):
            single_item_stack.interpret(command_line)
        assert str(single_item_stack) == str([1])


class TestPush:
    def test_push_on_empty_stack(self, empty_stack):
        command = f"{COMMAND.PUSH} 1"
        empty_stack.interpret(command)
        assert str(empty_stack) == str([1])

    def test_on_non_empty_stack(self, single_item_stack):
        command = f"{COMMAND.PUSH} 3"
        single_item_stack.interpret(command)
        assert str(single_item_stack) == str([1, 3])

    def test_push_with_invalid_argument_type(self, single_item_stack):
        with pytest.raises(InvalidCommandError, match="ERROR: an integer argument expected."):
            single_item_stack.interpret(f"{COMMAND.PUSH} ABC")


class TestPop:
    def test_on_single_item_stack(self, single_item_stack):
        single_item_stack.interpret(COMMAND.POP)
        assert str(single_item_stack) == str([])

    def test_on_double_item_stack(self, double_item_stack):
        double_item_stack.interpret(COMMAND.POP)
        assert str(double_item_stack) == str([1])


class TestDup:
    def test_on_single_item_stack(self, single_item_stack):
        single_item_stack.interpret(COMMAND.DUP)
        assert str(single_item_stack) == str([1, 1])

    def test_on_double_item_stack(self, double_item_stack):
        double_item_stack.interpret(COMMAND.DUP)
        assert str(double_item_stack) == str([1, 2, 2])


class TestSwap:
    def test_on_double_item_stack(self, double_item_stack):
        double_item_stack.interpret(COMMAND.SWAP)
        assert str(double_item_stack) == str([2, 1])


class TestAdd:
    def test_on_double_item_stack(self, double_item_stack):
        double_item_stack.interpret(OPERATORS.ADD)
        assert str(double_item_stack) == str([3])


class TestDivide:
    def test_without_remainder(self, double_item_stack):
        double_item_stack.interpret(OPERATORS.DIVIDE)
        assert str(double_item_stack) == str([0])

    def test_with_remainder(self, double_item_stack_push_2_push_5):
        double_item_stack_push_2_push_5.interpret(OPERATORS.DIVIDE)
        assert str(double_item_stack_push_2_push_5) == str([0])

    def test_with_two_non_zero_integers_first_operand_is_larger(
            self,
            double_item_stack_two_non_zero_integers_first_operand_is_larger):
        double_item_stack_two_non_zero_integers_first_operand_is_larger.interpret(OPERATORS.DIVIDE)
        assert str(double_item_stack_two_non_zero_integers_first_operand_is_larger) == str([0])

    def test_with_two_non_zero_integers_first_operand_is_smaller(
            self,
            double_item_stack_two_non_zero_integers_first_operand_is_smaller):
        double_item_stack_two_non_zero_integers_first_operand_is_smaller.interpret(OPERATORS.DIVIDE)
        assert str(double_item_stack_two_non_zero_integers_first_operand_is_smaller) == str([2])

    def test_zero_divided_by_integer(self, double_item_stack_push_0_push_2):
        double_item_stack_push_0_push_2.interpret(OPERATORS.DIVIDE)
        assert str(double_item_stack_push_0_push_2) == str([0])

    def test_for_divide_by_zero_error(self, double_item_stack_push_2_push_0):
        with pytest.raises(InvalidOperationError):
            double_item_stack_push_2_push_0.interpret(OPERATORS.DIVIDE)


class TestMultiply:
    def test_on_double_item_stack_push_0_push_2(self, double_item_stack_push_0_push_2):
        double_item_stack_push_0_push_2.interpret(OPERATORS.MULTIPLY)
        assert str(double_item_stack_push_0_push_2) == str([0])

    def test_on_zero_operand(self, double_item_stack_push_2_push_0):
        double_item_stack_push_2_push_0.interpret(OPERATORS.MULTIPLY)
        assert str(double_item_stack_push_2_push_0) == str([0])

    def test_with_non_zero_integer(self, double_item_stack_push_2_push_5):
        double_item_stack_push_2_push_5.interpret(OPERATORS.MULTIPLY)
        assert str(double_item_stack_push_2_push_5) == str([10])


class TestSubtract:
    def test_on_negative_result(self, double_item_stack):
        double_item_stack.interpret(OPERATORS.SUBTRACT)
        assert str(double_item_stack) == str([-1])

    def test_operand_order_with_second_as_larger(self, double_item_stack_push_0_push_2):
        """Check which stack value is used as the first operand."""
        double_item_stack_push_0_push_2.interpret(OPERATORS.SUBTRACT)
        assert str(double_item_stack_push_0_push_2) == str([-2])

    def test_operand_order_with_second_as_smaller(self, double_item_stack_push_2_push_0):
        """Check which stack value is used as the first operand."""
        double_item_stack_push_2_push_0.interpret(OPERATORS.SUBTRACT)
        assert str(double_item_stack_push_2_push_0) == str([2])
