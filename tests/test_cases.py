from pathlib import Path


PROGRAMS_NAME = 'programs'
PROGRAMS_PATH = Path(__file__).parent.parent / PROGRAMS_NAME

BRAINFUCK_ORG_PATH = PROGRAMS_PATH / 'brainfuck.org'
SIMPLE_PRINTS_PATH = PROGRAMS_PATH / 'simple_prints'
UMULLER_PATH = PROGRAMS_PATH / 'umueller-brainfuck'
FRANS_FAASE_PATH = PROGRAMS_PATH / 'frans_faase'
ARCHIVE_PATH = PROGRAMS_PATH / 'brainfuck_archive'
ARCHIVE_CODE_GOLF_TEXT = ARCHIVE_PATH / 'code_golf_text_to_bf_that_prints_it'
ARCHIVE_CODE_GOLF_SET = ARCHIVE_PATH / 'code_golf_set_theory_num_repr'
ARCHIVE_CODE_GOLF_SORT = ARCHIVE_PATH / 'code_golf_sort_bytes'
ARCHIVE_SRC = ARCHIVE_PATH / 'bf-source'
ARCHIVE_QUINE = ARCHIVE_SRC / 'quine'
ARCHIVE_INNER_SRC = ARCHIVE_SRC / 'src-bf'
ARCHIVE_PROG = ARCHIVE_SRC / 'prog'
ARCHIVE_LIB = ARCHIVE_SRC / 'lib'
ARCHIVE_BERTRAM_QUINE = ARCHIVE_QUINE / 'BertramFelgenhauer'
LINUSAKESSON_PATH = PROGRAMS_PATH / 'linusakesson'


ARCHIVE_QUINE_DIRS = [
    # ARCHIVE_BERTRAM_QUINE / 't',   # 40 seconds
    # ARCHIVE_BERTRAM_QUINE / 'u',   # 50 seconds
    # ARCHIVE_BERTRAM_QUINE / 'v',   # 50 seconds
    # ARCHIVE_BERTRAM_QUINE / 'x',   # 50 seconds
    # ARCHIVE_BERTRAM_QUINE / 'y',   # 50 seconds
    # ARCHIVE_BERTRAM_QUINE / 'z',   # 27 seconds
    # ARCHIVE_BERTRAM_QUINE / 'z2',  # 22 seconds
    # ARCHIVE_BERTRAM_QUINE / 'z3',  # 21 seconds
    # ARCHIVE_BERTRAM_QUINE / 'z4',  # 3 minutes
    # ARCHIVE_BERTRAM_QUINE / 'z5',  # 4 minutes
    # ARCHIVE_BERTRAM_QUINE / 'z6',  # 25 seconds
    # ARCHIVE_BERTRAM_QUINE / 'z7',  # 5 minutes
    # ARCHIVE_BERTRAM_QUINE / 'z8',  # 9 minutes
    # ARCHIVE_BERTRAM_QUINE / 'z9',  # took a lot of time, hasn't finished
    # ARCHIVE_BERTRAM_QUINE / 'z9a',

    ARCHIVE_QUINE / 'dquine',
    ARCHIVE_QUINE / 'quine-bock',
    ARCHIVE_QUINE / 'quine410',
    ARCHIVE_QUINE / 'quine414',
    ARCHIVE_QUINE / 'quinebf',
    ARCHIVE_QUINE / 'QUINEBF1',
    ARCHIVE_QUINE / 'QUINEBF3',
    ARCHIVE_QUINE / 'ryanquine',
    ARCHIVE_QUINE / 'selfmodquine',
    ARCHIVE_QUINE / 'selfportrait',
]

SIMPLE_PRINTS_DIRS = [
    SIMPLE_PRINTS_PATH / 'hello_world',  # 1 second
    SIMPLE_PRINTS_PATH / 'hello_100nops',  # 1 second
]

