import operator as op
import csv
V = 100

def compute_payoffs(x_a, x_d, c_a):
    return ( (1 - prob_defended(x_a, x_d)) * payoff_success_a(x_a, c_a) + 
            prob_defended(x_a, x_d) * payoff_fail_a(x_a, c_a),
            (1 - prob_defended(x_a, x_d)) * payoff_fail_d(x_d) +
            prob_defended(x_a, x_d) * payoff_success_d(x_d) )

def payoff_success_a(x_a, c_a):
    return 10000 - x_a * c_a

def payoff_fail_a(x_a, c_a):
    return - x_a * c_a

def payoff_success_d(x_d):
    return - x_d * 100

def payoff_fail_d(x_d):
    return (- 10000 - x_d * 100)

def prob_defended(x_a, x_d):
    if (x_a + x_d >= 101):
        return 1
    else: 
        return 1 - (float(ncr(100 - x_a, x_d)) / ncr(100, x_d))
    
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom

def build_table(c_a):
    table = []
    for x in xrange(1,101):
        row = []
        for y in xrange(1,101):
            row.append(compute_payoffs(x, y, c_a))
        table.append(row)
    return table

with open ('table.csv', 'w') as f:
    writer = csv.writer(f, delimiter = ',')
    for row in build_table(100):
        writer.writerow(row)

