# In which we simulate gameplay under MUCM for the 
# attacker and defender. We are going to need the payofff
# computations from the previous calculations, as well as
# the nash equilibrium solutions that you found. We should
# be specifically looking at equilibrium strategy profiles.

# Now, there are 100 Nash Equilibria for each given cost, so we
# should randomize the choice between all of them. We will start
# with five different gamplay situations, with c_a at 10, 50, 100
# 200, 300.

# Maybe run things more than once.

# So it would be nice if we had a function play_game that took a strategy
# profile and spit out a result when using X random elements v.
# The output should say which elements were chosen, whether or not
# the attacker was caught, and what the payoff was
import random
from payoff_matrix import *

def play_game(x_a, x_d, c_a):
    # Randomly select x_a and x_d random values without replacement
    V = xrange(1,101)
    v_a = set(random.sample(V, x_a))
    v_d = set(random.sample(V, x_d))
    
    if (v_a.isdisjoint(v_d)):
      payoff_a = payoff_success_a(x_a, c_a)
      payoff_d = payoff_fail_d(x_d)
    else:
      payoff_a = payoff_fail_a(x_a, c_a)
      payoff_d = payoff_success_d(x_d)

    # If there is an intersection, ... compute payoffs for that.

    # otherwise, if there is no intersection, compute the payoffs for that


    print("\nResults:")
    print("The attacker's payoff was: {0}".format(payoff_a))
    print("The defender's payoff was: {0}".format(payoff_d))


print("\n---------- x_a = 50 ---------")
for x in xrange(1,6):
  play_game(1, 50, x*100)

print("\n---------- x_a = 60 ---------")
for x in xrange(1,6):
  play_game(1, 60, x*100)

print("\n---------- x_a = 65 ---------")
for x in xrange(1,6):
  play_game(1, 65, x*100)

print("\n---------- x_a = 70 ---------")
for x in xrange(1,6):
  play_game(1, 70, x*100)

print("\n---------- x_a = 75 ---------")
for x in xrange(1, 6):
  play_game(1, 75, x*100)

print("\n---------- x_a = 80 ---------")
for x in xrange(1, 6):
  play_game(1, 80, x*100)

# We want a function that calls play_game for a given cost matrix that chooses
# a random Nash equilibrium from the matrix. 


