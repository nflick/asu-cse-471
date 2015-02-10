// ASU CSE 471 Course Project
// Team HAL

#ifndef GRAPH_H
#define GRAPH_H

#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/labeled_graph.hpp>

struct VertexData {
	int id;
};

typedef boost::labeled_graph<
	boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS, VertexData>, int> Graph;

typedef boost::graph_traits<Graph>::vertex_descriptor Vertex;
typedef boost::graph_traits<Graph>::vertex_iterator VertexIterator;
typedef boost::graph_traits<Graph>::out_edge_iterator OutEdgeIterator;
typedef boost::graph_traits<Graph>::edge_descriptor Edge;

#endif // GRAPH_H