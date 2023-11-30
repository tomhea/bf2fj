>>,[>>,]<<
        create a fine interleaved array of the characters to be sorted
        0 0 c1 0 c2 ::: 0 *cn 0 0|
[
        loop while there are characters left
        0 x c1 x c2 ::: x *cn 0 0| (x = number of outer loops executed)
  [-<+<]>
        decrement all characters by one; increment every x by one
        0 *x' c1' x' c2' ::: x' cn' 0 0| (note that x' != 0)
  [
        now walk through the whole array
        0 *x' c1' ::: x' cn' 0 0|
    >[>>]<
        and search for characters which were just decremented to zero
        0 x' c1' ::: *x' 0 ::: x' cn' 0 0| or 0 x' c1' ::: x' cn' *0 0|
    [
        we found one
        0 x' c1' ::: *x' 0 ::: x' cn' 0 0|
      .[-]<[[>>+<<-]<]>>
        print x' (which is equal to the original character's value)
        then delete this x' and move everything in the left of the
        current pointer two to the right
        0 0 *0 x' c1' ::: x' c(n')' 0 0|
    ]
        0 0 *0 x' c1' ::: x' c(n')' 0 0| or 0 x' c1' ::: x' cn' *0 0|
    >
        check whether we've walked through the whole array or found a
        zero; scan the array for zeroes again in the latter case
        0 *x' c1' ::: x' c(n')' 0 0| or 0 x' c1' ::: x' cn' 0 *0| or 0 *0 0|
  ]
  <<
        align the pointer and check if there are characters left
        0 x' c1' x' c2' ::: x' *cn' 0 0|
]
