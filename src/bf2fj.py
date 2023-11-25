from pathlib import Path

from flipjump import assemble_and_run_test_output

from definitions import BRAINFUCK_DIR, FLIPJUMP_DIR
from bf2fj_compiler import Bf2FjCompiler

from flipjump.utils.classes import PrintTimer


BRAINFUCK_FILE_EXTENSIONS = ['.b', '.bf']
FLIPJUMP_EXTENSION = '.fj'
INPUT_FILE_NAME = 'input'
OUTPUT_FILE_NAME = 'output'


fjm_width = 32
DEBUG_INFO_LENGTH = 1000


HELLO_WORLD_DIRECTORY = Path('./brainfuck/hello_world')

# BRAINFUCK_PROGRAM_PATH: Path = BRAINFUCK_DIR / 'hello_world.bf'
# FLIPJUMP_PROGRAM_PATH: Path = FLIPJUMP_DIR / 'hello_world.fj'
#
# FIXED_INPUT: bytes = b''
# EXPECTED_OUTPUT: bytes = b'Hello World!\n'


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
                                 memory_width=fjm_width, last_ops_debugging_list_length=DEBUG_INFO_LENGTH)


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


def main() -> None:
    compile_and_test_single_program(HELLO_WORLD_DIRECTORY)


if __name__ == '__main__':
    main()
