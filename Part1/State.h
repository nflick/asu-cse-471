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
#include <algorithm>
#include <iostream>

#include "Graph.h"


class State {
public:
	inline State(Graph *graph, unsigned int maxFreeCards) : _graph(graph), _expectedAdopters(0.0),
		_nonAdopters(0.0), _receivedCard(), _maxFreeCards(maxFreeCards),
		_numPeople(boost::num_vertices(*graph)) {
			std::unordered_set<int> exposed;
			calcHeuristic(exposed);
		}

	inline ~State() {}

	inline double expectedAdopters() const { return _expectedAdopters; }
	inline double nonAdopters() const { return _nonAdopters; }
	inline double heuristic() const { return _heuristic; }
	inline const std::vector<int> & receivedCard() const { return _receivedCard; }
	inline unsigned int timestep() const { return _receivedCard.size(); }
	inline unsigned int maxFreeCards() const { return _maxFreeCards; }

	inline bool operator<(const State & other) const {	
		// C++ STL priority queues always pop the highest element. Therefore
		// the node with the lowest cost needs to be considered greatest, which
		// is why this uses a greater-than rather than a less-than in comparing
		// the costs.
		return _heuristic > other._heuristic;
	}

	bool isGoal() const;
	void calcHeuristic(std::unordered_set<int> & exposed);
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
		std::unordered_set<int> _exposed;
		std::vector<int> _tempExposed;
	};

	friend class SuccessorIterator;

private:
	Graph *_graph;
	double _expectedAdopters;
	double _nonAdopters;
	double _heuristic;
	std::vector<int> _receivedCard;
	unsigned int _maxFreeCards;
	unsigned int _numPeople;
};

namespace std {
	template<>
	struct less<State*> {
		bool operator()(const State *a, const State *b) const {
			return (*a) < (*b);
		}
	};
}

#endif // STATE_H