>>>>,(read n)<<+[-[>>+<<-]+++++[>+++++<-]>[<+++++>-]>]<<
  initialize memory like this:
  0 { 0 '}' } (n times) 0 pointer:'}'

[--.++<+<[<<]>[->.>]>]
  count a n plus one bit binary number which is stored in the bytes
  just before the '}' in the memory layout above (with LSB on the left)
  from 2^n to 2^(n plus one) printing on '{' at the beginnung of the
  loop; then in the first loop set the number to 2^n then clear all one
  digits from the end printing a '}' for each of them; incrementing the
  first zero digit found is done in the next loop iteration (using the
  same plus sign which set the number to 2^n)