import shlex
from pathlib import Path

from flipjump.src.defs import PrintTimer
from flipjump.src.fj import assemble_run_according_to_cmd_line_args

from definitions import BRAINFUCK_DIR, FLIPJUMP_DIR
from bf2fj_compiler import Bf2FjCompiler


DEBUG_FLAGS = '-d --debug-ops-list 1000'
GENERAL_FLAGS = '-w 32'


BRAINFUCK_PROGRAM_PATH = BRAINFUCK_DIR / 'hello_world.bf'
FLIPJUMP_PROGRAM_PATH = FLIPJUMP_DIR / 'hello_world.fj'

FIXED_INPUT = b''
EXPECTED_OUTPUT = b'Hello World!\n'


def run_fj_and_verify_expected_output(flipjump_code_path: Path, fixed_input: bytes, expected_output: bytes) -> bool:
    assemble_run_according_to_cmd_line_args(cmd_line_args=shlex.split(
        f'"{flipjump_code_path}" {DEBUG_FLAGS} {GENERAL_FLAGS}'
    ))

    # TODO use fixed input as input, and assert that the output is exactly expected_output.
    #  Can be done by using  flipjump.src.assembler.assemble(..)  and  flipjump.src.fjm_run.run(..)  directly.
    return False


def main() -> None:
    with open(BRAINFUCK_PROGRAM_PATH, 'r') as bf_file:
        bf_code = bf_file.read()

    compiler = Bf2FjCompiler(bf_code)
    with PrintTimer('  compile bf->fj:  '):
        fj_code = compiler.get_compiled_code()

    with open(FLIPJUMP_PROGRAM_PATH, 'w') as fj_file:
        fj_file.write(fj_code)

    run_fj_and_verify_expected_output(FLIPJUMP_PROGRAM_PATH, FIXED_INPUT, EXPECTED_OUTPUT)


if __name__ == '__main__':
    main()
