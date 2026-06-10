from pathlib import Path

import pytest

from bf2fj import compile_brainfuck_file_to_flipjump_file
from bf2fj.bf2fj_compiler import Bf2FjCompiler, can_cover_256_loop
from tests.test_compile_run_all import run_fj_and_verify_expected_output


SET_DATA_0 = 'set_data 0'
LOOP_START_MACRO = 'loop_start'


def get_optimized_fj_ops(bf_code: str) -> str:
    """
    :param bf_code: a brainfuck code string.
    :return: The fj-ops body (macro calls) that the optimizing compiler generates for it.
    """
    compiler = Bf2FjCompiler(bf_code)
    compiler.parse_brainfuck_ops()
    compiler.optimize_ops()
    return compiler.get_fj_code_of_brainfuck_ops()


@pytest.mark.parametrize("odd_jump_value", [1, -1, 3, -3, 5, 7, 17, 255, -255, 257])
def test_can_cover_256_loop__odd_jumps_cover(odd_jump_value: int):
    assert can_cover_256_loop(odd_jump_value)


@pytest.mark.parametrize("even_jump_value", [0, 2, -2, 4, 6, -6, 8, 10, 12, 100, 128, 256])
def test_can_cover_256_loop__even_jumps_dont_cover(even_jump_value: int):
    assert not can_cover_256_loop(even_jump_value)


@pytest.mark.parametrize("zeroing_loop_code", ['[-]', '[+]', '[+++]', '[-----]', '[+-++-]'])
def test_optimize_zeroing_loop__odd_step_loops_become_set_data_0(zeroing_loop_code: str):
    fj_ops = get_optimized_fj_ops(zeroing_loop_code)
    assert SET_DATA_0 in fj_ops
    assert LOOP_START_MACRO not in fj_ops


def test_optimize_zeroing_loop__data_ops_before_the_loop_are_folded_into_it():
    fj_ops = get_optimized_fj_ops('+++[-]')
    assert SET_DATA_0 in fj_ops
    assert 'add_data' not in fj_ops


@pytest.mark.parametrize("non_zeroing_loop_code", ['[++]', '[--]', '[++++++]', '[+-]', '+[++++++]'])
def test_optimize_zeroing_loop__even_step_loops_are_preserved(non_zeroing_loop_code: str):
    """
    A loop that adds an even value can never reach 0 from an odd starting value (it's an infinite loop),
     so it must not be optimized into "*ptr = 0".
    """
    fj_ops = get_optimized_fj_ops(non_zeroing_loop_code)
    assert SET_DATA_0 not in fj_ops
    assert LOOP_START_MACRO in fj_ops


def test_optimize_zeroing_loop__loop_around_nonzero_set_is_preserved():
    """
    "[[-]+]" sets the data to 1 on every iteration, so it never terminates (for non-zero starting data).
     It must not be optimized into "*ptr = 0".
    """
    fj_ops = get_optimized_fj_ops('[[-]+]')
    assert 'set_data 1' in fj_ops
    assert LOOP_START_MACRO in fj_ops


def test_optimize_zeroing_loop__loop_around_zeroing_set_becomes_set_data_0():
    """
    "[[-]]" always terminates with data == 0, so the whole thing can be optimized into "*ptr = 0".
    """
    fj_ops = get_optimized_fj_ops('[[-]]')
    assert SET_DATA_0 in fj_ops
    assert LOOP_START_MACRO not in fj_ops


def compile_and_run_brainfuck_code(bf_code: str, expected_output: bytes, tmp_path: Path, *,
                                   apply_optimizations: bool = True) -> None:
    """
    Compile the given brainfuck code, run the compiled flipjump program, and verify its output.
    :param bf_code: a brainfuck code string.
    :param expected_output: the output the program is expected to print.
    :param tmp_path: pytest's temporary directory for this test.
    :param apply_optimizations: passed to the compiler.
    """
    brainfuck_path = tmp_path / 'program.b'
    flipjump_path = tmp_path / 'program.fj'
    brainfuck_path.write_text(bf_code)
    compile_brainfuck_file_to_flipjump_file(brainfuck_path, flipjump_path, apply_optimizations=apply_optimizations)
    run_fj_and_verify_expected_output(flipjump_path, b'', expected_output)


@pytest.mark.parametrize("apply_optimizations", [True, False], ids=['optimized', 'unoptimized'])
def test_run_compiled_loops__zeroing_loops_zero_the_data(tmp_path: Path, apply_optimizations: bool):
    compile_and_run_brainfuck_code('+++++[[-]]++.', b'\x02', tmp_path, apply_optimizations=apply_optimizations)
    compile_and_run_brainfuck_code('+++++[+++].', b'\x00', tmp_path, apply_optimizations=apply_optimizations)


@pytest.mark.parametrize("apply_optimizations", [True, False], ids=['optimized', 'unoptimized'])
def test_run_compiled_loops__terminating_even_step_loop_behaves_correctly(tmp_path: Path, apply_optimizations: bool):
    # The loop subtracts 2 from a starting value of 4, so it terminates at 0 (then the '-' makes it 255).
    compile_and_run_brainfuck_code('++++[--]-.', b'\xff', tmp_path, apply_optimizations=apply_optimizations)


def test_compile_brainfuck_file_with_high_byte_comments(tmp_path: Path):
    """
    Comments with non-ascii bytes shouldn't crash the compilation (on any platform / locale),
     should be preserved in the compiled file, and the compiled file should still be assembleable.
    """
    brainfuck_path = tmp_path / 'program.b'
    flipjump_path = tmp_path / 'program.fj'
    brainfuck_path.write_bytes(b'comment \x81\x9d\xff\n+++.')

    compile_brainfuck_file_to_flipjump_file(brainfuck_path, flipjump_path)

    compiled_code = flipjump_path.read_text(encoding='utf-8')
    assert 'comment \x81\x9d\xff' in compiled_code
    run_fj_and_verify_expected_output(flipjump_path, b'', b'\x03')
