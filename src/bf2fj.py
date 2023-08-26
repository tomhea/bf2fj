import argparse
import shlex
from pathlib import Path
from tempfile import TemporaryDirectory

from flipjump.src import fjm, assembler, fjm_run
from flipjump.src.defs import PrintTimer
from flipjump.src.fj import assemble_run_according_to_cmd_line_args, get_file_tuples

from definitions import BRAINFUCK_DIR, FLIPJUMP_DIR
from bf2fj_compiler import Bf2FjCompiler
from flipjump.tests.test_fj import test_run, RunTestArgs, CSV_TRUE, DEBUGGING_FILE_SUFFIX

fjm_width = 32

DEBUG_FLAGS: str = '-d --debug-ops-list 1000'
GENERAL_FLAGS: str = f'-w {fjm_width}'


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
    
    with TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        fjm_file_path = tmp_dir_path / f'{flipjump_code_path.stem}.fjm'
        debugging_file_path = tmp_dir_path / f'{fjm_file_path.name}{DEBUGGING_FILE_SUFFIX}'
        in_file_path = tmp_dir_path / f'fixed_input.txt'
        out_file_path = tmp_dir_path / f'expected_output.txt'

        with open(in_file_path, 'wb') as in_file:
            in_file.write(fixed_input)
        with open(out_file_path, 'wb') as out_file:
            out_file.write(expected_output)

        file_tuples = get_file_tuples(argparse.Namespace(no_stl=False, files=[flipjump_code_path]))

        fjm_writer = fjm.Writer(fjm_file_path, fjm_width, fjm.RelativeJumpVersion)   # TODO use compressed when available
        assembler.assemble(file_tuples, fjm_width, fjm_writer,
                           debugging_file_path=debugging_file_path)

        try:
            test_run(RunTestArgs(
                save_debug_file=True, debug_info_length=100, test_name=flipjump_code_path.stem,
                fjm_path=str(fjm_file_path.absolute()),
                in_file_path=str(in_file_path.absolute()), out_file_path=str(out_file_path.absolute()),
                read_in_as_binary__str=CSV_TRUE, read_out_as_binary__str=CSV_TRUE))
            return True
        except AssertionError as e:
            print(e)
            return False

    # assemble_run_according_to_cmd_line_args(cmd_line_args=shlex.split(
    #     f'"{flipjump_code_path}" {DEBUG_FLAGS} {GENERAL_FLAGS} -o "{flipjump_code_path}m" -v 0'
    # ))


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
