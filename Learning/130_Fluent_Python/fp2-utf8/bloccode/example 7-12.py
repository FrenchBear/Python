# Example 7-12. Factorial implemented with reduce and operator.mul

from functools import reduce
from operator import mul

def factorial(n):
    return reduce(mul, range(1, n+1))
