from dataclasses import dataclass
from enum import Enum


class BrainfuckOps(Enum):
    pass


class BrainfuckNonLoopOps(BrainfuckOps):
    INC_DATA = '+'
    DEC_DATA = '-'
    INC_PTR = '>'
    DEC_PTR = '<'
    OUTPUT = '.'
    INPUT = ','

    def __str__(self):
        return ''   # TODO implement with actual fj-code string


class BrainfuckLoopOps(BrainfuckOps):
    LOOP_START = '['
    LOOP_END = ']'


@dataclass
class LineComment:
    text_line: str

    def __str__(self):
        return f'//{self.text_line}\n'


_LOOP_LABELS_PREFIX = 'loop_op_'


@dataclass
class LoopOpWithContext:
    loop_op_type: BrainfuckLoopOps
    current_op_index: int
    matching_op_index: int

    def __str__(self) -> str:
        macro_name = 'loop_start' if self.loop_op_type == BrainfuckLoopOps.LOOP_START else 'loop_end'
        this_label = f'{_LOOP_LABELS_PREFIX}{self.current_op_index}'
        matching_label = f'{_LOOP_LABELS_PREFIX}{self.matching_op_index}'
        return f'{macro_name} {matching_label}\n' \
               f'{this_label}:'
