// ASU CSE 471 Course Project
// Team HAL

// The State class represents the current marketing situation
// for the CactusCard, including the people who have been given
// free cards so far, a set of people that have been exposed,
// and the expected number of adopters so far.

#ifndef STATE_H
#define STATE_H

#include <vector>
#include <unordered_set>
#include <utility>
#include <ostream>

#include "Graph.h"


class State {
public:
	inline State(Graph *graph, unsigned int maxFreeCards) : _graph(graph), _expectedAdopters(0.0),
		_nonAdopters(0.0), _receivedCard(), _exposed(), _maxFreeCards(maxFreeCards) {}
	inline ~State() {}

	inline double expectedAdopters() const { return _expectedAdopters; }
	inline double nonAdopters() const { return _nonAdopters; }
	inline const std::vector<int> & receivedCard() const { return _receivedCard; }
	inline const std::unordered_set<int> & exposed() const { return _exposed; }
	inline unsigned int timestep() const { return _receivedCard.size(); }
	inline unsigned int maxFreeCards() const { return _maxFreeCards; }

	bool isGoal() const;
	void print(std::ostream & os);
	
	class SuccessorIterator;
	SuccessorIterator successors() const;

	class SuccessorIterator {
	public:
		SuccessorIterator(const State *predecessor);

		bool next();
		inline bool hasCurrent() const { return _current != 0; }
		inline State *current() const { return _current; } // Caller has responsibility for deleting.

	private:
		const State *_predecessor;
		State *_current;
		VertexIterator _nextVertex;
		VertexIterator _endVertex;
	};

	friend class SuccessorIterator;

private:
	Graph *_graph;
	double _expectedAdopters;
	double _nonAdopters;
	std::vector<int> _receivedCard;
	std::unordered_set<int> _exposed;
	unsigned int _maxFreeCards;
};

#endif // STATE_H