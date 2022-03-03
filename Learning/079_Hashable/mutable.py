# mutable.py
# play with immutable hashable class
# 2021-03-02    PV
# 2021-03-07    PV      Test virtual methods and @property x is read only (a getter only)

import math


# Playing class
class Vect2D:
    typecode = 'd'

    def __init__(self, x, y) -> None:
        self.__x = x        # __ makes __x private (at least declaratively, the name is just decorated in dir())
        self.__y = y

    # Makes this a readonly accessor
    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __str__(self) -> str:
        return f"({self.__x}, {self.__y})"

    def __repr__(self) -> str:
        #return f"Vect2D({repr(self.__x)}, {repr(self.__y)})"
        return '{}({!r}, {!r})'.format(type(self).__name__, *self)

    def __iter__(self):
        yield self.__x
        yield self.__y

    def __eq__(self, o: object) -> bool:
        return self.__x == o.__x and self.__y == o.__y      # type: ignore[attr-defined]

    def __hash__(self) -> int:
        return hash(self.__x) ^ hash(self.__y)

    def mutate(self):
        self.__x = self.__x + 12

    def __complex__(self):
        return complex(self.__x, self.__y)

    # __int__ and __float__ do not make sense here

    def __bool__(self):
        return bool(abs(self))

    def __abs__(self):
        return math.hypot(self.__x, self.__y)

    def argument(self):
        return math.atan2(self.__y, self.__x)

    def __format__(self, format_spec: str) -> str:
        if format_spec == None:
            return str(self)
        if format_spec.endswith('r'):
            nf = '{:'+format_spec[:-1]+'f}'
            return '('+nf.format(self.x)+', '+nf.format(self.y)+')'
        if format_spec.endswith('p'):
            nf = '{:'+format_spec[:-1]+'f}'
            import math
            arg = math.atan2(self.y, self.x)
            mod = math.hypot(self.x, self.y)
            return '('+nf.format(mod)+' ∠'+nf.format(arg)+')'
        return str(self)

    def __bytes__(self):
        from array import array
        return bytes([ord(self.typecode)])+bytes(array(self.typecode, self))

    @classmethod
    def frombytes(cls, octets):
        typecode=chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)

    def virt_method(self):
        print('Vect2D.virt_method()')

    def test_virt(self):
        print(self.virt_method())

class SubVect2D(Vect2D):
    def virt_method(self):
        print('SubVect2D.virt_method()')

v1 = Vect2D(3, 4)
v2 = Vect2D(4, 3)

print(v1, 'hash:', hash(v1))
print(v2, 'hash:', hash(v2))

v3 = Vect2D('a', (3.14, 1.732))
print(repr(v3), 'hash:', hash(v3))

d = {}
d[v1] = 'vect1'
v1.mutate()
# print(d[v1])        # fails, a hashable object should be immutable
print(v1.x)
# v1.x = 7            # AttributeError: can't set attribute

# print(v1.__x)       # Error: 'Vect2D' object has no attribute '__x'
print(v1._Vect2D__x)  # type: ignore[attr-defined]    # Cheating...
v1._Vect2D__x = 7     # type: ignore[attr-defined]    # even worse cheating
print(v1)
print(complex(v1))    # use __complex__
print('abs=', abs(v1), ', arg=', v1.argument()) # use __abs__
print(format(v1, '.3r'), format(v1, '.3p'))  # custom formats, rect and polar
print(tuple(v1))      # v1 is iterable

print()
b = bytes(v1)
print(Vect2D.frombytes(b))      # Members converted to float because of typecode d

# In python, class functions are always 'virtual'
v1.test_virt()
sv1 = SubVect2D(2, 3)
sv1.test_virt()     # test_virt is in base class Vect2D, but it calls virt_method of SubVect2D
