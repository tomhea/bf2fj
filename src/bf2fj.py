from pathlib import Path

from flipjump import assemble_and_run_test_output

from definitions import BRAINFUCK_DIR, FLIPJUMP_DIR
from bf2fj_compiler import Bf2FjCompiler

from flipjump.utils.classes import PrintTimer


fjm_width = 32
DEBUG_INFO_LENGTH = 1000

BRAINFUCK_PROGRAM_PATH: Path = BRAINFUCK_DIR / 'hello_world.bf'
FLIPJUMP_PROGRAM_PATH: Path = FLIPJUMP_DIR / 'hello_world.fj'

FIXED_INPUT: bytes = b''
EXPECTED_OUTPUT: bytes = b'Hello World!\n'


def run_fj_and_verify_expected_output(flipjump_code_path: Path, fixed_input: bytes, expected_output: bytes) -> None:
    """
    Run the given flip-jump program, give it the fixed-input, and check if the output is as expected.
    :param flipjump_code_path: A path to a (non-compiled) flip-jump code file.
    :param fixed_input: This will be the input to the fj-code-file.
    :param expected_output: The expected output the fj-code-file should output given the fixed_input input.
    :raise AssertionError: if running the code generates different output then the expected-output.
    """
    assemble_and_run_test_output([flipjump_code_path], fixed_input, expected_output,
                                 should_raise_assertion_error=True,
                                 w=fjm_width, last_ops_debugging_list_length=DEBUG_INFO_LENGTH)


def compile_brainfuck_file_to_flipjump_file(brainfuck_file_path: Path, flipjump_file_path: Path) -> None:
    """
    Compile the given brainfuck file into a flip-jump file.
    :param brainfuck_file_path: The path to the input brainfuck file.
    :param flipjump_file_path: The result flip-jump file will be outputted to this path.
    """
    with open(brainfuck_file_path, 'r') as bf_file:
        bf_code = bf_file.read()

    compiler = Bf2FjCompiler(bf_code)
    with PrintTimer('  compile bf->fj:  '):
        fj_code = compiler.get_compiled_code()

    with open(flipjump_file_path, 'w') as fj_file:
        fj_file.write(fj_code)


def main() -> None:
    compile_brainfuck_file_to_flipjump_file(BRAINFUCK_PROGRAM_PATH, FLIPJUMP_PROGRAM_PATH)
    run_fj_and_verify_expected_output(FLIPJUMP_PROGRAM_PATH, FIXED_INPUT, EXPECTED_OUTPUT)


if __name__ == '__main__':
    main()
