from typing import List

from definitions import SOURCE_DIR
from src.bf_classes import BrainfuckNonLoopOps, LineComment, LoopOpWithContext, BrainfuckLoopOps, \
    BrainfuckUnbalancedBrackets, OpsBeforeOptimization, OpsAfterOptimization, DataAddOp, DataSetOp, PtrAddOp, \
    OptimizationDataOp

FLIPJUMP_OUTPUT_FORMAT_FILE = SOURCE_DIR / 'flipjump_output_format.fj'
COMPILED_BRAINFUCK_OPS_SPOT__FJ_FORMAT_CONST = '!!!HERE_THE_COMPILED_BRAINFUCK_OPS_WILL_BE!!!'
NUMBER_OF_BRAINFUCK_DATA_CELLS__FJ_FORMAT_CONST = "!!!NUMBER_OF_BRAINFUCK_DATA_CELLS!!!"

DEFAULT_NUMBER_OF_BRAINFUCK_DATA_CELLS = 30000

_UNDEFINED_INDEX = -1
_FIRST_LINE_INDEX = 1


def can_cover_256_loop(jump_value: int):
    abs_jump = abs(jump_value)
    is_0_or_power_of_2 = (abs_jump & (abs_jump - 1)) == 0
    return not is_0_or_power_of_2 or abs_jump == 1


def is_loop_end(op: OpsBeforeOptimization) -> bool:
    return isinstance(op, LoopOpWithContext) and op.loop_op_type == BrainfuckLoopOps.LOOP_END


def is_loop_start(op: OpsBeforeOptimization) -> bool:
    return isinstance(op, LoopOpWithContext) and op.loop_op_type == BrainfuckLoopOps.LOOP_START


def can_optimize_loop_to_set_data_0(op: OpsBeforeOptimization, optimized_ops: List[OpsAfterOptimization]):
    return is_loop_end(op) and \
        len(optimized_ops) >= 2 and is_loop_start(optimized_ops[-2]) and \
        isinstance(optimized_ops[-1], OptimizationDataOp) and can_cover_256_loop(optimized_ops[-1].value)


