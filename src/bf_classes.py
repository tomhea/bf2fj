from dataclasses import dataclass
from enum import Enum


class BrainfuckException(Exception):
    pass


class BrainfuckUnbalancedBrackets(BrainfuckException):
    pass


class BrainfuckOps(Enum):
    pass


class BrainfuckNonLoopOps(BrainfuckOps):
    INC_DATA = '+'
    DEC_DATA = '-'
    INC_PTR = '>'
    DEC_PTR = '<'
    OUTPUT = '.'
    INPUT = ','

    def __str__(self) -> str:
        """
        @return: the fj-macro that executes the [self] brainfuck-op.
        """
        return self.name.lower()


class BrainfuckLoopOps(BrainfuckOps):
    LOOP_START = '['
    LOOP_END = ']'


@dataclass
class LineComment:
    text_line: str

    def __str__(self) -> str:
        """
        @return: A flip-jump line comment with the given text.
        """
        return f'// {self.text_line}'


_LOOP_LABELS_PREFIX = 'loop_op_'


@dataclass
class LoopOpWithContext:
    """
    Holds a loop start/end brainfuck-op,
     together with its index in the ops array, and the index of the matching loop-brainfuck-op.
    """
    loop_op_type: BrainfuckLoopOps
    current_op_index: int
    matching_op_index: int

    def __str__(self) -> str:
        """
        @return: the fj-macro that executes loop_start / loop_end, proceeds by the current-op label declaration.
        """
        macro_name = self.loop_op_type.name.lower()
        this_label = f'{_LOOP_LABELS_PREFIX}{self.current_op_index}'
        matching_label = f'{_LOOP_LABELS_PREFIX}{self.matching_op_index}'
        return f'{macro_name} {matching_label}\n' \
               f'{this_label}:'
