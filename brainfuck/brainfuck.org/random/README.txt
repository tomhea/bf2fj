a random number generator BASED ON** a cellular automaton

The basic format is
r 0 a t a t ... a t 0 0 0 0 ...
where r holds the random bits accumulated so far, a are states of cells of the
automaton (the leftmost a also tells how many bits are still required to
complete the next byte), and t are temporaries as in fib.b, except that the
middle one holds a 2; we have to mark it because successive values of the
middle cell are used as the "random" bit stream.


**
[The "random" number generator used is derived from the Rule 30 cellular
automaton; this is a one-dimensional, two-state automaton whose rules are:
111 110 101 100 011 010 001 000
 0   0   0   1   1   1   1   0
(00011110 is binary for decimal 30, hence the name.)
The initial condition is an infinite row of 0s with a single 1 in the
middle; from there it grows outward in both directions at a rate of one cell
per step, since 001 and 100 both produce 1. The "random" sequence of bits is
taken from the middle cell; they are gathered into bytes and output.

Now. Since a finite portion of the field is nonzero at any given time, it can
be stored in a finite amount of memory at any given time. But that portion
grows both left and right, whereas the brainfuck memory only extends to the
right from the pointer's initial position. The solution is to replace the Rule
30 automaton with the almost identical one
111 110 101 100 011 010 001 000
  0   0   0   1   1   1   1   0
which grows only to the right, at the rate of two cells per step.

The bits must be gathered in groups of eight to make bytes. So we need a place
to gather them, and also a bit counter. These go at left because the array of
cells has to grow to the right. We can update the cells in place, without using
another temporary array, since each depends only on its previous value and
those of cells to the left; we just update right-to-left. However, we need to
mark the extent of the array used, and its middle cell since that's where we
get the "random" bits. We'll follow every represented cell of the automaton
with a marker byte, holding a 1 to mark it as a cell of the automaton, or a 2
if it's the middle cell. It turns out we can also use the leftmost nonzero cell
of the automaton to store the count of how many bits still need gathering to
make a "random" byte. So the overall memory picture is: The accumulated
"random" bits are moved back and forth between byte 0 and byte 1. After n steps
of the automaton, bytes 2, 4, ..., 4n+2 hold values of cells of the automaton,
with byte 2 holding the bit counter; and bytes 3, 5, ..., 4n+3 hold markers,
all set to 1 except byte 2n+3 which holds 2. It's most convenient to extract
the "random" bit from the center cell immediately before updating it, and to
move the middle-cell marker at the same time.

One more innovation: the eight rules above end up meaning that the value of a
cell in the automaton is equal to
(previous value of that cell OR previous value of cell 1 to left)
    XOR previous value of cell 2 to left
and it turns out to be most efficient, rather than gathering all the causes of
the new value at once, to process all the effects of the old value at
once--that is, for each OLD cell, leave its value alone; and if its value is
one, set the cell 1 to the right to 1, and invert the cell 2 to the right.
Since we travel right-to-left, this still results in things being done in the
right order; each new value is derived by taking the old value, then oring it
with its left neighbor when that's processed, then xoring it with the cell 2 to
the left when THAT's processed.

Now, the actual code:]

>>>++
set first (and currently only and therefore central) marker to 2

[
start a loop which makes and outputs one byte each time through

    <++++++++
    set first cell (and bit counter) to 8 (nonzero)

    [
    start a loop which gets one bit (processes one step) each time through

        <[<++>-]
        move accumulated "random" bits from byte 1 to byte 0
        and double at the same time to bitshift left to make room for new bit
        (which is the reason for moving them in the first place)

        >>[>>]
        go to right end

        +>>+
        make two new markers for two new cells with initial values of 0

        [
        start a loop processing one cell of the automaton each time through

            -[
            start a loop which is entered if the current cell is the middle

                ->>+
                move the middle cell marker one cell right

                <<<[<[<<]<+>]>[>[>>]]
                add 1 to "random" bits in byte 0 if current cell has a 1
                (compare the movement in both cases)

            ]
            wrap up bit extraction loop; this marker cell is 0 now either way

            <[>>[-]]
            if the current cell has a 1 move to next cell right and clear it

            >[>[-<<]>[<+<]]
            in which case we'll enter this loop (since the marker of the cell
            1 to the right is nonzero); this loop has the net effect of
            setting the next cell to the right and inverting the second cell
            to the right (compare the movement in both cases)

            +<<
            set marker and go left to next marker to process that cell

        ]
        finish cell processing loop; we're at byte 1

        <[>+<-]
        move accumulated "random" bits from byte 0 to byte 1
        
        >>-
        go to first cell (and bit counter) and subtract 1
    ]
    wrap up bit getting (step processing) loop

    <.[-]>>
    output "random" byte at byte 1 and clear it and go to first marker again

]
wrap up byte gathering and outputting loop (program doesn't terminate)

Of course the whole thing looks tidier without so many comments:

>>>++[
    <++++++++[
        <[<++>-]>>[>>]+>>+[
            -[->>+<<<[<[<<]<+>]>[>[>>]]]
            <[>>[-]]>[>[-<<]>[<+<]]+<<
        ]<[>+<-]>>-
    ]<.[-]>>
]
"Random" byte generator using the Rule 30 automaton.
Doesn't terminate; you will have to kill it.
To get x bytes you need 32x+4 cells.
Turn off any newline translation!
Daniel B Cristofani (cristofdathevanetdotcom)
http://www.hevanet.com/cristofd/brainfuck/
