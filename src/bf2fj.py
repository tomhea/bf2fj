import shlex
from pathlib import Path

from flipjump.src.defs import PrintTimer
from flipjump.src.fj import assemble_run_according_to_cmd_line_args

from definitions import BRAINFUCK_DIR, FLIPJUMP_DIR
from bf2fj_compiler import Bf2FjCompiler


DEBUG_FLAGS: str = '-d --debug-ops-list 1000'
GENERAL_FLAGS: str = '-w 32'


BRAINFUCK_PROGRAM_PATH: Path = BRAINFUCK_DIR / 'hello_world.bf'
FLIPJUMP_PROGRAM_PATH: Path = FLIPJUMP_DIR / 'hello_world.fj'

FIXED_INPUT: bytes = b''
EXPECTED_OUTPUT: bytes = b'Hello World!\n'


def run_fj_and_verify_expected_output(flipjump_code_path: Path, fixed_input: bytes, expected_output: bytes) -> bool:
    """
    Run the given flip-jump program, give it the fixed-input, and check if the output is as expected.
    :param flipjump_code_path: A path to a (non-compiled) flip-jump code file.
    :param fixed_input: This will be the input to the fj-code-file.
    :param expected_output: The expected output the fj-code-file would output given the fixed_input input.
    :return: True if the file's output matched the expected-output, while the input was fixed-input.
    """
    assemble_run_according_to_cmd_line_args(cmd_line_args=shlex.split(
        f'"{flipjump_code_path}" {DEBUG_FLAGS} {GENERAL_FLAGS} -o "{flipjump_code_path}m" -v 0'
    ))

    # TODO use fixed input as input, and assert that the output is exactly expected_output.
    #  Can be done by using  flipjump.src.assembler.assemble(..)  and  flipjump.src.fjm_run.run(..)  directly.
    return False


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
