#!/usr/bin/env python

'''
File: utils.py
Author: Adrien Lemaire
Description: Utils functions
'''

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time


def get_percent(value, results):
    """return percentage of value in results"""
    return len(value) / float(len(results)) * 100


class execution_time(object):
    """Time logger decorator"""

    def __init__(self, func):
        self.func = func
        self.__name__ = self.func.__doc__

    def __call__(self, *args, **kwargs):
        start = time.time()
        result = self.func(*args, **kwargs)
        end = time.time()
        total_time = time.gmtime(end - start)
        print "the function `%s` took: %dh:%d:%d\n" % (self.func,
            total_time.tm_hour, total_time.tm_min, total_time.tm_sec)
        return result

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


def draw(result):
    """Save values in fixtures and render a matplotlib graph in results"""
    f = open("fixtures/%s.py" % result.img_name, "w")

    for label, values in result.iteritems():
        # Draw each line
        plt.plot(values, label=str(label))
        # write data in file
        file_label = str(label).replace(".", "_")
        f.write("%s_%s = %s\n" % (result.img_name, file_label, values))
    f.close()
    # Set axes labels
    plt.ylabel(str(result))
    plt.xlabel("Plays")
    plt.legend()

    if result.img_name:
        plt.savefig('results/%s.png' % result.img_name)  # Save graph
        print "The image %s.png has been saved" % result.img_name
