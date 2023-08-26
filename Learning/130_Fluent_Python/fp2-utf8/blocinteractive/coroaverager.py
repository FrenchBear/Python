# Example 17-39. coroaverager.py: continuing from Example 17-38

>>> coro_avg.send(20)
16.25
>>> coro_avg.close()
>>> coro_avg.close()
>>> coro_avg.send(5)
Traceback (most recent call last):
  ...
StopIteration
