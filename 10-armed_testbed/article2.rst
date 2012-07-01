==============================
The n-Armed Bandit Problem (2)
==============================

Introduction
============

After discovering the **E-greedy** action-value methods on the 10-armed_testbed
in `my first article <>`_, we'll see today another method called **Softmax**,
which grade action probabilities by estimated values.

The most common softmax uses a Gibbs or Boltzmann distribution


Math 2: Boltzmann Distribution
==============================

Gases are composed of of atoms or molecules. These atoms or molecules do not
really interact with each other except through collisions. In many cases, we may
think of a gas as a collection of tiny billiard balls flying through space,
hitting one another again and again. Even if we were to think that all atoms or
molecules had the same speed to begin with (although we do not), the constant
collisions would result in a spread of many speeds. Some atoms could have very
high speeds, others low ones. In real gases at equilibrium there is a
distribution of speeds. This distribution is called the `Maxwell-Boltzmann
distribution`, and it depends on temperature, as shown. The high temperature
curve has proportionally many more fast molecules or atoms than the low
temperature curves. As the temperature rises, the highest point on the curve is
pushed out to higher v, and the maxium is pushed down toward the axis. All
curves shown below have a similarity in their shape.
