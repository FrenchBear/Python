# vector_v2.py
# Variation on chapter 12, Vector Take #2
#
# 2023-08-05    PV


from array import array
from collections.abc import Iterable
import operator
import reprlib
import math

class Vector:
    typecode = 'd'

    def __init__(self, *components):
        if len(components)==1 and isinstance(components[0], Iterable):
            self._components = array(self.typecode, components[0])
        else:
            self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        t = self.__class__.__name__
        return f'{t}({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self) -> bytes:
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(*self)

    def __bool__(self):
        #return bool(abs(self))
        return any(self)

    @classmethod
    def frombytes(cls, octets: bytes):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)
        return self._components[index]


v7 = Vector(range(7))
print(v7[-1])
print(v7[1:4])
print(v7[-1:])
print(v7[::-1])
print(v7[1,2])
