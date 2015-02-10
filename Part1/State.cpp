// Team HAL

// The State class represents the current marketing situation
// for the CactusCard, including the people who have been given
// free cards so far, a set of people that have been exposed,
// and the expected number of adopters so far.

#include "State.h"

State::State(Graph *graph) : _graph(graph), _expectedAdopters(0.0),
	_receivedCard(), _exposed(), _timestep(0)
{

}

State::~State()
{

}

bool State::isGoal() const
{
	return _receivedCard.size() == 10;
}

State::SuccessorIterator State::successors() const
{
	return SuccessorIterator(this);
}

State::SuccessorIterator::SuccessorIterator(const State *predecessor) : _predecessor(predecessor),
	_current(0)
{
	_vertexIterators = boost::vertices(*predecessor->_graph);
	next();
}

bool State::SuccessorIterator::next()
{
	Graph & g = *_predecessor->_graph;

	// Find someone who is not already exposed.
	while (_vertexIterators.first != _vertexIterators.second &&
			_predecessor->_exposed.count(g[*_vertexIterators.first].id) > 0) {
		++_vertexIterators.first;
	}

	if (_vertexIterators.first == _vertexIterators.second) {
		// We have iterated through all non-exposed people.
		_current = 0;
		return false;
	}

	// Person who is receiving a free card.
	int receiver = g[*_vertexIterators.first].id;

	// Don't delete old _current as it is client's responsibility to delete.
	_current = new State(*_predecessor);
	_current->_receivedCard.push_back(receiver);
	++_current->_timestep;

	std::pair<OutEdgeIterator, OutEdgeIterator> ep;
	for (ep = boost::out_edges(*_vertexIterators.first, g); ep.first != ep.second; ++ep.first) {
		Edge e = *ep.first;
		_current->_exposed.insert(g[boost::target(e, g)].id);
	}

	int newExposed = _current->_exposed.size() - _predecessor->_exposed.size();
	double prop1 = 1.0 - 1.0 / _predecessor->_exposed.size();
	double propAdopting = prop1 > 0.1 ? prop1 : 0.1;
	double newAdopting = newExposed * propAdopting;
	_current->_expectedAdopters += newAdopting;

	return true;
}