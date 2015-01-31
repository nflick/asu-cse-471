// Team HAL

// The State class represents the current marketing situation
// for the CactusCard, including the people who have been given
// free cards so far, a set of people that have been exposed,
// and the expected number of adopters so far.

#include "State.h"

State::State() : _expectedAdopters(0.0), _receivedCard(),
	_exposed(), _timestep(0)
{

}

State::~State()
{

}

double State::expectedAdopters()
{
	return _expectedAdopters;
}

const std::vector<int> & State::receivedCard()
{
	return _receivedCard;
}

const std::unordered_set<int> & State::exposed()
{
	return _exposed;
}

int State::timespec()
{
	return _timestep;
}