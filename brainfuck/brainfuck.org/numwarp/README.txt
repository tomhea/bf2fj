a number...obfuscator? Prettifier? (sample output: https://brainfuck.org/numwarp.png)

Sample output:
    /\
    \/\
  /\ \/
  \/\
/\ \/
\/\
 \/

map of structure of the above output:
ssssccr
sss1cccr
ssbb1ccr
s1bbbr
aa1bbr
aaar
1aar

And as it's represented in memory, just before the output loop:
00aa1330aaa30bb1aa0bbb10cc1bb0ccc10333cc0000000n0000...
r's and s's are not represented directly in memory;
n contains the number of s's in the first line.
We have a series of frames, in reverse order of output, separated by zeroes.
1 represents space, 2 slash or backslash, 3 "no output" (used at ends).
