a brainfuck interpreter

The brainfuck commands ][><.-,+ are stored as numbers 1-8 respectively. They
are laid out contiguously from the start of the array, except for a two-cell
gap just left of the next command to execute, which serves as instruction
pointer. The last instruction in the program is followed by two zeroes,
followed by the cells in the (simulated) array, each preceded by a 1 if the
(simulated) data pointer is at or to the right of that cell, and a 0 otherwise.
