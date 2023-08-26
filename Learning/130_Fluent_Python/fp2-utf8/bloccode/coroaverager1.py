# Example 31-6. coroaverager1.py: doctest and code for a running average coroutine using the @coroutine decorator from Example 31-5

"""
A coroutine to compute a running average

    >>> coro_avg = averager()
    >>> from inspect import getgeneratorstate
    >>> getgeneratorstate(coro_avg)
    'GEN_SUSPENDED'
    >>> coro_avg.send(10)
    10.0
    >>> coro_avg.send(30)
    20.0
    >>> coro_avg.send(5)
    15.0
"""

from coroutil import coroutine

@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count
