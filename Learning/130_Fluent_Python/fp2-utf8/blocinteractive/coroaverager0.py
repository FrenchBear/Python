# Example 31-4. coroaverager0.py: doctest for the running average coroutine in Example 31-3

>>> coro_avg = averager()
>>> next(coro_avg)
>>> coro_avg.send(10)
10.0
>>> coro_avg.send(30)
20.0
>>> coro_avg.send(5)
15.0
