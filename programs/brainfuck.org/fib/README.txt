outputs arbitrarily many Fibonacci numbers

The format is
0 10 a t b a t b ... a t b 0 0 0 0 0 ...
where a and b are (decimal) digits of the two Fibonacci numbers most recently
calculated, stored with the most significant digit to the right, and t are
temporaries which are nonzero when not in use, to mark how far b extends to the
right. The 10 is just used to output a linefeed.
