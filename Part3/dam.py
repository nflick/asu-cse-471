# So we want to look 500 times. The first 5 times, we choose
# at random. And then after that, we do the comparison between
# the remembered sets and the non-remembered sets.

from collections import deque
import sys
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
        i = random.randint(0, 101)
        while (i in mru_queue_a):
            i = random.randint(0, 101)

        strat_a = i

    d = random.random()
    if (d < s_d):
        # Choose strategy from mru_queue_d
        i = random.randint(0, M_d - 1)
        strat_d = mru_queue_d[i] 
    else:
        # Choose strategy not in mru_queue_q
        i = random.randint(0, 101)
        while (i in mru_queue_d):
            i = random.randint(0, 101)

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
    a, d = play_game(sys.argv[1], sys.argv[2])
    payoff_total_a += a
    payoff_total_d += d

print("Result:")
print("Payoff total attacker: {0}".format(payoff_total_a))
print("Payoff total defender: {0}".format(payoff_total_d))

