a universal Turing machine

Squares of the Turing machine's tape are laid out consecutively, with 0-5
representing symbols 01b<>c and a three-cell gap for the Turing machine's head;
the rightmost of the three holds the state (1-4 or 0 for "halt"). During input,
the head is always kept just right of the rightmost "b" found so far. During
processing, the new state, symbol, and direction are calculated from the old
using the layout:
tape tape nsym ndir (ost-1)*6+osym nst tape tape
