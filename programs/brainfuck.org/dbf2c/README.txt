a brainfuck-to-C translator

During the main processing period, the values are
0 0 0 '{' '1' 'w' 'e' '+' ';' '\n' 0 i 0 0 0 ...
where commands are read into spot i, changed into codes as follows:
[]<>+- ,.
123456 89
just to the left of i, and those codes used to choose which text to output.
