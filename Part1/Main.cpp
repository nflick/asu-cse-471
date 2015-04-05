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
#include <algorithm>
#include <string>

#include "Graph.h"
#include "State.h"
#include "Search.h"

// Function Declarations
void loadEdgeFile(const char *pathname, Graph & graph);
void printGraphStats(Graph & graph);

const int MAX_DEPTH = 2;

int main(int argc, char *argv[])
{
	if (argc != 4) {
		std::cout << "Usage: " << argv[0] << " <ALGORITHM> <DEPTH> <EDGE FILE>\n" <<
			"\twhere ALGORITHM is one of 'uniform', 'exhaustive', or 'A-star'\n";
		return 0;
	}

	try {
		std::string algorithm(argv[1]);
		int depth = std::stoi(std::string(argv[2]));
		Graph graph;
		loadEdgeFile(argv[3], graph);
		State initialState(&graph, depth);
		State *solution = 0;

		if (algorithm == "uniform") {
			std::cout << "Running uniform cost search.\n";
			solution = uniformCostSearch(&initialState);
		} else if (algorithm == "exhaustive") {
			std::cout << "Running exhaustive search.\n";
			solution = exhaustiveSearch(&initialState);
		} else if (algorithm == "A-star") {
			std::cout << "Running A-star search.\n";
			solution = astar(&initialState);
		} else {
			std::cout << "Unknown algorithm.\n";
			return 1;
		}

		solution->print(std::cout);
		
		//for (State::SuccessorIterator iter = initialState.successors(); iter.hasCurrent(); iter.next()) {
		//	State *current = iter.current();
		//	current->print(std::cout);
		//	std::cout << "Heuristic non-adopters: " << current->heuristicNonAdopters() << "\n\n";
		//}


		//std::cout << "heuristicNonAdopters: " << initialState.heuristicNonAdopters() << "\n";
		//std::cout << "nonAdopters: " << initialState.nonAdopters() << "\n";
		//solution->print(std::cout);
		//std::cout << "heuristicNonAdopters: " << solution->heuristicNonAdopters() << "\n";
		//std::cout << "nonAdopters: " << solution->nonAdopters() << "\n";
		//printGraphStats(graph);
		//iterativeDeepening(&graph, 10, std::cout);
		//State initialState(&graph, 3);
		//State *solution = uniformCostSearch(&initialState);
		//solution->print(std::cout);
		//delete solution;

		return 0;

	} catch (std::exception *e) {
		std::cout << "search: An exception occurred: " << e->what();
	}

	return 1;
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

struct NodeInfo {
	NodeInfo(const int & id) : _id(id), _edges(0) {}

	int _id, _edges;

	bool operator<(const NodeInfo & other) {
		return _edges > other._edges;
	}
};

void printGraphStats(Graph & graph)
{
	std::vector<NodeInfo> vec;

	for (std::pair<VertexIterator, VertexIterator> vp = boost::vertices(graph);
			vp.first != vp.second; ++vp.first) {

		vec.emplace_back(graph[*vp.first].id);

		for (std::pair<OutEdgeIterator, OutEdgeIterator> ep = boost::out_edges(*vp.first, graph);
				ep.first != ep.second; ++ep.first) {
			++vec.back()._edges;
		}
	}

	std::sort(vec.begin(), vec.end());

	std::cout << "<Node>: <Edge count>\n";
	std::cout << "--------------------\n";
	for (auto iter = vec.cbegin(); iter != vec.cend(); ++iter) {
		std::cout << iter->_id << ": " << iter->_edges << "\n";
	}
}