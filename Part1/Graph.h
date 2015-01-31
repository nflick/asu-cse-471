// Team HAL

// The Graph class represents a simple graph where nodes
// can contain values of a specific type, specified by 
// the template parameter. Implementation must be in the
// header because this is a template class.

#ifndef GRAPH_H
#define GRAPH_H

#include <vector>
#include <unordered_map>

template <typename T>
class Graph {
public:
	class Node {
	public:
		Node(const T & item);
		~Node();

		const T & item() const;
		const std::vector<Node*> & neighbors() const;

		friend class Graph<T>;

	private:
		T _item;
		std::vector<Node*> _neighbors;
	};

	Graph();
	~Graph();

	Node* addNode(const T & item);
	Node* getNode(const T & item);
	int nodeCount() const;
	
	void addEdge(const T & src, const T & dest);

private:
	std::unordered_map<T, Node*> _nodes;
};

template <typename T>
Graph<T>::Graph() : _nodes()
{

}

template <typename T>
Graph<T>::~Graph()
{
	for (auto iter = _nodes.begin(); iter != _nodes.end(); iter++) {
		delete (*iter).second;
	}

	_nodes.clear();
}

template <typename T>
typename Graph<T>::Node *Graph<T>::addNode(const T & item)
{
	if (_nodes.count(item)) {
		return _nodes[item];
	} else {
		Node *node = new Node(item);
		_nodes[item] = node;
		return node;
	}
}

template <typename T>
typename Graph<T>::Node *Graph<T>::getNode(const T & item)
{
	typename std::unordered_map<T, Node*>::iterator iter = _nodes.find(item);
	if (iter != _nodes.end()) {
		return *iter;
	} else {
		return 0;
	}
}

template <typename T>
int Graph<T>::nodeCount() const
{
	return _nodes.size();
}

// Adds a bidirectional edge
template <typename T>
void Graph<T>::addEdge(const T & src, const T & dest)
{
	Node *srcNode = addNode(src);
	Node *destNode = addNode(dest);
	srcNode->_neighbors.push_back(destNode);
	destNode->_neighbors.push_back(srcNode);
}

template <typename T>
Graph<T>::Node::Node(const T & item) : _item(item)
{

}

template <typename T>
Graph<T>::Node::~Node()
{

}

template <typename T>
const T & Graph<T>::Node::item() const
{
	return _item;
}

template <typename T>
const std::vector<typename Graph<T>::Node*> & Graph<T>::Node::neighbors() const
{
	return _neighbors;
}


#endif // GRAPH_H