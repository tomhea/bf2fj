from definitions import *

from bf2fj_compiler import Bf2FjCompiler


BRAINFUCK_PROGRAM_PATH = BRAINFUCK_DIR / 'hello_world.bf'
FLIPJUMP_PROGRAM_PATH = FLIPJUMP_DIR / 'hello_world.fj'


FIXED_INPUT = b''
EXPECTED_OUTPUT = b'Hello World!\n'


def main():
    with open(BRAINFUCK_PROGRAM_PATH, 'r') as bf_file:
        compiler = Bf2FjCompiler(bf_file.read())

    with open(FLIPJUMP_PROGRAM_PATH, 'w') as fj_file:
        fj_file.write(compiler.get_compiled_code())


if __name__ == '__main__':
    main()
