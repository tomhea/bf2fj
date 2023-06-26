from pathlib import Path

from definitions import BRAINFUCK_DIR, FLIPJUMP_DIR
from bf2fj_compiler import Bf2FjCompiler


BRAINFUCK_PROGRAM_PATH = BRAINFUCK_DIR / 'hello_world.bf'
FLIPJUMP_PROGRAM_PATH = FLIPJUMP_DIR / 'hello_world.fj'


FIXED_INPUT = b''
EXPECTED_OUTPUT = b'Hello World!\n'


def run_fj_and_verify_expected_output(flipjump_code_path: Path, fixed_input: bytes, expected_output: bytes) -> bool:
    pass


def main() -> None:
    with open(BRAINFUCK_PROGRAM_PATH, 'r') as bf_file:
        bf_code = bf_file.read()

    compiler = Bf2FjCompiler(bf_code)
    fj_code = compiler.get_compiled_code()

    with open(FLIPJUMP_PROGRAM_PATH, 'w') as fj_file:
        fj_file.write(fj_code)

    run_fj_and_verify_expected_output(FLIPJUMP_PROGRAM_PATH, FIXED_INPUT, EXPECTED_OUTPUT)


if __name__ == '__main__':
    main()
