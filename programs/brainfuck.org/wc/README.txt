the standard (line and) word (and character) count utility

The format is
0 0 0 o 0 n i l t w t c t l t w t c t ... c t 0 0 0 ...
where o and n are the old and new whitespace flags; i is the character just
input; l, w, and c are decimal digits of the respective counts, least
significant to the left; and t are used as temporaries and otherwise set to 1
to mark the extent of the counts.
