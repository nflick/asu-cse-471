// ASU CSE 471 Course Project
// Team HAL

// The State class represents the current marketing situation
// for the CactusCard, including the people who have been given
// free cards so far, a set of people that have been exposed,
// and the expected number of adopters so far.

#include <vector>
#include <unordered_set>



class State {
public:
	State();
	~State();
	double expectedAdopters();
	const std::vector<int> & receivedCard();
	const std::unordered_set<int> & exposed();
	int timestep();

private:
	double _expectedAdopters;
	std::vector<int> _receivedCard;
	std::unordered_set<int> _exposed;
	int _timestep;
}