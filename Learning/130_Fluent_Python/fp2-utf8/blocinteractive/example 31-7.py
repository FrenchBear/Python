# Example 31-7. How an unhandled exception kills a coroutine

>>> from coroaverager1 import averager
>>> coro_avg = averager()
>>> coro_avg.send(40)
40.0
>>> coro_avg.send(50)
45.0
>>> coro_avg.send('spam')
Traceback (most recent call last):
  ...
TypeError: unsupported operand type(s) for +=: 'float' and 'str'
>>> coro_avg.send(60)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
