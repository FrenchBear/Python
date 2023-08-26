# Example 7-6. Sum of integers up to 99 performed with reduce and sum

>>> from functools import reduce
>>> from operator import add
>>> reduce(add, range(100))
4950
>>> sum(range(100))
4950
