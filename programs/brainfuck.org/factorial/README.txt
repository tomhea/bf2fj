Calculated factorials (a much faster version is factorial2)

The format at the start of the main loop is normally
0 10 0 0 n t o c b n t o c b... 
where b is the number whose factorial was output last, stored in binary, least
significant digit to the left, using the values 2 and 1 in place of 1 and 0; c
is where that number will be copied to, only using 1 and 0; o holds decimal
digits of the last factorial output, t are temps that are nonzero as far as
n has been set, and n is where the next factorial will be accumulated.
