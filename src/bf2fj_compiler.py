import string
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import List, Union

from definitions import SOURCE_DIR


FLIPJUMP_OUTPUT_FORMAT_FILE = SOURCE_DIR / 'flipjump_output_format.fj'
COMPILED_BRAINFUCK_OPS_SPOT = '!!!HERE_THE_COMPILED_BRAINFUCK_OPS_WILL_BE!!!'


class BrainfuckOps(Enum):
    IncData = '+'
    DecData = '-'
    IncPtr = '>'
    DecPtr = '<'
    Output = '.'
    Input = ','
    LoopStart = '['
    LoopEnd = ']'


@dataclass
class LineComment:
    text_line: str

    def __str__(self):
        return f'//{self.text_line}'


class FormatDict(dict):
    def __missing__(self, key):
        return f"{{key}}"


class Bf2FjCompiler:
    def __init__(self, brainfuck_code: str):
        self.brainfuck_code = brainfuck_code

    @cached_property
    def brainfuck_ops(self) -> List[Union[BrainfuckOps, LineComment]]:
        brainfuck_ops = []
        current_comment = ''
        for char in self.brainfuck_code:
            try:
                brainfuck_op = BrainfuckOps(char)

                brainfuck_ops.extend(LineComment(text_line) for text_line in current_comment.split('\n'))
                current_comment = ''

                brainfuck_ops.append(brainfuck_op)
            except ValueError:
                current_comment += char

        return brainfuck_ops

    def get_compiled_code(self) -> str:
        brainfuck_ops = self.brainfuck_ops

        fj_code_lines = []
        for brainfuck_op in brainfuck_ops:
            fj_code_lines.append('')    # TODO something
            # TODO implement '[' stack for the '[' , ']' ops.
        fj_code__brainfuck_ops = '\n'.join(fj_code_lines)

        with open(FLIPJUMP_OUTPUT_FORMAT_FILE, 'r') as fj_format:
            generic_fj_code__without_brainfuck_ops = fj_format.read()

        return generic_fj_code__without_brainfuck_ops.replace(COMPILED_BRAINFUCK_OPS_SPOT, fj_code__brainfuck_ops)
