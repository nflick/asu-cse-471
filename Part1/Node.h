// ASU CSE 471 Course Project
// Team HAL

// The Node class represents a Node in an informed
// or uninformed search.

#ifndef NODE_H
#define NODE_H

#include <vector>

#include "State.h"

class Node {
public:
	Node(State *state, Node *parent);
	~Node();

	inline State *state() const { return _state; }
	inline double cost() const { return _cost; }

	inline bool operator<(const Node & other) const {	
		// C++ STL priority queues always pop the highest element. Therefore
		// the node with the lowest cost needs to be considered greatest, which
		// is why this uses a greater-then rather than a less-then in comparing
		// the costs.
		return _cost > other._cost;
	}

private:
	State *_state;
	Node *_parent;
	double _cost;
	std::vector<Node*> _children;
};

namespace std {
	template<>
	struct less<Node*> {
		bool operator()(const Node *a, const Node *b) const {
			return (*a) < (*b);
		}
	};
}

#endif // NODE_H