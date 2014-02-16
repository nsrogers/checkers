CC = g++ -Wall -g
ALLFILES = README.md checkers.py cpp_code.cc makefile \
	 		Export.hs HaPy_init.c HsklAI.hs .gitignore

all: cpp hskl
	@ printf "======================\nCompilation Successful\n======================\n"
	
hskl:
	ghc --make -no-hs-main -optl '-shared' HaPy_init.c -o hsklAI.so Export.hs

cpp:
	$(CC) -c -fpic cpp_code.cc #Compiling C++ AI code
	$(CC) -shared -o cpp_code.so cpp_code.o #Make shared library
	rm cpp_code.o #We dont need this
	
clean:
	rm *.*o *.hi Export_stub.h
	
ci:
	git add $(ALLFILES)
	git status