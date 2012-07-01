#!/usr/bin/env python
"""Simple script to generate some normalized gaussian curves in a graph"""

from matplotlib.mlab import normpdf
import matplotlib.numerix as nx
import pylab as p


def gaussian_example():
    """Create graph with 4 gaussian distributions"""

    x = nx.arange(-4, 4, 0.01)
    list_sigma = [0.2, 0.5, 1, 2]
    for sigma in list_sigma:
        y = normpdf(x, 0, sigma) # unit normal
        p.plot(x,y, lw=2)
    p.legend(["$\sigma = %s$" % s for s in list_sigma])
    p.title("Normal Gaussian Distribution")
    p.savefig('results/gaussian.png')  # Save graph


if __name__ == '__main__':
    gaussian_example()
