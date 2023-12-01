from pathlib import Path
from typing import List, Union

from bf2fj.bf_classes import BrainfuckNonLoopOps, LineComment, LoopOpWithContext, BrainfuckLoopOps, \
    OpsBeforeOptimization, OpsAfterOptimization, DataAddOp, DataSetOp, PtrAddOp, OptimizationDataOp
from bf2fj.compiler_exceptions import CharDoesntMatchHandler, BrainfuckUnbalancedBrackets


SOURCE_DIR = Path(__file__).parent
FLIPJUMP_OUTPUT_FORMAT_FILE = SOURCE_DIR / 'flipjump_output_format.fj'
COMPILED_BRAINFUCK_OPS_SPOT__FJ_FORMAT_CONST = '!!!HERE_THE_COMPILED_BRAINFUCK_OPS_WILL_BE!!!'
NUMBER_OF_BRAINFUCK_DATA_CELLS__FJ_FORMAT_CONST = "!!!NUMBER_OF_BRAINFUCK_DATA_CELLS!!!"

DEFAULT_NUMBER_OF_BRAINFUCK_DATA_CELLS = 30000

_UNDEFINED_INDEX = -1
_FIRST_LINE_INDEX = 1

LAST_INDEX = -1
FILE_READ = 'r'

OPTIMIZATION_STARTING_COMMENT = 'The next code was optimized by bf2fj:\n'

ADDING_VALUE_BY_OP = {
    BrainfuckNonLoopOps.INC_DATA: 1,
    BrainfuckNonLoopOps.INC_PTR: 1,
    BrainfuckNonLoopOps.DEC_DATA: -1,
    BrainfuckNonLoopOps.DEC_PTR: -1,
}
DATA_OPS = (BrainfuckNonLoopOps.INC_DATA, BrainfuckNonLoopOps.DEC_DATA)
PTR_OPS = (BrainfuckNonLoopOps.INC_PTR, BrainfuckNonLoopOps.DEC_PTR)


def can_cover_256_loop(jump_value: int) -> bool:
    """
    :param jump_value: some ptr-offset-jump (e.g. "><<<<>" -> "-2").
    :return: True if its possible reaches index 0 while continuing jumping that jump-value (with mod 256)
     from any starting index. It does it by checking if gcd(jump_value, 256) == 1.
    """
    abs_jump = abs(jump_value)
    is_0_or_power_of_2 = (abs_jump & (abs_jump - 1)) == 0
    return not is_0_or_power_of_2 or abs_jump == 1


def is_loop_end(op: OpsBeforeOptimization) -> bool:
    """
    :param op: a brainfuck op.
    :return: True if it's a loop-end op.
    """
    return isinstance(op, LoopOpWithContext) and op.loop_op_type == BrainfuckLoopOps.LOOP_END


def is_loop_start(op: OpsBeforeOptimization) -> bool:
    """
    :param op: a brainfuck op.
    :return: True if it's a loop-start op.
    """
    return isinstance(op, LoopOpWithContext) and op.loop_op_type == BrainfuckLoopOps.LOOP_START


