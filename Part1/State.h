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

#include "Graph.h"


class State {
public:
	State(Graph *graph);
	~State();

	inline double expectedAdopters() { return _expectedAdopters; }
	inline const std::vector<int> & receivedCard() { return _receivedCard; }
	inline const std::unordered_set<int> & exposed() { return _exposed; }
	inline int timestep() { return _timestep; }

	bool isGoal() const;
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
		std::pair<VertexIterator, VertexIterator> _vertexIterators;
	};

	friend class SuccessorIterator;

private:
	Graph *_graph;
	double _expectedAdopters;
	std::vector<int> _receivedCard;
	std::unordered_set<int> _exposed;
	int _timestep;
};

#endif // STATE_H