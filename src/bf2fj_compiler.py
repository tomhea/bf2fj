from typing import List, Union

from definitions import SOURCE_DIR
from src.bf_classes import BrainfuckNonLoopOps, LineComment, LoopOpWithContext, BrainfuckLoopOps, \
    BrainfuckUnbalancedBrackets

FLIPJUMP_OUTPUT_FORMAT_FILE = SOURCE_DIR / 'flipjump_output_format.fj'
COMPILED_BRAINFUCK_OPS_SPOT__FJ_FORMAT_CONST = '!!!HERE_THE_COMPILED_BRAINFUCK_OPS_WILL_BE!!!'
NUMBER_OF_BRAINFUCK_DATA_CELLS__FJ_FORMAT_CONST = "!!!NUMBER_OF_BRAINFUCK_DATA_CELLS!!!"

DEFAULT_NUMBER_OF_BRAINFUCK_DATA_CELLS = 30000

_UNDEFINED_INDEX = -1
_FIRST_LINE_INDEX = 1


class Bf2FjCompiler:
    brainfuck_ops: List[Union[BrainfuckNonLoopOps, LoopOpWithContext, LineComment]]
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
        @raises ValueError: if current_char doesn't represent a non-loop op.
        """
        brainfuck_loop_op = BrainfuckNonLoopOps(current_char)   # raises ValueError if current_char matches nothing.
        self._insert_current_line_comment()
        self.brainfuck_ops.append(brainfuck_loop_op)

    def _verify_and_handle_loop_op(self, current_char: str) -> None:
        """
        If current_char is a loop-op, register and handle it (appends LoopOpWithContext).
        Otherwise, raise an exception.
        :param current_char: the currently-processed char from the brainfuck code.
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

    def get_brainfuck_ops(self) -> List[Union[BrainfuckNonLoopOps, LoopOpWithContext, LineComment]]:
        """
        @raises BrainfuckUnbalancedBrackets: if brackets aren't ordered right.
        @return: The list of
        """
        self.brainfuck_ops = []
        self.current_comment = ''
        self.current_line = _FIRST_LINE_INDEX
        self.loop_start_indices_stack = []

        for char in self.brainfuck_code:
            try:    # is it non-loop-op?
                self._verify_and_handle_non_loop_op(char)
                continue

            except ValueError:
                pass
            try:    # is it loop-op?
                self._verify_and_handle_loop_op(char)
                continue

            except ValueError:  # it's comment.
                self._handle_non_op_char(char)

        if self.loop_start_indices_stack:
            raise BrainfuckUnbalancedBrackets("Brainfuck program ended while still in a loop.")
        return self.brainfuck_ops

    # @cached_property
    # def brainfuck_ops_with_context(self):
    #     ops_with_context = []
    #     loop_start_indices_stack = []
    #
    #     for i, op in enumerate(self.brainfuck_ops):
    #         if op == BrainfuckNonLoopOps.LoopStart:
    #             loop_start_indices_stack.append(i)
    #             ops_with_context.append(LoopOpWithContext(op, _UNDEFINED_INDEX))
    #
    #         elif op == BrainfuckNonLoopOps.LoopEnd:
    #             try:
    #                 start_index = loop_start_indices_stack.pop()
    #             except IndexError:
    #                 raise SyntaxError("Brainfuck loop closed ")
    #             ops_with_context[start_index].matching_op_index = i
    #             ops_with_context.append(LoopOpWithContext(op, start_index))
    #
    #         else:
    #             ops_with_context.append(op)
    #
    #     assert not loop_start_indices_stack, "Brainfuck program contains more ']' than '['"
    #     return ops_with_context

    def get_compiled_code(self) -> str:
        brainfuck_ops_with_context = self.get_brainfuck_ops()

        fj_code_lines = []
        for brainfuck_op in brainfuck_ops_with_context:
            fj_code_lines.append(str(brainfuck_op))
        fj_code__brainfuck_ops = '\n'.join(fj_code_lines)

        with open(FLIPJUMP_OUTPUT_FORMAT_FILE, 'r') as fj_format:
            generic_fj_code__without_brainfuck_ops = fj_format.read()

        return generic_fj_code__without_brainfuck_ops\
            .replace(COMPILED_BRAINFUCK_OPS_SPOT__FJ_FORMAT_CONST, fj_code__brainfuck_ops)\
            .replace(NUMBER_OF_BRAINFUCK_DATA_CELLS__FJ_FORMAT_CONST, str(self.number_of_brainfuck_cells))
