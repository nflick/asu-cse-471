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
	std::pair<VertexIterator, VertexIterator> pair = boost::vertices(*predecessor->_graph);
	_nextVertex = pair.first;
	_endVertex = pair.second;
	next();
}

bool State::SuccessorIterator::next()
{
	Graph & graph = *_predecessor->_graph;

	if (_nextVertex == _endVertex) {
		_current = 0;
		return false;
	}

	// Person who is receiving a free card.
	Vertex currentVertex = *_nextVertex;
	int receiver = graph[currentVertex].id;

	// Find someone who is not already exposed.
	do {
		++_nextVertex;
	} while (_nextVertex != _endVertex &&
		_predecessor->_exposed.count(graph[*_nextVertex].id) > 0);

	// Don't delete old _current as it is client's responsibility to delete.
	_current = new State(*_predecessor);
	_current->_receivedCard.push_back(receiver);
	++_current->_timestep;

	std::pair<OutEdgeIterator, OutEdgeIterator> ep;
	for (ep = boost::out_edges(currentVertex, graph); ep.first != ep.second; ++ep.first) {
		Edge e = *ep.first;
		_current->_exposed.insert(graph[boost::target(e, graph)].id);
	}

	int previousExposed = _predecessor->_exposed.size();
	int newExposed = _current->_exposed.size() - previousExposed;

	double proportionAdopting;
	if (previousExposed == 0) {
		proportionAdopting = 0.1;
	} else {
		double prop = 1.0 - 1.0 / previousExposed;
		proportionAdopting = prop > 0.1 ? prop : 0.1;
	}

	double newAdopting = newExposed * proportionAdopting;
	_current->_expectedAdopters += newAdopting;

	return true;
}