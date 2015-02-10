// ASU CSE 471 Course Project
// Team HAL

// Main file for the Part 1 of the course project.
// Loads data into a graph structure, then performs
// a search on the data to determine the optimal choices
// for free marketing cards.

#include <iostream>
#include <fstream>
#include <stdexcept>

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

	if (file.is_open()) {
		while (!file.eof()) {	// Checks for errors as well as end-of-file.
			int src, dest;
			file >> src >> dest;

			boost::add_vertex(src, graph);
			graph[src].id = src;
			boost::add_vertex(dest, graph);
			graph[dest].id = dest;

			boost::add_edge_by_label(src, dest, graph);
		}
	} else {
		throw new std::runtime_error("File could not be opened.\n");
	}
}