FRANS_FAASE_DIRS = [
    FRANS_FAASE_PATH / '99_bottles',  # 50 seconds
    # FRANS_FAASE_PATH / 'BFinterpreter_fails',  # fails with EOF read.
    FRANS_FAASE_PATH / 'BFinterpreter_working',  # 4 seconds
    FRANS_FAASE_PATH / 'quine1',  # 15 seconds
    FRANS_FAASE_PATH / 'quine2',  # 50 seconds
    # FRANS_FAASE_PATH / 'quine3',  # takes a lot of time, haven't finished.
]

ARCHIVE_CODE_GOLF_DIRS = [
    ARCHIVE_CODE_GOLF_TEXT / 'cgolf_text_bf_1',
    ARCHIVE_CODE_GOLF_TEXT / 'cgolf_text_bf_2',
    ARCHIVE_CODE_GOLF_TEXT / 'cgolf_text_bf_3',
    ARCHIVE_CODE_GOLF_TEXT / 'cgolf_text_bf_4',
    ARCHIVE_CODE_GOLF_TEXT / 'cgolf_text_bf_5',
    ARCHIVE_CODE_GOLF_TEXT / 'cgolf_text_bf_6',
    ARCHIVE_CODE_GOLF_TEXT / 'cgolf_text_bf_7',
    ARCHIVE_CODE_GOLF_TEXT / 'cgolf_text_bf_8',

    # CODE_GOLF_SET / 'cgolf_num_set_repr_1',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_2',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_3',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_4',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_5',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_6',  # takes a lot of time, haven't finished.
    # CODE_GOLF_SET / 'cgolf_num_set_repr_7',  # takes a lot of time, haven't finished.

    # about 4-7 seconds each:
    ARCHIVE_CODE_GOLF_SORT / 'cgolf_sort_1',
    ARCHIVE_CODE_GOLF_SORT / 'cgolf_sort_2',
    ARCHIVE_CODE_GOLF_SORT / 'cgolf_sort_3',
    ARCHIVE_CODE_GOLF_SORT / 'cgolf_sort_4',
    ARCHIVE_CODE_GOLF_SORT / 'cgolf_sort_5',
    ARCHIVE_CODE_GOLF_SORT / 'cgolf_sort_6',
    ARCHIVE_CODE_GOLF_SORT / 'cgolf_sort_7',
    ARCHIVE_CODE_GOLF_SORT / 'cgolf_sort_8',
]

ARCHIVE_GENERAL = [
    ARCHIVE_PATH / 'text2bf',
    ARCHIVE_PATH / 'asciiart',
]

BRAINFUCK_ORG_DIRS = [
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
    BRAINFUCK_ORG_PATH / 'sierpinski',
    BRAINFUCK_ORG_PATH / 'squares',
    BRAINFUCK_ORG_PATH / 'squares2',
    BRAINFUCK_ORG_PATH / 'thuemorse',
    BRAINFUCK_ORG_PATH / 'tictactoe',
    BRAINFUCK_ORG_PATH / 'utm',
    BRAINFUCK_ORG_PATH / 'wc',
    BRAINFUCK_ORG_PATH / 'xmastree',
]

ARCHIVE_INNER_SRC_DIR = [
    ARCHIVE_INNER_SRC / '666',
    ARCHIVE_INNER_SRC / 'cat',
    ARCHIVE_INNER_SRC / 'cat2',
    ARCHIVE_INNER_SRC / 'hello',
    ARCHIVE_INNER_SRC / 'mul',
    ARCHIVE_INNER_SRC / 'mul10',
    ARCHIVE_INNER_SRC / 'prime',
    ARCHIVE_INNER_SRC / 'rev',
    ARCHIVE_INNER_SRC / 'varia',
]

