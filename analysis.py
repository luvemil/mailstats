#!/usr/bin/env python3

from notmuchData import mailDir
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

class getData(Database):
    """docstring for getData"""
    def __init__(self, *args, **kwargs):
        super(getData, self).__init__(*args, **kwargs)

    def addresses(self):
        addrs = mailDir(self,"*").search_addresses()
        count = {}
        for addr in addrs:
            if addr in count:
                count[addr] += 1
            else:
                count[addr] = 1
        data = np.array(list(count.values()))
        return data

    def mex_in_threads(self):
        threads = mailDir(self,"*").search_threads()
        data = np.array(list(map(
            lambda x: x.get_total_messages(),
            threads
        )))
        return data

    def addresses_in_threads(self):
        threads = mailDir(self,"*").search_threads()
        data = []
        for thread in threads:
            data.append(
                mailDir(self,
                        "thread:"+thread.get_thread_id()).count_addresses()
            )
        return np.array(data)

def do_threads(path):
    data = getData(path).mex_in_threads()
    CDF = cdf_from_data(data)
    complot(CDF, math.log)

def do_addresses_in_threads(path):
    data = getData(path).addresses_in_threads()
    CDF = cdf_from_data(data)
    complot(CDF,math.log)

def do_all(path):
    data = getData(path).addresses()
    CDF = cdf_from_data(data)
    complot(CDF, math.log)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = dbpath
    do_addresses_in_threads(path)
