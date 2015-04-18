#!/usr/bin/env python

import sys
import csv
import copy
import random
import itertools
import math
import scipy.stats
import operator
import functools

import PyML as pyml

class DataSet:
	def __init__(self, num_features, continuous, discrete, strategy):
		self.num_features = num_features
		self.continuous = set(continuous)
		self.discrete = set(discrete)
		assert(self.num_features == len(self.continuous) + len(self.discrete))
		if strategy == 'average' or strategy == 'isolate':
			self.strategy = strategy
		else:
			raise Exception('Invalid argument strategy. Must be one of \'average\' or \'isolate\'.')

	def load(self, source, extractor):
		self.source = source
		with open(source, 'r') as f:
			self.samples = []
			reader = csv.reader(f)
			for line in reader:
				self.samples.append(extractor(self, line))
		self.gen_averages()
		self.fill_missing()
		self.fill_values()

	def gen_averages(self):
		self.averages = {}
		for i in range(self.num_features):
			if i in self.continuous:
				average = sum(sample.features[i] for sample in self.samples if sample.features[i] is not None) / len(self.samples)
				self.averages[i] = average
			elif i in self.discrete:
				values = {}
				for sample in self.samples:
					if sample.features[i] in values:
						values[sample.features[i]] += 1
					else:
						values[sample.features[i]] = 1
				most_common = max((pair[1], pair[0]) for pair in values.items())[1]
				self.averages[i] = most_common
		positive_count = sum(1 if sample.classification else 0 for sample in self.samples)
		self.proportion = float(positive_count) / len(self.samples)
		self.plurality = positive_count > (len(self.samples) / 2.0)

	def fill_missing(self):
		for i in range(self.num_features):
			if i in self.continuous:
				average = self.averages[i]
				for sample in self.samples:
					if sample.features[i] is None:
						sample.features[i] = average
			elif i in self.discrete:
				if self.strategy == 'average':
					replacement = self.averages[i]
				elif self.strategy == 'isolate':
					replacement = '?'
				else:
					raise Exception('Unknown strategy. Must be one of \'average\' or \'isolate\'.')
				for sample in self.samples:
					if sample.features[i] is None:
						sample.features[i] = replacement

	def fill_values(self):
		self.values = {}
		for i in range(self.num_features):
			if i in self.continuous:
				min_ = self.samples[0].features[i]
				max_ = min_
				for sample in self.samples:
					feature = sample.features[i]
					min_ = min(min_, feature)
					max_ = max(max_, feature)
				self.values[i] = (min_, max_)
			elif i in self.discrete:
				values = set()
				for sample in self.samples:
					values.add(sample.features[i])
				self.values[i] = values


class Sample:
	def __init__(self, dataset, features, classification):
		self.dataset = dataset
		self.features = features
		self.classification = classification

	def continuous(self):
		return [self.features[i] for i in sorted(self.dataset.continuous)]

	def discrete(self):
		return [self.features[i] for i in sorted(self.dataset.discrete)]

	def __str__(self):
		return 'Sample(features={0}, classification={1})'.format(self.features, self.classification)

	def __repr__(self):
		return str(self)

def extract_sample(dataset, line):
	features = line[:dataset.num_features]
	for i in range(len(features)):
		if i in dataset.continuous:
			try:
				features[i] = float(features[i])
			except ValueError:
				features[i] = None
		else:
			if features[i] == '?':
				features[i] = None
	classification = True if line[-1] == '+' else False
	return Sample(dataset, features, classification)

class DecisionNode:
	def __init__(self, parent, samples, feature, gain):
		self.parent = parent
		self.samples = samples
		self.feature = feature
		self.gain = gain
		self.children = {}

	def classify(self, sample):
		return self.children[sample.features[self.feature]].classify(sample)

	def __str__(self):
		p = sum(1 if sample.classification else 0 for sample in self.samples)
		n = len(self.samples) - p
		if self.parent is None:
			value = None
		else:
			for value, child in self.parent.children.items():
				if self == child:
					break
		return 'DecisionNode(value={0}, p={1}, n={2}, feature={3})'.format(value, p, n, self.feature)

	def print_repr(self, depth):
		print('{0}{1}'.format('    ' * depth, self))
		for child in self.children:
			self.children[child].print_repr(depth + 1)

