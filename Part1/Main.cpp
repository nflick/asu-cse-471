// ASU CSE 471 Course Project
// Team HAL

// Main file for the Part 1 of the course project.
// Loads data into a graph structure, then performs
// a search on the data to determine the optimal choices
// for free marketing cards.

#include <iostream>
#include <fstream>
#include <stdexcept>
#include <unordered_map>

#include "Graph.h"
#include "State.h"

// Function Declarations
void loadEdgeFile(const char *pathname, Graph & graph);

int main(int argc, char *argv[])
{
	if (argc != 2) {
		std::cout << "Usage: " << argv[0] << " <EDGE FILE>\n";
		return 0;
	}

	try {

		Graph graph;
		loadEdgeFile(argv[1], graph);

		State *initial = new State(&graph);
		State *best = 0;
		for (State::SuccessorIterator iter = initial->successors(); iter.hasCurrent(); iter.next()) {
			if (!best) {
				best = iter.current();
			} else if (iter.current()->expectedAdopters() > best->expectedAdopters()) {
				delete best;
				best = iter.current();
			} else {
				delete iter.current();
			}
		}

		std::cout << "Best result after first timestep is achieved by picking person " <<
			best->receivedCard().back() << "\nresulting in " << best->expectedAdopters() << " expected adopters.\n";

		return 0;

	} catch (std::exception *e) {
		std::cout << "search: An exception occurred: " << e->what();
	}
}

void loadEdgeFile(const char *pathname, Graph & graph)
{
	std::ifstream file(pathname);
	std::unordered_map<int, Vertex> vertexMap;
	typedef std::unordered_map<int, Vertex>::iterator MapIterator;

	if (file.is_open()) {
		while (!file.eof()) {	// Checks for errors as well as end-of-file.
			int srcId, destId;
			file >> srcId >> destId;

			Vertex src;
			MapIterator srcIter = vertexMap.find(srcId);
			if (srcIter == vertexMap.end()) {
				src = boost::add_vertex(graph);
				graph[src].id = srcId;
				vertexMap.insert(std::pair<int, Vertex>(srcId, src));
			} else {
				src = srcIter->second;
			}

			Vertex dest;
			MapIterator destIter = vertexMap.find(destId);
			if (destIter == vertexMap.end()) {
				dest = boost::add_vertex(graph);
				graph[dest].id = destId;
				vertexMap.insert(std::pair<int, Vertex>(destId, dest));
			} else {
				dest = destIter->second;
			}

			boost::add_edge(src, dest, graph);
		}
	} else {
		throw new std::runtime_error("File could not be opened.\n");
	}
}