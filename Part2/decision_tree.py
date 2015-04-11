#!/usr/bin/env python

import csv
import copy
import random
import itertools
import math

class Sample:
	def __init__(self, line):
		self.continuous = []
		self.discrete = []
		for entry in line[:-1]:
			try:
				self.continuous.append(int(entry))
			except ValueError:
				try:
					self.continuous.append(float(entry))
				except ValueError:
					self.discrete.append(entry)
		self.classification = True if line[-1] == '+' else False

	def __str__(self):
		return 'Sample(continuous={0}, discrete={1}, classification={2})'.format(
			self.continuous, self.discrete, self.classification)

class DecisionNode:
	def __init__(self, value, attribute, children):
		self.value = value
		self.attribute = attribute
		self.children = children

	def classify(self, sample):
		return self.children[sample.discrete[self.attribute]].classify(sample)

	def expand(self, depth):
		print('{0}DecisionNode value={1}, attribute={2}'.format('  ' * depth, self.value, self.attribute))
		for child in self.children:
			self.children[child].expand(depth + 1)

class LeafNode:
	def __init__(self, value, classification):
		self.value = value
		self.classification = classification

	def classify(self, sample):
		return self.classification

	def expand(self, depth):
		print('{0}LeafNode value={1}, classification={2}'.format('  ' * depth, self.value, self.classification))

def entropy(q):
	if q <= 0 or q >= 1:
		return 0
	return q * math.log(1/q, 2) + (1 - q) * math.log(1/(1-q), 2)

def attribute_entropy(samples, attr):
	p = 0
	n = 0
	pk = {}
	nk = {}
	for sample in samples:
		if sample.classification:
			p += 1
			if sample.discrete[attr] in pk:
				pk[sample.discrete[attr]] += 1
			else:
				pk[sample.discrete[attr]] = 1
		else:
			n += 1
			if sample.discrete[attr] in nk:
				nk[sample.discrete[attr]] += 1
			else:
				nk[sample.discrete[attr]] = 1
	m = set(itertools.chain(pk.keys(), nk.keys()))
	e = 0.0
	for k in m:
		if k in pk:
			pk_ = pk[k]
		else:
			pk_ = 0
		if k in nk:
			nk_ = nk[k]
		else: nk_ = 0
		e += (float(pk_ + nk_) / (p + n)) * entropy(float(pk_) / (pk_ + nk_))
	return e

def gain(samples, attr):
	return 1 - attribute_entropy(samples, attr)

def build_tree(samples, parent_value, remaining_attr):
	positive_count = sum(1 if sample.classification else 0 for sample in samples)
	if positive_count == len(samples):
		return LeafNode(parent_value, True)
	elif positive_count == 0:
		return LeafNode(parent_value, False)

	if len(remaining_attr) == 0:
		return LeafNode(parent_value, True if positive_count > (len(samples) / 2) else False)

	best_attr = min(remaining_attr)
	best_gain = 0
	for attr in remaining_attr:
		g = gain(samples, attr)
		if g > best_gain:
			best_attr = attr
			best_gain = g

	next_remaining_attr = copy.copy(remaining_attr)
	next_remaining_attr.discard(best_attr)

	values = set()
	for sample in samples:
		values.add(sample.discrete[best_attr])

	children = {}
	for value in values:
		filtered_samples = [sample for sample in samples if sample.discrete[best_attr] == value]
		child = build_tree(filtered_samples, value, next_remaining_attr)
		children[value] = child

	return DecisionNode(parent_value, best_attr, children)

def read(path):
	with open(path, 'r') as f:
		reader = csv.reader(f)
		return [Sample(line) for line in reader]

def main():
	samples = read('crx.data.csv')
	random.shuffle(samples)
	mid = len(samples) >> 1
	training = samples[:mid]
	test = samples[mid:]

	root = build_tree(samples, None, set(range(len(samples[0].discrete))))
	correct = 0
	for trial in test:
		if root.classify(trial) == trial.classification:
			correct += 1
	print('Correct: {0} / {1}'.format(correct, len(test)))

if __name__ == '__main__':
	main()