class LeafNode:
	def __init__(self, parent, samples, classification, type_):
		self.parent = parent
		self.samples = samples
		self.classification = classification
		self.type_ = type_

	def classify(self, sample):
		return (self.classification, self.type_)

	def __str__(self):
		p = sum(1 if sample.classification else 0 for sample in self.samples)
		n = len(self.samples) - p
		if self.parent is None:
			value = None
		else:
			for value, child in self.parent.children.items():
				if self == child:
					break
		return 'LeafNode(value={0}, p={1}, n={2}, classification={3}, type={4})'.format(
			value, p, n, self.classification, self.type_)

	def print_repr(self, depth):
		print('{0}{1}'.format('    ' * depth, self))

class SvmNode:
	def __init__(self, parent, samples):
		self.parent = parent
		self.samples = samples
		self.type_ = 'svm'
		matrix = [sample.continuous() for sample in self.samples]
		labels = ['+' if sample.classification else '-' for sample in samples]
		self.vds = pyml.VectorDataSet(matrix, L=labels)
		self.svm = pyml.SVM()
		self.svm.train(self.vds)

	def classify(self, sample):
		vds = pyml.VectorDataSet([sample.continuous()])
		res = self.svm.test(vds)
		return (res.getPredictedLabels(0)[0] == '+', self.type_)

	def __str__(self):
		p = sum(1 if sample.classification else 0 for sample in self.samples)
		n = len(self.samples) - p
		if self.parent is None:
			value = None
		else:
			for value, child in self.parent.children.items():
				if self == child:
					break
		return 'LeafNode(value={0}, p={1}, n={2})'.format(value, p, n)

	def print_repr(self, depth):
		print('{0}{1}'.format('    ' * depth, self))


def entropy(q):
	if q <= 0 or q >= 1:
		return 0
	return q * math.log(1.0/q, 2) + (1 - q) * math.log(1/(1.0-q), 2)

def feature_entropy(samples, feature):
	p = 0
	n = 0
	pk = {}
	nk = {}
	for sample in samples:
		value = sample.features[feature]
		if sample.classification:
			p += 1
			if value in pk:
				pk[value] += 1
			else:
				pk[value] = 1
		else:
			n += 1
			if value in nk:
				nk[value] += 1
			else:
				nk[value] = 1
	m = set(itertools.chain(pk.keys(), nk.keys()))
	e = 0.0
	for k in m:
		if k in pk:
			pk_ = pk[k]
		else:
			pk_ = 0
		if k in nk:
			nk_ = nk[k]
		else:
			nk_ = 0
		e += (float(pk_ + nk_) / (p + n)) * entropy(float(pk_) / (pk_ + nk_))
	return e

def gain(dataset, samples, feature):
	return entropy(dataset.proportion) - feature_entropy(samples, feature)

def plurality_value(samples):
	positive_count = sum(1 if sample.classification else 0 for sample in samples)
	return (positive_count > (len(samples) / 2.0), positive_count == len(samples) or positive_count == 0)

def build_tree(dataset, samples, parent, remaining_features):
	if len(samples) == 0:
		return LeafNode(parent, samples, plurality_value(parent.samples)[0], 'empty')
		#return LeafNode(parent, samples, dataset.plurality, 'empty')

	plurality, unanimous = plurality_value(samples)
	if unanimous:
		return LeafNode(parent, samples, plurality, 'unanimous')
	if len(remaining_features) == 0:
		return LeafNode(parent, samples, plurality, 'plurality')

	best_feature = min(remaining_features)
	best_gain = gain(dataset, samples, best_feature)
	for feature in remaining_features:
		g = gain(dataset, samples, feature)
		if g > best_gain:
			best_feature = feature
			best_gain = g

	next_remaining_features = copy.copy(remaining_features)
	next_remaining_features.discard(best_feature)

	node = DecisionNode(parent, samples, best_feature, best_gain)
	for value in dataset.values[best_feature]:
		filtered_samples = [sample for sample in samples if sample.features[best_feature] == value]
		node.children[value] = build_tree(dataset, filtered_samples, node, next_remaining_features)

	return node

