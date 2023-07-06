from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Union


class BrainfuckOps(Enum):
    pass


class BrainfuckNonLoopOps(BrainfuckOps):
    INC_DATA = '+'
    DEC_DATA = '-'
    INC_PTR = '>'
    DEC_PTR = '<'
    OUTPUT = '.'
    INPUT = ','

    def to_fj(self) -> str:
        """
        @return: the fj-macro that executes the [self] brainfuck-op.
        """
        return self.name.lower()


class BrainfuckLoopOps(BrainfuckOps):
    LOOP_START = '['
    LOOP_END = ']'


@dataclass
class LineComment:
    """
    Sequence of consecutive non-brainfuck chars, that ends by a new-line / EOF / brainfuck-char.
    """
    text_line: str

    def to_fj(self) -> str:
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

    def to_fj(self) -> str:
        """
        @return: the fj-macro that executes loop_start / loop_end, proceeds by the current-op label declaration.
        """
        macro_name = self.loop_op_type.name.lower()
        this_label = f'{_LOOP_LABELS_PREFIX}{self.current_op_index}'
        matching_label = f'{_LOOP_LABELS_PREFIX}{self.matching_op_index}'
        return f'{macro_name} {matching_label}\n' \
               f'{this_label}:'


class OptimizationOp(ABC):
    """
    Abstract class for optimization-ops.
    """
    @abstractmethod
    def to_fj(self) -> str:
        pass


@dataclass
class OptimizationDataOp(OptimizationOp, ABC):
    value: int


class DataSetOp(OptimizationDataOp):
    """
    Optimization-op that represents a loop that sets Data to 0, followed by some DataInc/DataDec ops.
    """
    FJ_MACRO_NAME = 'set_data'

    def to_fj(self) -> str:
        ubyte_value = ((self.value % 256) + 256) % 256
        return f'{self.FJ_MACRO_NAME} {ubyte_value}'


class DataAddOp(OptimizationDataOp):
    """
    Optimization-op that represents multiple DataInc/DataDec ops.
    """
    FJ_MACRO_NAME = 'add_data'

    def to_fj(self) -> str:
        ubyte_value = ((self.value % 256) + 256) % 256
        return {
            0:   '',
            1:   f'{BrainfuckNonLoopOps.INC_DATA.to_fj()}',
            255: f'{BrainfuckNonLoopOps.DEC_DATA.to_fj()}',
        }.get(ubyte_value, f'{self.FJ_MACRO_NAME} {ubyte_value}')


@dataclass
class PtrAddOp(OptimizationOp):
    """
    Optimization-op that represents multiple PtrInc/PtrDec ops.
    """
    FJ_POSITIVE_MACRO_NAME = 'add_ptr'
    FJ_NEGATIVE_MACRO_NAME = 'sub_ptr'
    MAX_ABS_VALUE = 255
    value: int

    def to_fj(self) -> str:
        macro_name = self.FJ_POSITIVE_MACRO_NAME if self.value > 0 else self.FJ_NEGATIVE_MACRO_NAME
        inc_dec_macro_name = BrainfuckNonLoopOps.INC_PTR.to_fj() if self.value > 0 \
            else BrainfuckNonLoopOps.DEC_PTR.to_fj()
        value = abs(self.value) % self.MAX_ABS_VALUE

        ops_prefix = f'{macro_name} {self.MAX_ABS_VALUE}\n' * (abs(self.value) // self.MAX_ABS_VALUE)
        value %= self.MAX_ABS_VALUE

        if value == 0:
            return ops_prefix[:-1]
        if value == 1:
            return f'{ops_prefix}{inc_dec_macro_name}'
        return f'{ops_prefix}{macro_name} {value}'


OpsBeforeOptimization = Union[BrainfuckNonLoopOps, LoopOpWithContext, LineComment]
OpsAfterOptimization = Union[OpsBeforeOptimization, DataSetOp, DataAddOp, PtrAddOp]