ARCHIVE_PROG_DIR = [
    ARCHIVE_PROG / '196-commented',
    ARCHIVE_PROG / '2d_table',
    ARCHIVE_PROG / '99botles',
    ARCHIVE_PROG / 'another_rot13',
    ARCHIVE_PROG / 'ATOI',
    ARCHIVE_PROG / 'beer',
    ARCHIVE_PROG / 'bertram-rot13',
    ARCHIVE_PROG / 'bertram-sort',
    ARCHIVE_PROG / 'BFC',
    ARCHIVE_PROG / 'bfcl',
    ARCHIVE_PROG / 'BFI',
    ARCHIVE_PROG / 'bfi446',
    ARCHIVE_PROG / 'bfide_hello',
    ARCHIVE_PROG / 'bfide_packbits',
    ARCHIVE_PROG / 'bfide_power',
    ARCHIVE_PROG / 'bockbeer',
    ARCHIVE_PROG / 'BOTTLES',
    ARCHIVE_PROG / 'char',
    ARCHIVE_PROG / 'collatz',
    ARCHIVE_PROG / 'css-brainfuck',
    ARCHIVE_PROG / 'dbf2c',
    ARCHIVE_PROG / 'dbfi',
    ARCHIVE_PROG / 'decss',
    ARCHIVE_PROG / 'dquine',
    ARCHIVE_PROG / 'dvorak',
    ARCHIVE_PROG / 'ECHO2',
    ARCHIVE_PROG / 'factor',
    ARCHIVE_PROG / 'fib',
    ARCHIVE_PROG / 'fibo7',
    ARCHIVE_PROG / 'fibonacci',
    ARCHIVE_PROG / 'gameoflife',
    ARCHIVE_PROG / 'hanoi',
    ARCHIVE_PROG / 'hello3',
    ARCHIVE_PROG / 'HELLOBF',
    ARCHIVE_PROG / 'HELLOBF2',
    ARCHIVE_PROG / 'hellom',
    ARCHIVE_PROG / 'HELLOUM',
    ARCHIVE_PROG / 'helloyou',
    ARCHIVE_PROG / 'hello_world',
    ARCHIVE_PROG / 'htmlconv',
    ARCHIVE_PROG / 'jabh',
    ARCHIVE_PROG / 'mandelbrot',
    ARCHIVE_PROG / 'numwarp',
    ARCHIVE_PROG / 'oobrain',
    ARCHIVE_PROG / 'PI16',
    ARCHIVE_PROG / 'quine505',
    ARCHIVE_PROG / 'quinetail505',
    ARCHIVE_PROG / 'random',
    ARCHIVE_PROG / 'rot13',
    ARCHIVE_PROG / 'rpn',
    ARCHIVE_PROG / 'ryan-beer',
    ARCHIVE_PROG / 'SORT',
    ARCHIVE_PROG / 'triangle',
    ARCHIVE_PROG / 'utm',
    ARCHIVE_PROG / 'wc',
    ARCHIVE_PROG / 'yapi',
]

ARCHIVE_LIB_DIR = [
    ARCHIVE_LIB / 'ARRAY',
    ARCHIVE_LIB / 'ATOI',
    ARCHIVE_LIB / 'DIV10',
    ARCHIVE_LIB / 'ECHO4',
    ARCHIVE_LIB / 'fill',
    ARCHIVE_LIB / 'input',
    ARCHIVE_LIB / 'loop',
    ARCHIVE_LIB / 'MUL10',
    ARCHIVE_LIB / 'slurp',
    ARCHIVE_LIB / 'UMHELLO',
    ARCHIVE_LIB / 'VARIA',
]

LINUSAKESSON_DIR = [
    LINUSAKESSON_PATH / 'game_of_life',
    LINUSAKESSON_PATH / 'quine',
]


PROGRAM_DIRECTORIES = (
    ARCHIVE_QUINE_DIRS +
    SIMPLE_PRINTS_DIRS +
    FRANS_FAASE_DIRS +
    ARCHIVE_CODE_GOLF_DIRS +
    ARCHIVE_GENERAL +
    BRAINFUCK_ORG_DIRS +
    ARCHIVE_INNER_SRC_DIR +
    ARCHIVE_PROG_DIR +
    ARCHIVE_LIB_DIR +
    LINUSAKESSON_DIR
)

PROGRAM_IDS = [path.as_posix().split(PROGRAMS_NAME, 1)[1] for path in PROGRAM_DIRECTORIES]
