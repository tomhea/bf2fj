memory: entries consisting of ( a b x y )
x = 1 when the entry is done
y = 1 for all living entries
entries done which are on the far left are disposed of by
marking them y = 0; when no more entry exists whose y == 1 then
the progam stops

leave y = 0
>
read until EOF leaving 0 1 between chars read:
,[>>>+>,]

(a 0 0 1) _0
<
while y
[
[
<
skip entries whose x = 1
[<<<<]
set y = 0 and move to a
>- <<<
_a b 0 0
[->+>]
_0 b 0 0 if a == 0
a' b'_0 0 if a != 0
>
0 _b 0 0 if a == 0
a' b' 0 _0 if a != 0
[.>+>]
0 b 1 _0 if a == 0 after having printed b
a' b' 0 _0 if a != 0
restore y = 1
+
move to next entry
<<<<
loop back
]
now y == 0
while x == 1 set y = 0
>>>[>->>>]>
while y move to next entry
[>>>>]
back to last entry whose y == 1 if any
<<<<
loop again except if no more valid entry
in latter case exit the loop and stop
]
