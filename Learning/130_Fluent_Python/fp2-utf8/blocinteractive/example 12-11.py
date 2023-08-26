# Example 12-11. Three ways of calculating the accumulated xor of integers from 0 to 5

>>> n = 0
>>> for i in range(1, 6):
...     n ^= i
...
>>> n
1
>>> import functools
>>> functools.reduce(lambda a, b: a^b, range(6))
1
>>> import operator
>>> functools.reduce(operator.xor, range(6))
1