class Bf2FjCompiler:
    """
    Compiles brainfuck code into flip-jump code.
    """
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
        :param current_char: the currently-processed char from the brainfuck code.
        :raises CharDoesntMatchHandler: if current_char doesn't represent a non-loop op.
        """
        try:
            brainfuck_loop_op = BrainfuckNonLoopOps(current_char)  # raises ValueError if current_char matches nothing.
        except ValueError:
            raise CharDoesntMatchHandler("Given char isn't a non-loop op")
        self._insert_current_line_comment()
        self.brainfuck_ops.append(brainfuck_loop_op)

    def _verify_and_handle_loop_op(self, current_char: str) -> None:
        """
        If current_char is a loop-op, register and handle it (appends LoopOpWithContext).
        Otherwise, raise an exception.
        :param current_char: the currently-processed char from the brainfuck code.
        :raises CharDoesntMatchHandler: if current_char doesn't represent a loop op.
        :raises BrainfuckUnbalancedBrackets: if current is loop-end, but we aren't in any loop.
        """
        try:
            brainfuck_loop_op = BrainfuckLoopOps(current_char)  # raises ValueError if current_char matches nothing.
        except ValueError:
            raise CharDoesntMatchHandler("Given char isn't a loop op")
        self._insert_current_line_comment()

        current_loop_op_index = len(self.brainfuck_ops)
        if brainfuck_loop_op == BrainfuckLoopOps.LOOP_START:
            self.brainfuck_ops.append(LoopOpWithContext(brainfuck_loop_op, current_loop_op_index, _UNDEFINED_INDEX))
            self.loop_start_indices_stack.append(current_loop_op_index)
            return

        try:
            loop_start_index = self.loop_start_indices_stack.pop()
        except IndexError:
            raise BrainfuckUnbalancedBrackets("Error: Encountered ']' but we aren't in any loop.")
        self.brainfuck_ops.append(LoopOpWithContext(brainfuck_loop_op, current_loop_op_index, loop_start_index))
        self.brainfuck_ops[loop_start_index].matching_op_index = current_loop_op_index

    def _handle_non_op_char(self, current_char: str) -> None:
        """
        If current_char is a new-line, register a new comment line. Otherwise, append char to the current comment line.
        :param current_char: the currently-processed char from the brainfuck code.
        """
        if current_char == '\n':
            self._insert_current_line_comment()
            self.current_line += 1
        else:
            self.current_comment += current_char

    def parse_brainfuck_ops(self) -> None:
        """
        Create the list of brainfuck ops, with brackets-context, and also the original comments.
        :raises BrainfuckUnbalancedBrackets: if brackets aren't ordered right.
        """
        self.brainfuck_ops = []
        self.current_comment = ''
        self.current_line = _FIRST_LINE_INDEX
        self.loop_start_indices_stack = []

        for char in self.brainfuck_code:
            try:  # is it non-loop-op?
                self._verify_and_handle_non_loop_op(char)
                continue
            except CharDoesntMatchHandler:
                pass

            try:  # is it loop-op?
                self._verify_and_handle_loop_op(char)
                continue
            except CharDoesntMatchHandler:
                pass

            # it is a comment
            self._handle_non_op_char(char)

        self._insert_current_line_comment()
        if self.loop_start_indices_stack:
            raise BrainfuckUnbalancedBrackets("Brainfuck program ended while still in a loop.")

    @staticmethod
    def optimize_multiple_data_ops(optimized_ops: List[OpsAfterOptimization], current_op: BrainfuckNonLoopOps) -> None:
        """
        Optimize multiple data ops. +++++ -> +5, ----++- -> -3. Does it in place (updates optimized_ops).
        :param optimized_ops: The current list of the already optimized ops.
        :param current_op: The current processed op (data-inc/dec).
        """
        last_op = optimized_ops[LAST_INDEX]
        value_diff = ADDING_VALUE_BY_OP[current_op]

        if isinstance(last_op, OptimizationDataOp):
            last_op.value += value_diff
        else:
            optimized_ops.append(DataAddOp(value_diff))

    @staticmethod
    def optimize_multiple_pointer_ops(optimized_ops: List[OpsAfterOptimization], current_op: BrainfuckNonLoopOps) -> None:
        """
        Optimize multiple pointer ops. ">>>>>" -> ">5", "<<<<>><" -> "<3". Does it in place (updates optimized_ops).
        :param optimized_ops: The current list of the already optimized ops.
        :param current_op: The current processed op (pointer-inc/dec).
        """
        last_op = optimized_ops[LAST_INDEX]
        value_diff = ADDING_VALUE_BY_OP[current_op]

        if isinstance(last_op, PtrAddOp):
            last_op.value += value_diff
        else:
            optimized_ops.append(PtrAddOp(value_diff))

    @staticmethod
    def can_optimize_loop_to_set_data_0(
            optimized_ops: List[OpsAfterOptimization], current_op: OpsBeforeOptimization) -> bool:
        """
        :param optimized_ops: The current list of the already optimized ops.
        :param current_op: The current op.
        :return: True if current op closes a loop that can be optimized into "*ptr = 0"
        """
        return is_loop_end(current_op) and \
            len(optimized_ops) >= 2 and is_loop_start(optimized_ops[-2]) and \
            isinstance(optimized_ops[LAST_INDEX], OptimizationDataOp) and \
            can_cover_256_loop(optimized_ops[LAST_INDEX].value)

    @staticmethod
    def optimize_zeroing_loop(optimized_ops: List[OpsAfterOptimization]) -> None:
        """
        Removes the whole loop (and if there is a data-op before it, removes it too) from the optimized ops list,
         and replace them with *ptr = 0.
        :param optimized_ops: The current list of the already optimized ops
        """
        optimized_ops.pop()
        optimized_ops.pop()
        if isinstance(optimized_ops[LAST_INDEX], OptimizationDataOp):
            optimized_ops.pop()  # remove
        optimized_ops.append(DataSetOp(0))

    def optimize_ops(self, remove_comments: bool = False) -> None:
        """
        Optimize the parsed brainfuck-ops list, in place.
        :param remove_comments: if True: removes existing comments from the optimized code.
         It allows more optimizations that having the comments block.
        """
        optimized_ops = [LineComment(OPTIMIZATION_STARTING_COMMENT)]  # The list is never empty.

        for current_op in self.brainfuck_ops:
            if current_op in DATA_OPS:
                self.optimize_multiple_data_ops(optimized_ops, current_op)  # +++, ---, +-++, ...

            elif current_op in PTR_OPS:
                self.optimize_multiple_pointer_ops(optimized_ops, current_op)  # >>>, <<<, <>><>>...

            elif self.can_optimize_loop_to_set_data_0(optimized_ops, current_op):
                self.optimize_zeroing_loop(optimized_ops)  # [+], [-], [+++], [+-+] ...

            elif not (remove_comments and isinstance(current_op, LineComment)):
                optimized_ops.append(current_op)

        self.brainfuck_ops = optimized_ops

    def get_fj_code_of_brainfuck_ops(self) -> str:
        """
        :return: The flip-jump code that represents the brainfuck ops.
        :note: This isn't the whole resulted fj-file, as many important macro definitions are missing from it.
         This is the main body of the fj-file, but mostly contains macro calls that it doesn't define.
        """
        fj_code_lines = [op.to_fj() for op in self.brainfuck_ops]
        return '\n'.join(fj_code_lines)

    def get_compiled_code(self, *, apply_optimizations: bool = True) -> str:
        """
        :return: The .fj file content, that was compiled from the given brainfuck_code.
        """
        self.parse_brainfuck_ops()
        if apply_optimizations:
            self.optimize_ops()

        fj_code__brainfuck_ops = self.get_fj_code_of_brainfuck_ops()

        with open(FLIPJUMP_OUTPUT_FORMAT_FILE, FILE_READ) as fj_format:
            generic_fj_code__without_brainfuck_ops = fj_format.read()

        return generic_fj_code__without_brainfuck_ops \
            .replace(COMPILED_BRAINFUCK_OPS_SPOT__FJ_FORMAT_CONST, fj_code__brainfuck_ops) \
            .replace(NUMBER_OF_BRAINFUCK_DATA_CELLS__FJ_FORMAT_CONST, str(self.number_of_brainfuck_cells))
