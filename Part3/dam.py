# So we want to look 500 times. The first 5 times, we choose
# at random. And then after that, we do the comparison between
# the remembered sets and the non-remembered sets.

from collections import deque
import sys
import csv
import random 

N = 500
M_a = 5
M_d = 5


mru_queue_a = deque()
mru_queue_d = deque()

def play_game(s_a, s_d):
    a = random.random()

    if (a < s_a):
        # Choose strategy from mru_queue_a
        i = random.randint(0, M_a - 1)
        strat_a = mru_queue_a[i] 
    else:
        # Choose strategy not in mru_queue_a
        i = random.randint(0, 100)
        while (i in mru_queue_a):
            i = random.randint(0, 100)

        strat_a = i

    d = random.random()
    if (d < s_d):
        # Choose strategy from mru_queue_d
        i = random.randint(0, M_d - 1)
        strat_d = mru_queue_d[i] 
    else:
        # Choose strategy not in mru_queue_q
        i = random.randint(0, 100)
        while (i in mru_queue_d):
            i = random.randint(0, 100)

        strat_d = i

    # Add in the start_a to mru_queue_a
    mru_queue_a.appendleft(strat_a)
    mru_queue_a.pop()
    # Add in the start_d to mru_queue_d
    mru_queue_d.appendleft(strat_d)
    mru_queue_d.pop()

    if (strat_d == strat_a):
        # You lose sucka
        return -100, -100
    else:
        return 9900, -10100

def compute_payoffs(s_a, s_d):
    payoff_total_a = 0
    payoff_total_d = 0

    for i in xrange(0, 5):
        strat_a = random.randint(0, 101)
        strat_d = random.randint(0, 101)

        # Add in the start_a to mru_queue_a
        mru_queue_a.appendleft(strat_a)
        # Add in the start_d to mru_queue_d
        mru_queue_d.appendleft(strat_d)

        if (strat_d == strat_a):
            # You lose sucka
            payoff_total_d -= 100
            payoff_total_a -= 100
        else:
            payoff_total_d -= 10100
            payoff_total_a += 9900

    for i in xrange(5, N + 1):
        a, d = play_game(s_a, s_d)
        payoff_total_a += a
        payoff_total_d += d

    return (payoff_total_a, payoff_total_d)

def build_table():
    table = []
    for s_a in [0.0, 0.25, 0.5, 0.75, 1.0]:
        row = []
        for s_d in [0.0, 0.25, 0.5, 0.75, 1.0]:
            a_total = 0
            d_total = 0
            for x in xrange(0, 100):
                (a, d) = compute_payoffs(s_a, s_d)
                a_total += a
                d_total += d
                mru_queue_d.clear()
                mru_queue_a.clear()
            row.append((a_total//100, d_total//100))
        table.append(row)
    return table

with open ('DAM.csv', 'w') as f:
    writer = csv.writer(f, delimiter = ',')
    for row in build_table():
        writer.writerow(row)
