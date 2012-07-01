==========================
The n-Armed Bandit Problem
==========================

Introduction
============

Welcome ! This is the first entry of a series of posts related to Reinforcement
learning.

I'll try to keep the same structure for each entry, which is:

- a math lesson

- a problem

- python code used to resolve this problem

- result

If you have any suggestions to improve my entries, I'd be grateful to hear them
from you !

Enough talk, let's start with the math lesson.


Math 1: Gaussian distribution
=============================

A Gaussian distribution is a symmetric curved shape that falls off towards +/-
infinity. Here is its formula:

.. math::

    ae^{-\frac{(x-b)_2}{2c_2}}

And here is its graphical representation:

.. image:: /static/reinforcement_learning/gaussian.png
    :alt: "Normalized Gaussian curves with expected value \03bc and variance \03c3"
    :width: 30em
    :align: right

This graph has been generated from this code:

.. colored_include:: python
    :linenos:
    :path: reinforcement_learning/10-armed_testbed/gaussian.py

.. colored_include is my custom directive made from pygments and include

For more information on **Gaussian Distributions**, `the wiki page
<http://en.wikipedia.org/wiki/Gaussian_function>`_ is well
documented.


Goal
====

Consider the following learning problem. You are faced repeatedly with a choice
among n different options, or actions. After each choice you receive a numerical
reward chosen from a stationary probability distribution that depends on the
action you selected. Your objective is to maximize the expected total reward over
some time period, for example, over 1000 action selections. Each action
selection is called a play.

This is the original form of the ``n-armed bandit problem``, so named by analogy
to a slot machine, or "one-armed bandit", except that it has n levers instead of
one.


``Source:`` *Reinforcement Learning*, by ``Richard S. Sutton`` and ``Andrew G.  Barto``


Explanations
============

This problem will be solved with the following values:

    - The bandit has 10 levers (10 actions).
    - We will play 1000 times on a Bandit.
    - We will repeat the same game 2000 times and average the results.

Let's consider the following statements:

    - Choose among n different actions repeatedly.
    - Each lever gives a reward calculated from a `normal distribution 
      <http://en.wikipedia.org/wiki/Normal_distribution>`_ N(0,1).
    - Each action has an optimal value, not known by the program.
      Each action has an estimated value, which is the average of received
      rewards at a given time.
    - A greedy action is the action whose estimated value is the greatest.

At the beginning of the game, we don't know anything. What are the rewards given
for each lever ? We will then give to all actions the estimated value 0
at the beginning.

If an action always gave the same reward, then the solution would be extremely
simple: after discovering each action's value, choose the highest one and only
play it.  But here, things are more subtile.

Let's call |Q*(a)| the true value of the action a, and |Qt(a)| the estimated
value of the action a at the |tth| play. We can state the following equation:

.. |Q*(a)| replace:: Q\ :sup:`*`\ (a)

.. |Qt(a)| replace:: Q\ :sub:`t`\ (a)

.. |tth| replace:: t\ :sup:`th`


.. math::

    Q"{*}(a) = \frac{1}{\sqrt{2\pi\sigma_2}} e^{-\frac{(x - \mu)_2}{2 * \sigma_2}}


At each time t, the average reward for an action a will be:

.. math::

    Q_{t}(a) = \frac{r1 + r2 + \ldots + r_{k_{a}}}{k_{a}}


We can create an Action class following these rules:

- An action has a play method to give a new reward

- Each instance of Action will get a value at the initialization.

- Each instance keep track of its estimated value |Qt(a)|

.. colored_include:: python
    :linenos:
    :start-line: 73
    :path: reinforcement_learning/10-armed_testbed/models.py


Then, we need a Bandit class which will contains a set of actions and make them
play:

- The bandit can explores (randomly choose between other actions than the
  greedy one.

- The bandit can exploits (play the greedy move and maximize the result)

- Of course, the bandit need to choose between exploration and exploitation
  depending on its e-greedy action/value method.

.. colored_include:: python
    :linenos:
    :start-line: 13
    :end-line: 72
    :path: reinforcement_learning/10-armed_testbed/models.py


Now we have everything. I created a small class to store the datas to render
the graphs. The class keep the name of the graph, and a list of lines (name and
values):

.. colored_include:: python
    :linenos:
    :start-line: 17
    :end-line: 35
    :path: reinforcement_learning/10-armed_testbed/main.py

I also created a game view (could have been a class though) for each strategy,
and the main view to start the computation:

.. colored_include:: python
    :linenos:
    :start-line: 43
    :end-line: 96
    :path: reinforcement_learning/10-armed_testbed/main.py


Result
======

After 3 hours of computation (could have been faster, but I was doing some other
stuff in the same time, so it didn't get 100\% of the cpu allocated),
my program finally generated the graphs ... 1000 actions per bandit *
2000 bandits * 3 strategies (greedy, e-greedy 0.01 and e-greedy 0.1) means that
it played 6 000 000 actions !

.. image:: /static/reinforcement_learning/average_rewards.png
    :alt: "Average rewards for 2000 Bandits"
    :width: 23.5em
    :align: left

.. image:: /static/reinforcement_learning/optimal_action.png
    :alt: "Percentage of optimal actions found for 2000 Bandits"
    :width: 23.5em
    :align: right

The first graph shows that a greedy play will get an average reward of 1.0, when
e-greedy plays are able to get a much better result. In a long term, the
0.01 e-greedy method will be more profitable than the 0.1 one, because once
the optimal action found, he will loose a lot less actions by exploring worse
actions.

The second graph show us that a greedy method will only find the best action
35\% of the time. Quite bad for the 65\% games remaining. We can also see that
the 0.1 e-greedy method find the best action much more faster than the
0.01 e-greedy one, which mean we have some space left for improvement:
For example, we could start the game with a bigger rule, and reduce it after
some time, to get the best of each e-greedy method.


Tests
=====

Tests are an important matter during the development. It saved me lots of time
while coding, as some bugs would have been really hard to track without them.
That's when **Tests Driven Development** is really useful: start by
writing your tests, and then write your code to make your tests working.

A good code should be covered by tests around 80% (less open doors to more
problems difficult to debug, and more take really to much of the developer's
time). For this project, here is my coverage::

    $ cd /path/to/project
    (fandekasp)$ py.test --doctest-modules --cov .

========================= ======= ====== =====
Name                       Stmts   Miss  Cover
========================= ======= ====== =====
__init__                       0      0   100%
fixtures/__init__              0      0   100%
fixtures/average_rewards       3      0   100%
fixtures/optimal_action        3      0   100%
fixtures/rewards               2      0   100%
fixtures/test                  2      0   100%
gaussian                      15      9    40%
gorun_settings                 1      0   100%
main                          43     11    74%
models                        53      1    98%
test_bandit                   77      0   100%
utils                         33     13    61%
------------------------- ------- ------ -----
TOTAL                        232     34    85%
========================= ======= ====== =====

You will be able to find the code for the tests in the download archive behind.


Code
====

You can download the whole project here_.

.. _here: /static/reinforcement_learning/10-armed_testbed.tar


Conclusion
==========

That's it for my first entry related to Reinforcement Learning, hope you liked
it! I'm not used to writing articles, so it's far away from being perfect, but
I'll improve my skills with the following ones !

Bye bye,
Fandekasp
