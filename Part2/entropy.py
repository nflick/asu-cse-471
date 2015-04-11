#!/usr/bin/env python

import math
import csv
import itertools

class Sample:
	def __init__(self, line):
		self.attributes = []
		for entry in line[:-1]:
			try:
				self.attributes.append(int(entry))
			except ValueError:
				try:
					self.attributes.append(float(entry))
				except ValueError:
					self.attributes.append(entry)
		self.value = True if line[-1] == '+' else False

def entropy(q):
	'''Returns the entropy of the proportion q.
	'''
	if q <= 0 or q >= 1:
		return 0
	return q * math.log(1/q, 2) + (1 - q) * math.log(1/(1-q), 2)

def read(path):
	with open(path, 'r') as f:
		reader = csv.reader(f)
		return [Sample(line) for line in reader]

def attribute_entropy(samples, attribute):
	p = 0
	n = 0
	pk = {}
	nk = {}
	for sample in samples:
		if sample.value:
			p += 1
			if sample.attributes[attribute] in pk:
				pk[sample.attributes[attribute]] += 1
			else:
				pk[sample.attributes[attribute]] = 1
		else:
			n += 1
			if sample.attributes[attribute] in nk:
				nk[sample.attributes[attribute]] += 1
			else:
				nk[sample.attributes[attribute]] = 1
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

def main():
	samples = read('crx.data.csv')
	attribute_entropy(samples, 8)
	return
	res = {}
	for i in range(15):
		res[i] = attribute_entropy(samples, i)
		print('{0}: {1}'.format(i, attribute_entropy(samples, i)))
	print(res)

if __name__ == '__main__':
	main()