class Bf2FjCompiler:
    brainfuck_ops: List[OpsBeforeOptimization]
    current_comment: str
    current_line: int
    loop_start_indices_stack: List[int]

    def __init__(self, brainfuck_code: str, *,
                 number_of_brainfuck_cells: int = DEFAULT_NUMBER_OF_BRAINFUCK_DATA_CELLS):
        self.brainfuck_code = brainfuck_code
        self.number_of_brainfuck_cells = number_of_brainfuck_cells

    def _insert_current_line_comment(self) -> None:
        """
        Register the current line-comment, and start a new empty one.
        """
        comment = self.current_comment.strip()
        if comment:
            self.brainfuck_ops.append(LineComment(comment))
        self.current_comment = ''

    def _verify_and_handle_non_loop_op(self, current_char: str) -> None:
        """
        If current_char is a non-loop-op, register and handle it. Otherwise, raise an exception.
        @param current_char: the currently-processed char from the brainfuck code.
        @raises ValueError: if current_char doesn't represent a non-loop op.
        """
        brainfuck_loop_op = BrainfuckNonLoopOps(current_char)   # raises ValueError if current_char matches nothing.
        self._insert_current_line_comment()
        self.brainfuck_ops.append(brainfuck_loop_op)

    def _verify_and_handle_loop_op(self, current_char: str) -> None:
        """
        If current_char is a loop-op, register and handle it (appends LoopOpWithContext).
        Otherwise, raise an exception.
        @param current_char: the currently-processed char from the brainfuck code.
        @raises ValueError: if current_char doesn't represent a loop op.
        @raises BrainfuckUnbalancedBrackets: if current is loop-end, but we aren't in any loop.
        """
        brainfuck_loop_op = BrainfuckLoopOps(current_char)   # raises ValueError if current_char matches nothing.
        self._insert_current_line_comment()

        current_loop_op_index = len(self.brainfuck_ops)
        if brainfuck_loop_op == BrainfuckLoopOps.LOOP_START:
            self.brainfuck_ops.append(LoopOpWithContext(brainfuck_loop_op, current_loop_op_index, _UNDEFINED_INDEX))
            self.loop_start_indices_stack.append(current_loop_op_index)
        else:
            try:
                loop_start_index = self.loop_start_indices_stack.pop()
                self.brainfuck_ops.append(LoopOpWithContext(brainfuck_loop_op, current_loop_op_index, loop_start_index))
                self.brainfuck_ops[loop_start_index].matching_op_index = current_loop_op_index
            except IndexError:
                raise BrainfuckUnbalancedBrackets("Error: Encountered ']' but we aren't in any loop.")

    def _handle_non_op_char(self, current_char: str) -> None:
        """
        If current_char is a new-line, register a new comment line. Otherwise, append char to the current comment line.
        @param current_char: the currently-processed char from the brainfuck code.
        """
        if current_char == '\n':
            self._insert_current_line_comment()
            self.current_line += 1
        else:
            self.current_comment += current_char

    def get_brainfuck_ops(self) -> List[OpsBeforeOptimization]:
        """
        Create the list of brainfuck ops, with brackets-context, and also the original comments.
        @raises BrainfuckUnbalancedBrackets: if brackets aren't ordered right.
        @return: The list of brainfuck ops.
        """
        self.brainfuck_ops = []
        self.current_comment = ''
        self.current_line = _FIRST_LINE_INDEX
        self.loop_start_indices_stack = []

        for char in self.brainfuck_code:
            try:    # is it non-loop-op?
                self._verify_and_handle_non_loop_op(char)
                continue

            except ValueError:  # TODO Throw a more indicative Error type.
                pass
            try:    # is it loop-op?
                self._verify_and_handle_loop_op(char)
                continue

            except ValueError:  # it's comment.
                self._handle_non_op_char(char)

        if self.loop_start_indices_stack:
            raise BrainfuckUnbalancedBrackets("Brainfuck program ended while still in a loop.")
        return self.brainfuck_ops

    @staticmethod
    def optimize_ops(brainfuck_ops: List[OpsBeforeOptimization]) -> List[OpsAfterOptimization]:
        """
        Optimize the given list of brainfuck-ops.
        @param brainfuck_ops: A list of brainfuck ops.
        @returns: the optimized ops.
        """
        # TODO functionalize and make it mote clean-code.

        _adding_value_by_op = {
            BrainfuckNonLoopOps.INC_DATA: 1,
            BrainfuckNonLoopOps.INC_PTR: 1,
            BrainfuckNonLoopOps.DEC_DATA: -1,
            BrainfuckNonLoopOps.DEC_PTR: -1,
        }
        _data_ops = (BrainfuckNonLoopOps.INC_DATA, BrainfuckNonLoopOps.DEC_DATA)
        _ptr_ops = (BrainfuckNonLoopOps.INC_PTR, BrainfuckNonLoopOps.DEC_PTR)

        optimized_ops = [LineComment('The next code was optimized by bf2fj:\n')]  # The list is never empty.

        for op in brainfuck_ops:
            last_op = optimized_ops[-1]

            if op in _data_ops:
                value_diff = _adding_value_by_op[op]
                if isinstance(last_op, OptimizationDataOp):             # +++, ---, +-++, ...
                    last_op.value += value_diff
                else:
                    optimized_ops.append(DataAddOp(value_diff))

            elif op in _ptr_ops:
                value_diff = _adding_value_by_op[op]
                if isinstance(last_op, PtrAddOp):                       # >>>, <<<, <>><>>...
                    last_op.value += value_diff
                else:
                    optimized_ops.append(PtrAddOp(value_diff))

            elif can_optimize_loop_to_set_data_0(op, optimized_ops):    # [+], [-], [+++], [+-+] ...
                optimized_ops.pop()
                optimized_ops.pop()
                if isinstance(optimized_ops[-1], OptimizationDataOp):
                    optimized_ops.pop()
                optimized_ops.append(DataSetOp(0))

            else:
                optimized_ops.append(op)

        return optimized_ops

    def get_compiled_code(self, *, apply_optimizations: bool = True) -> str:
        """
        @return: The .fj file content, that was compiled from the given brainfuck_code.
        """
        brainfuck_ops_with_context = self.get_brainfuck_ops()
        if apply_optimizations:
            brainfuck_ops_with_context = self.optimize_ops(brainfuck_ops_with_context)

        fj_code_lines = list(map(str, brainfuck_ops_with_context))
        fj_code__brainfuck_ops = '\n'.join(fj_code_lines)

        with open(FLIPJUMP_OUTPUT_FORMAT_FILE, 'r') as fj_format:
            generic_fj_code__without_brainfuck_ops = fj_format.read()

        return generic_fj_code__without_brainfuck_ops\
            .replace(COMPILED_BRAINFUCK_OPS_SPOT__FJ_FORMAT_CONST, fj_code__brainfuck_ops)\
            .replace(NUMBER_OF_BRAINFUCK_DATA_CELLS__FJ_FORMAT_CONST, str(self.number_of_brainfuck_cells))
