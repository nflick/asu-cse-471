CXX=g++
CXXFLAGS=-std=c++11 -Wall

debug: Main.cpp State.cpp State.h Node.cpp Node.h Uninformed.cpp Uninformed.h
	$(CXX) $(CXXFLAGS) -g -o main Main.cpp State.cpp Node.cpp Uninformed.cpp

clean:
	- rm main