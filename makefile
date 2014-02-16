CC = g++ -Wall -g
ALLFILES = README.md checkers.py cpp_code.cc makefile .gitignore

all:
	$(CC) -c -fpic cpp_code.cc #Compiling C++ AI code
	$(CC) -shared -o cpp_code.so cpp_code.o #Make shared library
	rm cpp_code.o #We dont need this
	
clean:
	rm *.*o
	
ci:
	git add $(ALLFILES)
	git status