CC = clang
CFLAGS = -Wall -pedantic -std=c99

SCHOOL_PYTHON_H_PATH = /usr/include/python3.7m
SCHOOL_PYTHON_LIB_PATH = /usr/lib/python3.7/config-3.7m-x86_64-linux-gnu
SCHOOL_PYTHON_LIB = python3.7m

all: libmol.so _molecule.so

libmol.so: mol.o
	$(CC) mol.o -shared -lm -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fpic -o mol.o

molecule_wrap.c molecule.py: molecule.i
	swig -python molecule.i

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -c molecule_wrap.c -fpic -I $(SCHOOL_PYTHON_H_PATH) -o molecule_wrap.o

_molecule.so: molecule_wrap.o
	$(CC) molecule_wrap.o -shared -L. -lmol -L$(SCHOOL_PYTHON_LIB_PATH) -l$(SCHOOL_PYTHON_LIB) -dynamiclib -o _molecule.so

clean:
	rm *.o *.so
