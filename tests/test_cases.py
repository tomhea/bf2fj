from pathlib import Path


PROGRAMS_PATH = Path(__file__).parent.parent / "programs"

BRAINFUCK_ORG_PATH = PROGRAMS_PATH / 'brainfuck.org'
SIMPLE_PRINTS_PATH = PROGRAMS_PATH / 'simple_prints'
UMULLER_PATH = PROGRAMS_PATH / 'umueller-brainfuck'
FRANS_FAASE_PATH = PROGRAMS_PATH / 'frans_faase'


PROGRAM_DIRECTORIES = [
    SIMPLE_PRINTS_PATH / 'hello_world',  # 1 second
    SIMPLE_PRINTS_PATH / 'hello_100nops',  # 1 second

    FRANS_FAASE_PATH / '99_bottles',  # 50 seconds
    # FRANS_FAASE_PATH / 'BFinterpreter_fails',  # fails with EOF read.
    FRANS_FAASE_PATH / 'BFinterpreter_working',  # 4 seconds
    FRANS_FAASE_PATH / 'quine1',  # 15 seconds
    FRANS_FAASE_PATH / 'quine2',  # 50 seconds
    # FRANS_FAASE_PATH / 'quine  # takes a lot of time, haven't finished.

    # UMULLER_PATH / 'prime',  # returns bad credentials.

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
