#!/usr/bin/env python3

from notmuchData import mailDir, getData
from notmuch import Database
import math
import matplotlib.pyplot as plt
import sys
import numpy as np
import powerlaw

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

def do_stuff(data):
    fit = powerlaw.Fit(data)
    fig1 = fit.plot_pdf(color='b', linewidth=2)
    fit.power_law.plot_pdf(color='b', linestyle='--', ax=fig1)
    fit.plot_ccdf(color='r', linewidth=2, ax=fig1)
    fit.power_law.plot_ccdf(color='r', linestyle='--', ax=fig1)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = dbpath
    data = getData(path).addresses()
    do_stuff(data)
