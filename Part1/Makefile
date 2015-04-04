CXX=g++
CXXFLAGS=-std=c++11 -Wall

debug: Main.cpp State.cpp State.h Node.cpp Node.h Search.cpp Search.h
	$(CXX) $(CXXFLAGS) -g -o main Main.cpp State.cpp Node.cpp Search.cpp

optimized: Main.cpp State.cpp State.h Node.cpp Node.h Search.cpp Search.h
	$(CXX) $(CXXFLAGS) -O3 -flto -o main Main.cpp State.cpp Node.cpp Search.cpp

clean:
	- rm main