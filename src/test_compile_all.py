from pathlib import Path
import pytest
from flipjump import assemble_and_run_test_output

from src.bf2fj import compile_brainfuck_file_to_flipjump_file


PROGRAMS_PATH = Path(__file__).parent.parent / "programs"

PROGRAM_DIRECTORIES = [
    PROGRAMS_PATH / 'hello_world',
    PROGRAMS_PATH / 'collatz',
    # PROGRAMS_PATH / 'bsort',
]

DEFAULT_FJM_WIDTH = 32
DEBUG_INFO_LENGTH = 1000

BRAINFUCK_FILE_EXTENSIONS = ['.b', '.bf']
FLIPJUMP_EXTENSION = '.fj'
INPUT_FILE_NAME = 'input'
OUTPUT_FILE_NAME = 'output'


def get_brainfuck_program_path(program_directory: Path) -> Path:
    extensions_found = []

    for file_extension in BRAINFUCK_FILE_EXTENSIONS:
        file_path = program_directory / f"{program_directory.name}{file_extension}"
        if file_path.exists():
            extensions_found.append(file_path)

    if not extensions_found:
        raise FileNotFoundError(f'No brainfuck file named "{program_directory.name}" with an extension of '
                                f'{BRAINFUCK_FILE_EXTENSIONS} was found in the next directory: '
                                f'{program_directory.absolute()}')
    if len(extensions_found) == 1:
        return extensions_found[0]

    raise FileExistsError(f'Found multiple files named "{program_directory.name}" with an extension of '
                          f'{BRAINFUCK_FILE_EXTENSIONS} in the next directory: '
                          f'{program_directory.absolute()}. You should only have one brainfuck file there.')


def compile_and_test_single_program(program_directory: Path) -> None:
    if not program_directory.is_dir() or not program_directory.exists():
        raise FileNotFoundError(f"Can't find the next directory: {program_directory.absolute()}")

    brainfuck_program_path = get_brainfuck_program_path(program_directory)
    fixed_input_path = program_directory / INPUT_FILE_NAME
    expected_output_path = program_directory / OUTPUT_FILE_NAME
    compiled_flipjump_path = program_directory / f"{program_directory.name}{FLIPJUMP_EXTENSION}"

    compile_brainfuck_file_to_flipjump_file(brainfuck_program_path, compiled_flipjump_path)
    with open(fixed_input_path, 'rb') as fixed_input_file, open(expected_output_path, 'rb') as expected_output_file:
        run_fj_and_verify_expected_output(compiled_flipjump_path, fixed_input_file.read(), expected_output_file.read())


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
                                 memory_width=DEFAULT_FJM_WIDTH, last_ops_debugging_list_length=DEBUG_INFO_LENGTH)


@pytest.mark.parametrize("program_directory", PROGRAM_DIRECTORIES)
def test_compile_bj__run_fj__verify_output(program_directory: Path):
    compile_and_test_single_program(program_directory)
