from pathlib import Path

from src.bf2fj_compiler import Bf2FjCompiler

from flipjump.utils.classes import PrintTimer


DEFAULT_FJM_WIDTH = 32


# TODO in 'flipjump_output_format.fj': dont hex.read_byte if ptr haven't changed yet (a flag on a pointer changed?)


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
    # TODO argparse that calls compile_brainfuck_file_to_flipjump_file()
    compile_brainfuck_file_to_flipjump_file(
        Path(input('Enter brainfuck program path: ')),
        Path(input('Enter output (flipjump) program path: ')),
    )


if __name__ == '__main__':
    main()
