# Example 12-12. Part of vector_v4.py: two imports and __hash__ method added to the Vector class from vector_v3.py

from array import array
import reprlib
import math
import functools
import operator


class Vector:
    typecode = 'd'

    # many lines omitted in book listing...

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

# more lines omitted...
