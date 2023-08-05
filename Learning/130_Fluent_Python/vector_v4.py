# vector_v4.py
# Variation on chapter 12, Vector Take #4
#
# 2023-08-05    PV


from array import array
from collections.abc import Iterable
import operator
import reprlib
import math
import functools

class Vector:
    typecode = 'd'
    __match_args__ = ('x', 'y', 'z', 't')  

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

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        msg = f'{cls.__name__!r} object has no attribute {name!r}'
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.__match_args__:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

v7 = Vector(range(7))
print(v7[-1])
print(v7[1:4])
print(v7[-1:])
print(v7[::-1])
#print(v7[1,2])

print(v7.x, v7.y, v7.z, v7.t)
v7.ψ='blue'
