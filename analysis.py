#!/usr/bin/env python3

from notmuchData import mailDir, getData
from notmuch import Database
import math
import matplotlib.pyplot as plt
import sys
import numpy as np

dbpath = "maildirs/arch-dev-public"

def complot(CDF,xfun=0,yfun=0):
    """Given a CDF (or something like it) in input, prints it xfun-yfun."""
    if xfun != 0:
        a = xfun
        b = xfun
    else:
        a = lambda x: x
        b = lambda x: x
    if yfun != 0:
        b = yfun

    x = [ a(i) for i in range(1,len(CDF)+1) ]
    y = [ b(i) for i in CDF ]

    plt.plot(x,y,'r.')
    plt.show()

def plot_log(CDF):
    """Given a CDF (or something like it) in input, prints it log-log."""
    x = [ math.log(i) for i in range(1,len(CDF)+1) ]
    y = [ math.log(i) for i in CDF ]

    plt.plot(x,y,'r.')
    plt.show()

def cdf_from_data(data):
    """Data is an array or a list of numbers (ideally numbers of occurrencies,
    meaning that [1,5,8] means that specimen 0 occurred 1 time, specimen 1
    occurred 5 times, and so on). Compute the CDF and return it as an array."""
    relative_freq = np.array([
        len(list(
            filter(
                lambda x: x > index,
                data
            )
        )) for index in range(max(data))
    ])
    tot = 0
    for x in relative_freq: tot += x
    cdf = np.true_divide(relative_freq, tot)
    return cdf

def do_threads(path):
    data = getData(path).mex_in_threads()
    CDF = cdf_from_data(data)
    return CDF

def do_addresses_in_threads(path):
    data = getData(path).addresses_in_threads()
    CDF = cdf_from_data(data)
    return CDF

def do_all(path):
    data = getData(path).addresses()
    CDF = cdf_from_data(data)
    return CDF

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = dbpath
    CDF = do_threads(path)
    plt.loglog(np.arange(1,len(CDF)+1),CDF,'r.')
    plt.show()
