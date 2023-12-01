import argparse
import os
from pathlib import Path
from typing import Tuple

from bf2fj.bf2fj_compiler import Bf2FjCompiler

from flipjump.utils.classes import PrintTimer
import flipjump


DEFAULT_FJM_WIDTH = 32
IO_BYTES_ENCODING = 'raw_unicode_escape'


# TODO (issue #3) in 'flipjump_output_format.fj':
#  dont hex.read_byte if ptr haven't changed yet (a flag on a pointer changed?)


def compile_brainfuck_file_to_flipjump_file(brainfuck_file_path: Path, flipjump_file_path: Path,
                                            apply_optimizations: bool = True) -> None:
    """
    Compile the given brainfuck file into a flip-jump file.
    :param brainfuck_file_path: The path to the input brainfuck file.
    :param flipjump_file_path: The result flip-jump file will be outputted to this path.
    :param apply_optimizations: If true, optimizes the generated code with some brainfuck-interpreter optimizations.
    """
    with open(brainfuck_file_path, 'r', encoding=IO_BYTES_ENCODING) as bf_file:
        bf_code = bf_file.read()

    compiler = Bf2FjCompiler(bf_code)
    with PrintTimer('  compile bf->fj:  '):
        fj_code = compiler.get_compiled_code(apply_optimizations=apply_optimizations)

    with open(flipjump_file_path, 'w') as fj_file:
        fj_file.write(fj_code)


def get_arguments() -> Tuple[Path, Path, bool, bool]:
    """
    :return: tuple of (input_brainfuck_path, output_flipjump_path, should_run_compiled_fj, apply_optimizations).
    :note: if the user haven't specified the output_path, it will be created in the same folder, with the ".fj" suffix.
    """
    parser = argparse.ArgumentParser(description='Compiles brainfuck programs to flipjump.')
    parser.add_argument("source", help="path to the brainfuck program", type=str)
    parser.add_argument("-o", "--output", default=None, type=str,
                        help="path to the compiled flipjump program. "
                             "if you don't specify it, the file will be created in the same directory")
    parser.add_argument("-r", "--run", action='store_true',
                        help="if specified - run the compiled flipjump file.")
    parser.add_argument("-d", "--disable-optimizations", action='store_true',
                        help="if specified - don't apply optimizations on the generated code.")
    args = parser.parse_args()

    input_path = Path(args.source)
    if not input_path.is_file():
        parser.error("source file must be a valid file.")

    if args.output is None:
        if input_path.suffix == '.fj':
            parser.error('If specify only the brainfuck source file, '
                         'you are not allowed to use the flipjump suffix ".fj".')
        output_path = input_path.with_suffix('.fj')
    else:
        output_path = Path(args.output)
        os.makedirs(output_path.parent, exist_ok=True)

    return input_path, output_path, args.run, not args.disable_optimizations


def assemble_and_run_fj(flipjump_path: Path, should_run_compiled_fj: bool):
    if should_run_compiled_fj:
        flipjump.assemble_and_run([flipjump_path])


def main() -> None:
    input_brainfuck_path, output_flipjump_path, should_run_compiled_fj, apply_optimizations = get_arguments()
    compile_brainfuck_file_to_flipjump_file(input_brainfuck_path, output_flipjump_path, apply_optimizations)
    assemble_and_run_fj(output_flipjump_path, should_run_compiled_fj)


if __name__ == '__main__':
    main()
