from pathlib import Path
from tempfile import TemporaryDirectory

from definitions import BRAINFUCK_DIR, FLIPJUMP_DIR
from bf2fj_compiler import Bf2FjCompiler

from flipjump.debugging.breakpoints import BreakpointHandler, load_labels_dictionary
from flipjump.fj import get_file_tuples
from flipjump.interpretter import fjm_run
from flipjump.io_devices.FixedIO import FixedIO
from flipjump.utils.classes import TerminationCause, PrintTimer
from flipjump.assembler import assembler

from flipjump.fjm.fjm_consts import CompressedVersion
from flipjump.fjm.fjm_writer import Writer

fjm_width = 32

DEBUG_FLAGS: str = '-d --debug-ops-list 1000'
GENERAL_FLAGS: str = f'-w {fjm_width}'
DEBUG_INFO_LENGTH = 1000
EXPECTED_TERMINATION_CAUSE = TerminationCause.Looping

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
    
    with TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        fjm_file_path = tmp_dir_path / f'{flipjump_code_path.stem}.fjm'
        debugging_file_path = tmp_dir_path / f'{fjm_file_path.name}.fj_debugging_info'

        # assemble
        file_tuples = get_file_tuples([str(flipjump_code_path.absolute())], no_stl=False)
        fjm_writer = Writer(fjm_file_path, fjm_width, CompressedVersion)
        assembler.assemble(file_tuples, fjm_width, fjm_writer, debugging_file_path=debugging_file_path)

        io_device = FixedIO(fixed_input)
        label_to_address = load_labels_dictionary(debugging_file_path, True)
        breakpoint_handler = BreakpointHandler({}, {label_to_address[label]: label
                                               for label in tuple(label_to_address)[::-1]})

        termination_statistics = fjm_run.run(fjm_file_path,
                                             io_device=io_device,
                                             time_verbose=True,
                                             last_ops_debugging_list_length=DEBUG_INFO_LENGTH,
                                             breakpoint_handler=breakpoint_handler)

        termination_statistics.print(labels_handler=breakpoint_handler,
                                     output_to_print=io_device.get_output(allow_incomplete_output=True))
        assert termination_statistics.termination_cause == EXPECTED_TERMINATION_CAUSE
        assert expected_output == io_device.get_output()


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
