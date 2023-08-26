# Example 17-12. The ArithmeticProgression class

from decimal import Decimal
from fractions import Fraction
import itertools

class ArithmeticProgression:
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end  # None -> "infinite" series

    # To make an ArithmeticProgression object, __iter__ can be a generator instead of returning an explicit iterator
    def __iter__(self):
        result_type = type(self.begin + self.step)
        result = result_type(self.begin)
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index


ap = ArithmeticProgression(0, 1, 3)
print(list(ap))
ap = ArithmeticProgression(1, .5, 3)
print(list(ap))
ap = ArithmeticProgression(0, 1 / 3, 1)
print(list(ap))
ap = ArithmeticProgression(0, Fraction(1, 3), 1)
print(list(ap))
ap = ArithmeticProgression(0, Decimal('.1'), .3)
print(list(ap))
ap = ArithmeticProgression('', 'A', 'AAAA')     # Ok, not arithmetic, but works...
print(list(ap))
print()

# Simpler:
def aritprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index

# v3
# Not a generator function (doesn't contain yield keyword), but returns a generator nonetheless
# Note that itertools.cound adds step repeteadly, so oit's not as precise as previous versions
# and doesn't work with strings
def aritprog_gen3(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    return ap_gen if end is None else itertools.takewhile(lambda n: n < end, ap_gen)


print(list(aritprog_gen3(0, 1, 3)))
print(list(aritprog_gen3(1, .5, 3)))
print(list(aritprog_gen3(0, 1 / 3, 1)))
print(list(aritprog_gen3(0, Fraction(1, 3), 1)))
print(list(aritprog_gen3(0, Decimal('.1'), .3)))
