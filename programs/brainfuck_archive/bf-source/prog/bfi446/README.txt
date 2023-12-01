;;; bfi446.rbf - 446-byte brainf*ck interpreter
;
; Coding this raped the brain of
;    (C) Dean Scarff <p00ya AT users . sf dot net>
;    17 Aug 2003
; Licensed under the Academic Free License version 2.0
;
; Stripping this file:
;sed -e 's/;.*//' bfi446.rbf | tr -d '[:space:]' > bfi446.b
; Pre-processing your own code 'src.bf':
;cat src.bf | tr -d -c '+,.<>[]-' > src.b
; Example use with guest code file 'src.bf':
;cat src.bf | tr -d -c '+,.<>[]-' > src.b
;printf '\0input' | cat src.b - | bfi bfi446.b
; Use with manual code input:
;printf 'code\0input' | bfi bfi446.b
;
; Conditional on the use of a conformant host interpreter, bfi446 conforms to
; the 'non-existent' [BF1.3] with the following constraints:
; o  Pure, valid brainfuck code (no whitespace, no comments, no NULs).
;    Stripping as above is recommended.
; o  Code cannot start with a '[' (which is redundant anyway)
; o  If the host's tape-length L is finite, and N is the guest code size
;       Tape-length available = L/3 - N - 1
; o  The maximum nesting level of pretest loops is limited to the maximum
;    value of the implementation-defined integer.
;

;;; CODE:

; *** Pre: Fill up the code buffer ***
>,[; Read code until NUL
>>++++++[<+++++[<--->-]>-]; (6*5*-3) pre-reduce by 90
->,; flag walkers
]
<[+<<<]>; @ [c=1]

[; while ([c] != NULL)
[>+>+<<-]; mov [c] to [c+1] and [c+2]
->; flag [c] -1 unfinished
; * A.1: "[]" block
-[; not '['
--[; not ']'

; ** B.1: Execute "<>.-,+"
<+>; flag [c] finished
; * B.1.1: Move into place
[>>>>+<<<<-]; mov remnant [c+1] to [c+5]
>>[>>[>>>-<<<+]>]; @ {-3}, remnant in {-1}
>+
[>[>>>-<<<+]>>]; @ [d+1], remnant in [d+2]

; ** A.2: "<>" block
++++++[>+++++<-]->; 6*5, flag [d+1] = -1
+[; not '>'
++[; not '<'

; ** A.3: "+,-." block
<+++++++[>+++<-]->; (-1+7)*3, flag [d+1] = -1 (unfinished)

; * B.1.2: Execute
-[; not '+'
-[; not ','
-[; not '-', therefore '.'
-< +<.> >; flag fin, exec, break
]<[+<->]>; '-'
]<[+<,>]>; ','
]<[+<+>]>;  '+'
]<[+<<<+]>; '<' d-=3
]<[>>>]; '>' d+=3

-[+<<<-]; @ {-2}
<<<<[<<<]>; @ [c+1]

; ** B.2: ']'
]<[; ']'
++++>>---; [c] = ']', [c+3] = 0
<<<-[; c-=3, @ [c+2] stack counter
<<[<+>>+<-]; move [c] to [c-1] and [c+1]
>-[; not '['
--[; not ']'
>+<[+]
]>--<; ']'
]>+; '['

<<<[>+<-]>>>; move [c-1] back to [c]
[<<<->>>+]<<<; move stack counter back
]; [c+3] is matching bracket, @ [c+2]
<<[>>+<<-]; @ [c]
]>; end ']'

; ** B.3: '['
]<[+; '['
>>>[>>>]>; @ {-2}
+[>>>]-<; @ [d], [d+1] = -1
[; if [d]
>[+<<<-]<<<<[<<<]; @ [c]
]>[; else (@ [c+1] or [d+1])
[+<<<-]<<<<[<<<]+; @ [c] = '['
>>[; c+=3, @ [c-1] stack counter
[>>>+<<<-]; mov [c-1] to [c+2]
>[>-<<->+]; mov [c] to [c+1] and [c-1]
>-[; not '['
--[; not ']'
>+<[+]
]>--<; ']'
]>+; '['
<<<[>+<-]; mov [c-1] to [c]
>>>; @ [c+2]
]+++; [c] is matching bracket, @ [c+2] = 3
<]; end else, @ [c+1]
<[-]]; end '[', @ [c]

; * A.4: get ready for the next instruction
>>[<<+>>-]>; restore bk, c += 3
]

;;; APPENDIX A: Memory layout

; [0] 0                   _
; [1] 1st instruction     |
; [2] GP                  |
; [3] GP                  |
; [4] 2nd instruction     |
; ...                     :
; [c-1] stack|bk          |
; [c] current|fin|GP      |
; [c+1] operating copy    |      code
; [c+2] bk                |
; [c+3] next instruction  |
; [c+4]                   |
; [c+5] remnant           |
; ...                     :
; {-6} last instruction   |
; {-5} GP                 |
; {-4} GP                 |
; {-3} NOP                ¯
; {-2} 0|+1                      transistion
; {-1} remnant|true       _
; {0} 1st data cell       |
; {1} -1                  |
; {2}                     |
; {3} 2nd data cell       |
; ...                     :
; [d-2] -1                |
; [d-1]                   |      data
; [d] current data        |
; [d+1] 0|fin             |
; [d+2] remnant           |
; [d+3] data right        |
; [d+4] 0                 |
; ...                     V

;;; REFERENCES:
; [BF1.3]
;  "The BrainF*** Language Specification v1.3",
;   Esoteric Non-existent Standards Institute, 01 January 2002
