#!/usr/bin/env python

'''
File: main.py
Author: Adrien Lemaire
Description: Main program for a 10-armed testbed
'''

import numpy as np
import os
import sys
import time

from models import Bandit
from utils import execution_time, draw


class Result(dict):
    """Datas for a graph. Contains lines and a label::

        >>> reward_values = Result("Average Rewards")
        >>> reward_values["egreedy 0.1"] = [0.1, 0.5, 0.2, 0.4]
        >>> reward_values
        {'egreedy 0.1': [0.1, 0.5, 0.2, 0.4]}
        >>> print reward_values
        Average Rewards
    """

    def __init__(self, label, img_name=None):
        self.label = label
        self.img_name = img_name

    def __str__(self):
        return self.label


# List of rewards lines for the first graph
REWARD_VALUES = Result("Average rewards", "average_rewards")
# List of optimal values percentages lines for the second graph
OPTIMAL_ACTIONS_VALUES = Result("Percentage of optimal value",
                                "optimal_action")


@execution_time
def game(nb_plays=1000, nb_actions=10, nb_bandits=2000, egreedy=0):
    bandits = [Bandit(nb_actions) for x in range(nb_bandits)]

    print "- game start"
    for bandit in bandits:
        for i in range(nb_actions, nb_plays):
            bandit.play_egreedy(egreedy)
        print "'",  # Trace computation
    print "- game end"

    # We have a list of bandits, each containing an history of rewards. Le's
    # merge them
    rewards = zip(*[bandit.rewards for bandit in bandits])
    average_rewards = [np.mean(results) for results in rewards]
    REWARD_VALUES[egreedy] = average_rewards

    # For each bandit, we have a list of boolean representing if the play was
    # the optimal action or not. Gather this as percentages
    l_optimal_actions = zip(*[bandit.l_is_optimal for bandit in bandits])
    optimal_actions = [float(sum(results)) / len(results) * 100 for results in
                       l_optimal_actions]
    OPTIMAL_ACTIONS_VALUES[egreedy] = optimal_actions


def main():
    """
    For egreedy in [0, 0.01, 0.1]:

    - Create a Bandit with 10 possible actions and plays 1000 times.
    - Repeat the whole thing 2000 times and average the results.
    """
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # for a better print

    # Let's record the execution times
    start = time.time()

    # greedy game
    game()

    # egreedy games
    game(egreedy=0.1)
    game(egreedy=0.01)

    end = time.time()
    total_time = time.gmtime(end - start)
    print "The total computation took: %dh:%d:%d\n" % (total_time.tm_hour,
        total_time.tm_min, total_time.tm_sec)

    # Draw graphs
    draw(REWARD_VALUES)
    draw(OPTIMAL_ACTIONS_VALUES)


if __name__ == '__main__':
    main()
