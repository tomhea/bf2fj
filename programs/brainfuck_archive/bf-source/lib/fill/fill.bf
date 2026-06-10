'DIM var(#)
'
'var     Placeholder for i/o:  This makes it possible for the compiler to
'        reference it just like any other variable
'x       temp: used to keep track of the value we are removing or adding
'_       used to keep track of where we are in the array
'*       unused
'
'DIM A(6)
'A(4)=7
'*Ax_0x_1x_2x_3x_4x_5x_6
'07000000000000000000000 the value 7 is stored here first
'07740000000000000000000 working with array element 4; copy the value 7 to x
'07750000000000000000000 add 1; it will take x plus 1 steps to get there
'======================= task: find array element 4
'07750740000000000000000 copy 7 to the next temp block; copy _ then minus 1
'57750740000000000000000 copy _ from last block to block before last
'57750740730000000000000 "
'57750750730000000000000 "
'57750750730720000000000 "
'57750750750720000000000 "
'57750750750720710000000 "
'57750750750750710000000 "
'57750750750750710700000 "
'57750750750750750700000 "
'======================= loop exhausted
'57750750750750757700000 copy 7 into array element 4
'======================= task: find our way back
'57750750750750747700000 subtract 1 from previous _ and go there
'57750750750730747700000 "
'57750750720730747700000 "
'57750710720730747700000 "
'57700710720730747700000 " we're home!

