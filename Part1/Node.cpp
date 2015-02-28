// ASU CSE 471 Course Project
// Team HAL

// The Node class represents a Node in an informed
// or uninformed search.

#include "Node.h"

Node::Node(State *state, Node *parent) : _state(state), _parent(parent),
	_cost(state->nonAdopters()), _children()
{
	if (_parent) {
		_parent->_children.push_back(this);
	}
}

Node::~Node()
{
	for (auto iter = _children.begin(); iter != _children.end(); ++iter) {
		delete *iter;
	}

	_children.clear();
	delete _state;
}