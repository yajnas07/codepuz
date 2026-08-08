CXX      = g++
CXXFLAGS = -std=c++17 -O2
# Static runtime avoids picking up a mismatched libstdc++-6.dll from PATH
# (e.g. Git's mingw), which otherwise crashes on stream construction.
LDFLAGS  = -static-libstdc++ -static-libgcc

all: sugiyama_demo sugiyama_tests

sugiyama_demo: sugiyama_demo.cpp sugiyama.hpp
	$(CXX) $(CXXFLAGS) sugiyama_demo.cpp -o sugiyama_demo $(LDFLAGS)

sugiyama_tests: sugiyama_tests.cpp sugiyama.hpp
	$(CXX) $(CXXFLAGS) sugiyama_tests.cpp -o sugiyama_tests $(LDFLAGS)

run: sugiyama_demo
	./sugiyama_demo

test: sugiyama_tests
	./sugiyama_tests

clean:
	rm -f sugiyama_demo sugiyama_tests sugiyama_demo.exe sugiyama_tests.exe *.svg
