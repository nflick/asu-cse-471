#ifndef SEARCH_H
#define SEARCH_H

#include "State.h"
#include "Node.h"

State *uniformCostSearch(State *initial);
State *exhaustiveSearch(State *state);
State *iterativeDeepening(Graph *graph, int maxDepth, std::ostream & os);
State *astar(State *initial);

#endif // SEARCH_H