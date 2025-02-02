# Example 17-6. A generator function that yields three numbers

>>> def gen_123():
...     yield 1
...     yield 2
...     yield 3
...
>>> gen_123  # doctest: +ELLIPSIS
<function gen_123 at 0x...>
>>> gen_123()   # doctest: +ELLIPSIS
<generator object gen_123 at 0x...>
>>> for i in gen_123():
...     print(i)
1
2
3
>>> g = gen_123()
>>> next(g)
1
>>> next(g)
2
>>> next(g)
3
>>> next(g)
Traceback (most recent call last):
  ...
StopIteration
