import operator as op
from functools import reduce
import csv
V = 100
B = 10000
c_d = 100

def compute_payoffs(x_a, x_d, c_a):
    return ( ((1 - prob_defended(x_a, x_d)) * payoff_success_a(x_a, c_a) + 
            prob_defended(x_a, x_d) * payoff_fail_a(x_a, c_a)),
            ((1 - prob_defended(x_a, x_d)) * payoff_fail_d(x_d) +
            prob_defended(x_a, x_d) * payoff_success_d(x_d)) )

def payoff_success_a(x_a, c_a):
    return B - x_a * c_a

def payoff_fail_a(x_a, c_a):
    return - x_a * c_a

def payoff_success_d(x_d):
    return - x_d * c_d

def payoff_fail_d(x_d):
    return - B - x_d * c_d

def prob_defended(x_a, x_d):
    if (x_a + x_d >= 101):
        return 1
    else: 
        return 1 - (float(ncr(100 - x_a, x_d)) / ncr(100, x_d))
    
def ncr(n, r):
	
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, range(n, n-r, -1))
    denom = reduce(op.mul, range(1, r+1))
    return numer//denom

def build_table(c_a):
    table = []
    for x in range(1,101):
        row = []
        for y in range(1,101):
            row.append(compute_payoffs(x, y, c_a))
        table.append(row)
    return table

	
def a_best(table):
	a = []
	for i in range (0, 100):
		max = table[0][i][0]
		row = 0
		for j in range (1, 100):
			if(table[j][i][0] >= max):
				max = table[j][i][0];
				row = j
				
		for k in range (0, 100):
			if(abs(table[k][i][0] - max) < .0001):
				a.append((row+1, i+1))
	return a

def d_best(table):
	d = [] 
	for i in range (0, 100):
		max = table[i][0][1]
		for j in range(1, 100):
			if(table[i][j][1] >= max):
				max = table[i][j][1]
				
		for j in range (0, 100):
			if(abs(table[i][j][1] - max) < .0001):
				d.append((i+1, j+1))
	return d

def nash(a, table):
	equilibriums = [] 
	
	for i in range(0, len(a)):
		flag = True
		row = a[i][0] - 1
		col = a[i][1] - 1
		for j in range(0, 100):
			if(table[row][col][1] < table[row][j][1] and abs(table[row][col][1] - table[row][j][1]) > .0001):
				flag = False
				break
	
		if(flag == True):
			equilibriums.append(a[i])
	return equilibriums

table = build_table(100)
	
with open ('table.csv', 'w') as f:
    writer = csv.writer(f, delimiter = ',')
    for row in table:
        writer.writerow(row)
		
a = a_best(table)
print("The nash equilibria are located at:")
print(nash(a, table))

			
		
			

