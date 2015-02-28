#include "Uninformed.h"

#include <queue>
#include <stdexcept>

State *uniformCostSearch(State *initialState)
{
	std::priority_queue<Node*> frontier;
	// Make a copy of initial state because the copy will be deleted with the node tree.
	Node *initialNode = new Node(new State(*initialState), 0);
	frontier.push(initialNode);
	Node *solution = 0;

	do {
		Node *node = frontier.top();
		frontier.pop();

		if (node->state()->isGoal()) {
			solution = node;
			break;
		}

		for (State::SuccessorIterator iter = node->state()->successors(); iter.hasCurrent(); iter.next()) {
			Node *child = new Node(iter.current(), node);
			frontier.push(child);
		}

	} while (!frontier.empty());

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