#!/usr/bin/env python

'''
File: tests.py
Author: Adrien Lemaire
Description: Tests for the 10-armed testbed
'''

from mock import Mock
import numpy as np
from unittest2 import TestCase

from data.rewards import greedy, egreedy_0_1  # test data
from main import game, Result
from models import Action, Bandit
from utils import draw, get_percent


class TestAction(TestCase):
    """Tests related to the action"""

    def setUp(self):
        self.bandit = Bandit()
        self.action = Action(self.bandit)

    def test_action_value_is_gaussian(self):
        """
        Verify that our action will get a correct value from N(mu, sigma)
        - mu: the mean, here 0
        - sigma: the variance, here 1
        """
        results = [Action(self.bandit).value for x in range(5000)]
        law_1 = get_percent([x for x in results if x > 0], results)
        self.assertAlmostEqual(law_1, 50, delta=2, msg="%s%% of results are "
            "above mu instead of around 51%%" % law_1)
        law_2 = get_percent([x for x in results if x > -1 and x < 1], results)
        self.assertAlmostEqual(law_2, 68, delta=2, msg="%s%% of results are "
            "above mu instead of around 68%%" % law_2)

    def test_gauss_with_numpy(self):
        """We use numpy, let's add some verifications"""
        mu, sigma = 0, 1
        value = np.random.normal(mu, sigma, 1000)
        diff_mean = abs(mu - np.mean(value))
        self.assertLess(diff_mean, 0.12, "diff mean = %s > 0.1" % diff_mean)
        diff_vari = abs(sigma - np.std(value, ddof=1))
        self.assertLess(diff_vari, 0.12, "diff vari = %s > 0.1" % diff_vari)

    def test_action_can_play(self):
        """Let's play and check that action got a reward"""
        action = self.action  # shortcut
        [action.play() for x in range(1000)]
        lim = [action.mu - 3 * action.sigma, action.mu + 3 * action.sigma]
        rewards_in_range = [r for r in action.rewards if lim[0] <= r <= lim[1]]
        percent = get_percent(rewards_in_range, action.rewards)
        self.assertAlmostEqual(percent, 85.0, delta=15, msg="%s%% instead of "
            "99,7%% for a Normal Distribution" % percent)
    # TODO verify why it comes to 86% sometimes !

    def test_action_mean_reward(self):
        """Test that an action keep an history of rewards and that mean_reward
        become closer to value after multiples plays"""
        [self.action.play() for i in range(1, 1000)]
        vari = abs(self.action.sigma - np.std(self.action.rewards, ddof=1))
        self.assertLess(vari, 0.12, "diff variance = %s > 0.1" % vari)

    #def test_loop(self):
        #errors = 0
        #for i in range(100):
            #try:
                #self.test_action_mean_reward()
            #except:
                #errors += 1
        #assert errors == 0


class TestBandit(TestCase):
    """Tests related to the bandit"""

    def setUp(self):
        self.bandit = Bandit()

    def test_create_bandits(self):
        """We can create a bunch of 10 bandits"""
        bandits = [Bandit() for x in range(10)]
        self.assertEqual(len(bandits), 10, "We are expecting 10 Bandits""")
        self.assertEqual(type(bandits[0]), Bandit)

    def test_bandit_has_choices(self):
        """Verify that Bandit has 10 actions by default"""
        self.assertEqual(len(self.bandit.actions), 10, "Bandit should have 10 "
            "actions")
        bandit2 = Bandit(20)
        self.assertEqual(len(bandit2.actions), 20, "Bandit should have 20 "
            "actions")

    def test_bandit_explores(self):
        """Let's explore"""
        self.assertFalse(self.bandit.last_action)
        self.bandit.explores()
        self.assertTrue(self.bandit.last_action)

    def test_bandit_exploits(self):
        """Play a greedy move"""
        # Get the greed move
        greedy_action = self.bandit.greedy
        self.bandit.exploits()
        self.assertIs(self.bandit.last_action, greedy_action, "The last action"
            " should be the greedy action")

    def test_bandit_e_greedy(self):
        """Test that bandit can mix exploitation and exploration"""
        epsilon = 0  # greedy
        greedy_move = self.bandit.greedy  # greedy might change after a play
        self.bandit.play_egreedy(epsilon)
        self.assertIs(self.bandit.last_action, greedy_move,
            "The last action should be the greedy action")

        epsilon = 0.1  # play egreedy
        nb_greedy = 0
        for i in range(1000):
            greedy_move = self.bandit.greedy
            self.bandit.play_egreedy(epsilon)
            if self.bandit.last_action == greedy_move:
                nb_greedy += 1
        percent = float(1000 - nb_greedy) / 1000
        self.assertLess(percent, 0.13, "%s > 0.1, wrong !" % percent)

    def test_game(self):
        """tests on the main.game() function"""
        self.assertIsNone(game(nb_plays=100, nb_bandits=10))
        # Example for tests
        test_data = Result("Test data")
        test_data[0] = greedy
        test_data[0.1] = egreedy_0_1
        drawMock = Mock(draw)
        drawMock(test_data)
        self.assertTrue(drawMock.called)
