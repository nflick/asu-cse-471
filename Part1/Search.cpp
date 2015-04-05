#include "Search.h"

#include <queue>
#include <stdexcept>
#include <ostream>
#include <iostream>

State *uniformCostSearch(State *initialState)
{
	long discovered = 0;
	long expanded = 0;

	std::priority_queue<Node*> frontier;
	// Make a copy of initial state because the copy will be deleted with the node tree.
	Node *initialNode = new Node(new State(*initialState), 0);
	frontier.push(initialNode);
	Node *solution = 0;

	do {
		Node *node = frontier.top();
		frontier.pop();
		++expanded;

		if (node->state()->isGoal()) {
			solution = node;
			break;
		}

		for (State::SuccessorIterator iter = node->state()->successors(); iter.hasCurrent(); iter.next()) {
			Node *child = new Node(iter.current(), node);
			frontier.push(child);
			++discovered;
		}

	} while (!frontier.empty());

	std::cout << "Uniform cost discovered: " << discovered << "\n";
	std::cout << "Uniform cost expanded: " << expanded << "\n";

	if (!solution) {
		throw new std::runtime_error("No goal state in solution space.");
	}

	// Make a copy because the original will be deleted when we delete the node tree.
	State *solutionState = new State(*solution->state());

	// Since Nodes delete their children in their destructor, this one call will
	// recursively delete the entire node tree.
	delete initialNode;

	return solutionState;
}

long exhaustiveStateCount;

State *exhaustiveSearchInner(State *state)
{
	++exhaustiveStateCount; 

	if (state->isGoal()) {
		return state;
	}

	State *best = 0;
	for (State::SuccessorIterator iter = state->successors(); iter.hasCurrent(); iter.next()) {
		State *current = iter.current();
		State *solution = exhaustiveSearchInner(current);

		if (current != solution) {
			delete current;
		}

		if (best == 0) {
			best = solution;
		} else if (solution != 0 && solution->nonAdopters() < best->nonAdopters()) {
			delete best;
			best = solution;
		} else if (solution != 0) {
			delete solution;
		}
	}

	return best;
}

State *exhaustiveSearch(State *state)
{
	exhaustiveStateCount = 0;
	State *solution = exhaustiveSearchInner(state);
	std::cout << "Exhaustive explored: " << exhaustiveStateCount << "\n";
	return solution;
}

State *iterativeDeepening(Graph *graph, int maxDepth, std::ostream & os)
{
	State *solution = 0;

	for (int depth = 1; depth <= maxDepth; ++depth) {
		if (solution) {
			delete solution;
		}

		State *initial = new State(graph, depth);
		solution = exhaustiveSearch(initial);

		os << "[Results for depth=" << depth << "]\n";
		solution->print(os);
		os << '\n';

		delete initial;
	}

	return solution;
}

State *astar(State *initial)
{
	long discovered = 0;
	long expanded = 0;

	std::priority_queue<State*> frontier;
	// Make a copy of initial state because the copy will be deleted with the node tree.
	frontier.push(new State(*initial));
	State *solution = 0;

	do {
		State *state = frontier.top();
		frontier.pop();
		++expanded;

		if (state->isGoal()) {
			solution = state;
			break;
		}

		for (State::SuccessorIterator iter = state->successors(); iter.hasCurrent(); iter.next()) {
			State *child = iter.current();
			frontier.push(child);
			++discovered;
		}

		delete state;

	} while (!frontier.empty());

	std::cout << "A* discovered: " << discovered << "\n";
	std::cout << "A* expanded: " << expanded << "\n";

	// Delete all remaining states in queue.
	while (!frontier.empty()) {
		delete frontier.top();
		frontier.pop();
	}

	if (!solution) {
		throw new std::runtime_error("No goal state in solution space.");
	}

	return solution;
}