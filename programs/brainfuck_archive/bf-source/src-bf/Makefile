
# $Id: Makefile,v 1.5 2000/09/08 13:50:32 panu Exp $

CC = gcc
CFLAGS = -O3 -Wall

exec = 666 Ha_BF cat cat2 hello prime

all: $(exec)

%.c: %.b
	../bfc <$< >$@ 2>debug.log

clean:
	rm -f *.c *.o debug.log $(exec)