def significance_test(dataset, node):
	delta = 0
	df = 0
	for child in node.children.values():
		if len(child.samples) == 0:
			continue
		pk = sum(1 if sample.classification else 0 for sample in child.samples)
		nk = len(child.samples) - pk
		pk_expected = dataset.proportion * len(child.samples)
		nk_expected = len(child.samples) - pk_expected
		delta += float(pk - pk_expected) ** 2 / pk_expected + float(nk - nk_expected) ** 2 / nk_expected
		df += 1
	p = 1 - scipy.stats.chi2.cdf(delta, df=df)
	return p <= 0.1

def prune_tree(dataset, parent, node):
	if isinstance(node, LeafNode):
		return node
	for value, child in list(node.children.items()):
		node.children[value] = prune_tree(dataset, node, child)

	# Check if all remaining children are leaf nodes
	for value, child in node.children.items():
		if not isinstance(child, LeafNode):
			return node

	# All remaining children are leaf nodes. Check if they all have the same classification.
	classification = next(iter(node.children.values())).classification
	for value, child in node.children.items():
		if child.classification != classification:
			break
	else:
		# All children have same classification. Prune this node.
		return LeafNode(parent, node.samples, classification, 'pruned')

	if significance_test(dataset, node):
		return node
	else:
		# Node is not significant. Prune it.
		plurality, unanimous = plurality_value(node.samples)
		return LeafNode(parent, node.samples, plurality, 'pruned')

def inject_svm(dataset, parent, node):
	if isinstance(node, DecisionNode):
		for value, child in list(node.children.items()):
			node.children[value] = inject_svm(dataset, node, child)
		return node

	if not isinstance(node, LeafNode):
		return node

	plurality, unanimous = plurality_value(node.samples)
	if unanimous:
		return node

	# Replace with SVM node
	return SvmNode(parent, node.samples)


def partition(samples, k):
	partitions = []
	while len(samples) > 0:
		num = int(math.ceil(float(len(samples)) / k))
		partitions.append(samples[:num])
		samples = samples[num:]
		k -= 1
	return partitions

def cross_validate(dataset, kfold):
	samples = dataset.samples[:]
	partitions = partition(samples, kfold)
	true_pos = 0
	true_neg = 0
	false_pos = 0
	false_neg = 0
	total = 0
	errors = {}

	stdout = sys.stdout
	sys.stdout = open('/dev/null', 'w')

	for k in range(kfold):
		training = functools.reduce(operator.add, (p for i, p in enumerate(partitions) if i != k))
		test = partitions[k]

		root = build_tree(dataset, training, None, dataset.discrete)
		root = prune_tree(dataset, None, root)
		#root = inject_svm(dataset, None, root)

		for sample in test:
			classification, type_ = root.classify(sample)
			error = False
			if classification and sample.classification:
				true_pos += 1
			elif not classification and sample.classification:
				false_neg += 1
				error = True
			elif classification and not sample.classification:
				false_pos += 1
				error = True
			else:
				true_neg += 1

			if error:
				if type_ in errors:
					errors[type_] += 1
				else:
					errors[type_] = 1

		total += len(test)

	null = sys.stdout
	sys.stdout = stdout
	null.close()

	print('Total:           {0}'.format(total))
	print('True positives:  {0}'.format(true_pos))
	print('False positives: {0}'.format(false_pos))
	print('True negatives:  {0}'.format(true_neg))
	print('False negatives: {0}'.format(false_neg))
	print('Precision:       {0}'.format(true_pos / float(true_pos + false_pos)))
	print('Recall:          {0}'.format(true_pos / float(true_pos + false_neg)))
	print('Errors:          {0}'.format(errors))

def compare_pruned(dataset):
	root = build_tree(dataset, dataset.samples, None, dataset.discrete)
	root.print_repr(0)
	print('===========================================================')
	print('===========================================================')
	root = prune_tree(dataset, None, root)
	root.print_repr(0)

def print_entropy(dataset):
	for feature in dataset.discrete:
		print('Feature {0}: {1}'.format(feature, feature_entropy(dataset.samples, feature)))

def main():
	dataset = DataSet(15, [1, 2, 7, 10, 13, 14], [0, 3, 4, 5, 6, 8, 9, 11, 12], 'isolate')
	dataset.load('crx.data.csv', extract_sample)
	cross_validate(dataset, 5)

if __name__ == '__main__':
	main()