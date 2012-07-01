#!/usr/bin/env python

'''
File: models.py
Author: Adrien Lemaire
Description: classes for the 10-armed testbed
'''

import numpy as np
import fractions
import random


class Bandit(object):
    """A Bandit with n-levers"""

    def __init__(self, nb_actions=10):
        """
        rewards = history of rewards for each play on this Bandit
        l_is_optimal = list of boolean, true if this play was optimal
        """
        super(Bandit, self).__init__()
        self.rewards = []
        self.l_is_optimal = []
        self.last_action = False
        self.actions = self.create_actions(nb_actions)

    @property
    def greedy(self):
        """Find action whose estimated value is greatest"""
        greedy_value = max([action.estimated_value for action in self.actions])
        for action in self.actions:
            if action.estimated_value == greedy_value:
                return action

    def set_last_action(self, action):
        """Save some stats"""
        # Update the last action
        self.last_action = action
        # update the rewards list
        self.rewards.append(action.rewards[-1])
        self.l_is_optimal.append(action == self.optimal_action)

    def create_actions(self, nb_actions):
        """Generate ``nb_actions`` Action(), and save the optimal_action"""
        actions = [Action(self) for x in range(nb_actions)]
        optimal_value = max([action.value for action in actions])
        for action in actions:
            if action.value == optimal_value:
                self.optimal_action = action
                return actions

    def explores(self):
        """Choose an action randomly and play it."""
        # We remove the greedy play from the list to choose
        action = random.choice([x for x in self.actions if x != self.greedy])
        action.play()

    def exploits(self):
        """Let's play the best move we know"""
        self.greedy.play()

    def play_egreedy(self, epsilon, nb_decimals=3):
        """Exploit or explore depending on epsilon
        Default 3 decimales max for epsilon"""
        x = int(10 ** nb_decimals * round((1 - epsilon), nb_decimals))
        y = int(10 ** nb_decimals * round(epsilon, nb_decimals))
        gcd = fractions.gcd(x, y)
        x /= gcd
        y /= gcd
        random.choice([self.exploits] * x + [self.explores] * y)()


class Action(object):
    """An action/lever of the bandit"""

    def __init__(self, parent, mu=0, sigma=1):
        """Each Q*(a)/value is chosen randomly from N(0, 1)"""
        self.parent = parent
        self.mu = mu
        self.sigma = sigma
        self.rewards = [0]  # History of rewards of this instance
        self.value = np.random.normal(self.mu, self.sigma)

    def __str__(self):
        return "action (%s)" % self.value

    @property
    def estimated_value(self):
        """Return the mean of each rewards"""
        return np.mean(self.rewards)

    def play(self):
        """Each r is also normal: N(Q*(a), 1)"""
        self.rewards.append(np.random.normal(self.value, self.sigma))
        self.parent.set_last_action(self)
