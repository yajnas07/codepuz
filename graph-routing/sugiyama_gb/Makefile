CXX      = g++
CXXFLAGS = -std=c++17 -O2
# Static runtime avoids picking up a mismatched libstdc++-6.dll from PATH
# (e.g. Git's mingw), which otherwise crashes on stream construction.
LDFLAGS  = -static-libstdc++ -static-libgcc

all: sugiyama_demo

sugiyama_demo: sugiyama_demo.cpp
	$(CXX) $(CXXFLAGS) sugiyama_demo.cpp -o sugiyama_demo $(LDFLAGS)


run: sugiyama_demo
	./sugiyama_demo


clean:
	rm -f sugiyama_demo  sugiyama_demo.exe  *.svg
