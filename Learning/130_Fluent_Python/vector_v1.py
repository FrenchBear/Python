# vector_v2.py
# Variation on chapter 12, Vector Take #1
# For instance, constructor is more versatile here
#
# 2023-08-02    PV

from array import array
from collections.abc import Iterable
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

v1 = Vector([3,4])
print(repr(v1))
v2 = Vector(3,4)
print(v2)
v3 = Vector(1)
print(v3)
v4 = Vector(*range(10))
print(v4, bool(v4))
v5 = Vector([0,0,0,0,0])
print(v5, bool(v5))

class VectorFloat(Vector):
    typecode = 'f'

vf1 = VectorFloat(1,2,3)
b1 = bytes(vf1)
print(len(b1))
vd2 = Vector.frombytes(b1)
b2 = bytes(vd2)
print(len(b2))
print(vf1==vd2)

