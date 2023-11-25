outputs the Thue-Morse sequence

The format is
0 0 p c n n ... n 0 0 ...
where n are bits of a binary number, least significant bit to left.
p is 1 for even parity or 2 for odd parity.
c is 48 for even parity and 49 for odd parity.
We output c, increment the number, and then update p and c.
