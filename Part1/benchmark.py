#!/usr/bin/python

import subprocess
import re
import csv
import sys

trials = 1
tests = {
	'uniform': [1, 2, 3],
	'exhaustive': [1, 2, 3],
	'A-star': [1, 2, 3, 4]
}

def call(args, shell=False):
	sp = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
		stderr=subprocess.PIPE, shell=shell)
	return sp.communicate()

def avg(l):
	return float(sum(l)) / len(l)

class Trial:
	def __init__(self, discovered, expanded, time, memory):
		self.discovered = discovered
		self.expanded = expanded
		self.time = time
		self.memory = memory

class TrialSet:
	def __init__(self):
		self.trials = []

	#def add(self, discovered, expanded, time, memory):
	#	self.trials.append(Trial(discovered, expanded, time, memory))

	def append(self, trial):
		self.trials.append(trial)

	def discovered(self):
		return str(int(avg([trial.discovered for trial in self.trials])))

	def expanded(self):
		return str(int(avg([trial.expanded for trial in self.trials])))

	def time(self):
		return '{0:.2f} s'.format(avg([trial.time for trial in self.trials]))

	def memory(self):
		return '{0:.2f} kB'.format(avg([trial.memory for trial in self.trials]))


def run(algorithm, depth):
	output, err = call(['/usr/bin/time', '-v', './search', algorithm, str(depth), '348.edges.txt'])
	output = output.decode('ascii')
	err = err.decode('ascii')
	m = re.search(r'explored: (\d+)', output)
	if m:
		discovered = int(m.group(1))
		expanded = discovered
	else:
		discovered = int(re.search(r'discovered: (\d+)', output).group(1))
		expanded = int(re.search(r'expanded: (\d+)', output).group(1))
	time = float(re.search(r'User time \(seconds\): ([.\d]+)', err).group(1))
	memory = float(re.search(r'Maximum resident set size \(kbytes\): (\d+)' , err).group(1))
	return Trial(discovered, expanded, time, memory)

def write(writer, results, name, max_depth, func):
	algorithms = [a for a in results]
	writer.writerow([name] + algorithms)
	for d in range(1, max_depth + 1):
		writer.writerow([str(d)] + [func(results[a][d]) if d in results[a] else '-' for a in algorithms])
	writer.writerow([])

def main():
	#call(['make', 'optimized'])
	results = {}
	max_depth = 0
	for algorithm in tests:
		results[algorithm] = {}
		for depth in tests[algorithm]:
			trialset = TrialSet()
			for i in range(trials):
				trialset.append(run(algorithm, depth))
			results[algorithm][depth] = trialset
			max_depth = max(max_depth, depth)
	path = sys.argv[1]
	with open(path, 'w') as f:
		writer = csv.writer(f)
		write(writer, results, 'discovered', max_depth, lambda s: s.discovered())
		write(writer, results, 'expanded', max_depth, lambda s: s.expanded())
		write(writer, results, 'time', max_depth, lambda s: s.time())
		write(writer, results, 'memory', max_depth, lambda s: s.memory())

if __name__ == '__main__':
	main()