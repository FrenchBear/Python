>>> def gen123():
...     yield from [1, 2, 3]
...
>>> tuple(gen123())
(1, 2, 3)
