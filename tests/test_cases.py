from pathlib import Path


PROGRAMS_PATH = Path(__file__).parent.parent / "programs"

BRAINFUCK_ORG_PATH = PROGRAMS_PATH / 'brainfuck.org'
SIMPLE_PRINTS_PATH = PROGRAMS_PATH / 'simple_prints'
UMULLER_PATH = PROGRAMS_PATH / 'umueller-brainfuck'
FRANS_FAASE_PATH = PROGRAMS_PATH / 'frans_faase'
ARCHIVE_PATH = PROGRAMS_PATH / 'brainfuck_archive'
CODE_GOLF_TEXT = ARCHIVE_PATH / 'code_golf_text_to_bf_that_prints_it'
CODE_GOLF_SET = ARCHIVE_PATH / 'code_golf_set_theory_num_repr'
CODE_GOLF_SORT = ARCHIVE_PATH / 'code_golf_sort_bytes'


PROGRAM_DIRECTORIES = [
    SIMPLE_PRINTS_PATH / 'hello_world',  # 1 second
    SIMPLE_PRINTS_PATH / 'hello_100nops',  # 1 second

    FRANS_FAASE_PATH / '99_bottles',  # 50 seconds
    # FRANS_FAASE_PATH / 'BFinterpreter_fails',  # fails with EOF read.
    FRANS_FAASE_PATH / 'BFinterpreter_working',  # 4 seconds
    FRANS_FAASE_PATH / 'quine1',  # 15 seconds
    FRANS_FAASE_PATH / 'quine2',  # 50 seconds
    # FRANS_FAASE_PATH / 'quine3',  # takes a lot of time, haven't finished.

    # UMULLER_PATH / 'prime',  # returns bad credentials.

    ARCHIVE_PATH / 'text2bf',
    ARCHIVE_PATH / 'asciiart',

    CODE_GOLF_TEXT / 'cgolf_text_bf_1',
    CODE_GOLF_TEXT / 'cgolf_text_bf_2',
    CODE_GOLF_TEXT / 'cgolf_text_bf_3',
    CODE_GOLF_TEXT / 'cgolf_text_bf_4',
    CODE_GOLF_TEXT / 'cgolf_text_bf_5',
    CODE_GOLF_TEXT / 'cgolf_text_bf_6',
    CODE_GOLF_TEXT / 'cgolf_text_bf_7',
    CODE_GOLF_TEXT / 'cgolf_text_bf_8',

    # CODE_GOLF_SET / 'cgolf_num_set_repr_1',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_2',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_3',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_4',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_5',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_6',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_7',  # takes a lot of time, haven't finished.

    # about 4-7 seconds each:
    CODE_GOLF_SORT / 'cgolf_sort_1',
    CODE_GOLF_SORT / 'cgolf_sort_2',
    CODE_GOLF_SORT / 'cgolf_sort_3',
    CODE_GOLF_SORT / 'cgolf_sort_4',
    CODE_GOLF_SORT / 'cgolf_sort_5',
    CODE_GOLF_SORT / 'cgolf_sort_6',
    CODE_GOLF_SORT / 'cgolf_sort_7',
    CODE_GOLF_SORT / 'cgolf_sort_8',

    BRAINFUCK_ORG_PATH / 'bsort',  # 15 seconds
    BRAINFUCK_ORG_PATH / 'collatz',
    BRAINFUCK_ORG_PATH / 'dbf2c',
    BRAINFUCK_ORG_PATH / 'dbfi',
    BRAINFUCK_ORG_PATH / 'dvorak',
    BRAINFUCK_ORG_PATH / 'e',
    BRAINFUCK_ORG_PATH / 'factorial',
    BRAINFUCK_ORG_PATH / 'factorial2',
    BRAINFUCK_ORG_PATH / 'fib',
    BRAINFUCK_ORG_PATH / 'golden',
    BRAINFUCK_ORG_PATH / 'head',
    BRAINFUCK_ORG_PATH / 'impeccable',
    BRAINFUCK_ORG_PATH / 'isort',
    BRAINFUCK_ORG_PATH / 'jabh',
    BRAINFUCK_ORG_PATH / 'life',
    BRAINFUCK_ORG_PATH / 'numwarp',
    BRAINFUCK_ORG_PATH / 'qsort',
    BRAINFUCK_ORG_PATH / 'random',
    BRAINFUCK_ORG_PATH / 'rot13',
    BRAINFUCK_ORG_PATH / 'short',
    BRAINFUCK_ORG_PATH / 'sierpinski',
    BRAINFUCK_ORG_PATH / 'squares',
    BRAINFUCK_ORG_PATH / 'squares2',
    BRAINFUCK_ORG_PATH / 'thuemorse',
    BRAINFUCK_ORG_PATH / 'tictactoe',
    BRAINFUCK_ORG_PATH / 'utm',
    BRAINFUCK_ORG_PATH / 'wc',
    BRAINFUCK_ORG_PATH / 'xmastree',
]

PROGRAM_IDS = [path.name for path in PROGRAM_DIRECTORIES]
