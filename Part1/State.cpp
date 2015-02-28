// Team HAL

// The State class represents the current marketing situation
// for the CactusCard, including the people who have been given
// free cards so far, a set of people that have been exposed,
// and the expected number of adopters so far.

#include "State.h"

State::State(Graph *graph, unsigned int maxFreeCards) : _graph(graph), _expectedAdopters(0.0),
	_nonAdopters(0.0), _receivedCard(), _exposed(), _maxFreeCards(maxFreeCards)
{

}

State::~State()
{

}

bool State::isGoal() const
{
	return _receivedCard.size() == _maxFreeCards;
}

void State::print(std::ostream & os)
{
	os << "Given free cards: [";
	for (auto iter = _receivedCard.cbegin(); iter != _receivedCard.cend(); ++iter) {
		if (iter != _receivedCard.cbegin()) {
			os << ", ";
		}

		os << *iter;
	}

	os << "]";
	if (isGoal()) {
		os << " (FINAL)\nExpected adopters: ";
	} else {
		os << "\nExpected adopters: ";
	}

	os << _expectedAdopters << "\nNon-adopters: " << _nonAdopters << '\n';
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

	std::pair<OutEdgeIterator, OutEdgeIterator> ep;
	for (ep = boost::out_edges(currentVertex, graph); ep.first != ep.second; ++ep.first) {
		Edge e = *ep.first;
		_current->_exposed.insert(graph[boost::target(e, graph)].id);
	}

	int previousExposed = _predecessor->_exposed.size();
	int newlyExposed = _current->_exposed.size() - previousExposed;

	double proportion;
	if (previousExposed == 0) {
		proportion = 0.1;
	} else {
		proportion = 1.0 - 1.0 / previousExposed;
		proportion = proportion > 0.1 ? proportion : 0.1;
	}

	double newlyAdopting = newlyExposed * proportion + 1; // +1 for the person who was given a free card
	_current->_expectedAdopters += newlyAdopting;
	double nonAdopting = newlyExposed * (1 - proportion);
	_current->_nonAdopters += nonAdopting;

	// The receiver is added to the set of exposed people here so that
	// it is not included in the above calculation to determine the number of people adopting.
	_current->_exposed.insert(receiver);

	if (_current->timestep() == _current->_maxFreeCards) {
		// The final card was just given. Therefore, add all people who have not been exposed
		// (and will now never be exposed) to the nonAdopters count.
		int totalExposed = _current->_exposed.size();
		_current->_nonAdopters += boost::num_vertices(graph) - totalExposed;
	}

	return true;
}