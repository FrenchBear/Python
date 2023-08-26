# Example 31-14. coroaverager2.py: doctest showing the behavior of averager

>>> coro_avg = averager()
>>> next(coro_avg)
>>> coro_avg.send(10)
>>> coro_avg.send(30)
>>> coro_avg.send(6.5)
>>> coro_avg.send(None)
Traceback (most recent call last):
   ...
StopIteration: Result(count=3, average=15.5)
